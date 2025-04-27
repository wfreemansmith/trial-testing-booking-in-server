from src.db import get_database
from typing import TypedDict, BinaryIO, List
from src.dao.candidate_dao import CandidateDAO
from src.dao.version_dao import VersionDAO
import pandas as pd
import json

class CandidateDict(TypedDict):
    candidate_number: int
    candidate_name: str
    paper_sat: str
    writing_version: str
    reading_version: str
    listening_version: str
    writing_version_id: str
    reading_version_id: str
    listening_version_id: str
    errors: list

class BatchDict(TypedDict):
    version_id: str
    component_id: str
    errors: list

class ErrorMessage(TypedDict):
    field: str
    message: str

# read file
# check candidate details are complete
# check candidate numbers are not already in database
## flag errors if numbers are repeated, if number & candidate are repeated do not proceed
# check versions are in the database
# format dataframe as a dict


def error_message(field, message=None) -> ErrorMessage:
    """Appends an error to relevant array in dataframe, indicating which row and field is problematic"""
    return {
        "field": field,
        "message": message
    }


def validate_candidate(dao: CandidateDAO, marking_window_id: int, centre_num: str, candidate: CandidateDict, position: int) -> list:
    """Checks candidate dict, returns error messages if any error"""
    errors = []
    candidate_name = candidate.get("candidate_name")
    candidate_number = candidate.get("candidate_number")

    # check for blanks etc
    if not candidate_name or not len(candidate_name):
        error = error_message("candidate_name", "Candidate name cannot be blank. Please provide a name for the candidate.")
        errors.append(error)
    
    if not candidate_number:
        error = error_message("candidate_number", "Candidate number cannot be blank or zero. Please provide a candidate number that you have not used previously.")
        errors.append(error)

    # check database here
    duplicate = dao.is_duplicate_candidate(marking_window_id, centre_num, candidate_name, candidate_number)
    if duplicate and type(duplicate) is int:
        candidate['candidate_number'] = duplicate + position
        error = error_message("candidate_number", "Candidate number was already found in our records. We have updated duplicate candidate numbers on your register. Please amend your test materials before scanning and uploading to reflect these changes.")
        errors.append(error)
    elif duplicate:
        error = error_message("duplicate")
        errors.append(error)

    return errors


def process_register_file(centre_num: str, marking_window_id: int, file: BinaryIO) -> tuple[
    List[CandidateDict],
    List[BatchDict]
    ]:
    """Receives a register and returns a list of candidate dicts and list of batch dicts"""
    df = pd.read_excel(file, header=4)

    # rename columns
    df = df.rename(
        columns={
            "Candidate Number": "candidate_number",
            "Candidate Name": "candidate_name",
            "Component": "paper_sat",
            "Reading": "reading_version",
            "Listening": "listening_version",
            "Writing": "writing_version"
            }
            )
    df = df.dropna(subset=['candidate_name'], how='all')

    # get columns
    string_columns = df.columns[1:]
    component_columns = df.columns[3:]

    # strip of spaces & additional info
    PREFIXES = ['ACW', 'ACR', 'GTR', 'GTW', 'List', 'LIST', 'L']
    for prefix in PREFIXES:
        df[component_columns] = df[component_columns].apply(lambda x: x.str.replace(prefix,''))
    df[string_columns] = df[string_columns].apply(lambda x: x.str.strip())

    # replace absent candidates with blank
    ABSENT_KEYWORDS = ["ABSENT", "ABS", "-", ""]
    df[component_columns] = df[component_columns].replace(ABSENT_KEYWORDS, None)

    # create database connection
    engine = get_database()
    version_dao = VersionDAO(engine)
    candidate_dao = CandidateDAO(engine)

    # get version ids & make batch data
    batches_data = []
    versions_not_found = []

    version_id_cols = ['reading_version_id', 'writing_version_id', 'listening_version_id']
    for version_id_col in version_id_cols:
        version_col_name = version_id_col.replace('_id', '')
        component_id = version_id_col[0].upper()

        # get version id
        if version_id_col != 'listening_version_id':
            version_id = df['paper_sat'] + component_id + df[version_col_name]
        else:
            version_id = component_id + df[version_col_name]
        df[version_id_col] = version_id

        # check database here
        errors = []
        version_exists = version_dao.version_exists(version_id)
        if not version_exists:
            versions_not_found.append(version_id)
            error = error_message("version_id", "This version cannot be found on the database. Please check the version, update your candidates, and try again. If you believe this is an error, please contact Cambridge.")
            errors.append(error)

        # collect batches data
        for idx, row in df.iterrows():
            if pd.notna(row[version_id_col]):
                batches_data.append((row[version_id_col], component_id, errors))
    
    # make batches df
    batches_df = pd.DataFrame(batches_data, columns=['version_id', 'component_id', 'errors'])
    batches_df = batches_df.dropna(subset=['version_id'])
    batches_df = batches_df.drop_duplicates(subset=['version_id'])
    batches_df = batches_df.sort_values(by=['version_id'], ascending=True)

    # get candidates dict
    candidates_df = df.copy()
    candidates_df['errors'] = [[] for _ in range(len(candidates_df))]
    candidates_list = candidates_df.to_dict(orient="records")
    
    # get batches dict
    batches_list = batches_df.to_dict(orient="records")
    
    # check candidate numbers against database
    for position, candidate in enumerate(candidates_list):
        errors = validate_candidate(candidate_dao, marking_window_id, centre_num, candidate, position)
        for version_id_col in version_id_cols:
            if candidate[version_id_col] in versions_not_found:
                version_error = error_message(version_id_col, "This version could not be found on the database, please double check")
                errors.append(version_error)        
        candidate['errors'].extend(errors)

    return candidates_list, batches_list
    # After this, remove duplicate candidates and add error message to JSON mentioning duplciates