from src.db import get_database
from typing import TypedDict, BinaryIO, List, Tuple
from src.dao.candidate_dao import CandidateDAO
from src.dao.version_dao import VersionDAO
import pandas as pd
from pandas import DataFrame


# type hints
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


# create database connection
engine = get_database()
version_dao = VersionDAO(engine)
candidate_dao = CandidateDAO(engine)


# constants
VERSION_ID_COLS = ['reading_version_id', 'writing_version_id', 'listening_version_id']
ABSENT_KEYWORDS = ["ABSENT", "ABS", "-", ""]


# validation functions
def error_message(field: str, message: str | None = None) -> ErrorMessage:
    """Returns an error to relevant array in dataframe, indicating which row and field is problematic"""
    return {
        "field": field,
        "message": message
    }


def validate_candidate(marking_window_id: int, centre_num: str, candidate: CandidateDict, position: int) -> List[ErrorMessage]:
    """Checks candidate dict against databsae, adjusts anything which can be adjusted, returns error messages if any error"""
    candidate_errors = []
    candidate_name = candidate.get("candidate_name")
    candidate_number = candidate.get("candidate_number")

    # check for blanks etc
    if not candidate_name or not len(candidate_name):
        error = error_message("candidate_name", "Candidate name cannot be blank. Please provide a name for the candidate.")
        candidate_errors.append(error)
    
    if not candidate_number:
        error = error_message("candidate_number", "Candidate number cannot be blank or zero. Please provide a candidate number that you have not used previously.")
        candidate_errors.append(error)

    # check database here
    duplicate = candidate_dao.is_duplicate_candidate(marking_window_id, centre_num, candidate_name, candidate_number)
    if duplicate and type(duplicate) is int:
        candidate['candidate_number'] = duplicate + position
        error = error_message("candidate_number", "Candidate number was already found in our records. We have updated duplicate candidate numbers on your register. Please amend your test materials before scanning and uploading to reflect these changes.")
        candidate_errors.append(error)
    elif duplicate:
        error = error_message("duplicate")
        candidate_errors.append(error)

    return candidate_errors


def validate_version(version_id: str) -> List[ErrorMessage]:
    """Checks version id on database, logs it as problematic, and returns an error if any are found"""
    version_errors = []
    version_exists = version_dao.version_exists(version_id)
    if not version_exists:
        error = error_message("version_id", f"Version cannot be found on the database. Please check the version, update your candidates, and try again. If you believe this is an error, please contact Cambridge.")
        version_errors.append(error)

    return version_errors


# df helper functions
def rename_columns(df: DataFrame) -> DataFrame:
    return df.rename(columns={
        "Candidate Number": "candidate_number",
        "Candidate Name": "candidate_name",
        "Component": "paper_sat",
        "Reading": "reading_version",
        "Listening": "listening_version",
        "Writing": "writing_version"
        })

def drop_empty_rows(df: DataFrame) -> DataFrame:
    return df.dropna(subset=['candidate_name'], how='all')

def strip_prefixes(df: DataFrame) -> DataFrame:
    component_columns = df.columns[3:]
    PREFIXES = ['ACW', 'ACR', 'GTR', 'GTW', 'List', 'LIST', 'L']
    for prefix in PREFIXES:
        df[component_columns] = df[component_columns].apply(
            lambda x: x.str.replace(prefix,'')
        )
    return df

def strip_strings(df: DataFrame) -> DataFrame:
    string_columns = df.columns[1:]
    df[string_columns] = df[string_columns].apply(lambda x: x.str.strip())
    return df

def replace_absent_candidates(df: DataFrame) -> DataFrame:
    component_columns = df.columns[3:]
    ABSENT_KEYWORDS = ["ABSENT", "ABS", "-", ""]
    df[component_columns] = df[component_columns].replace(ABSENT_KEYWORDS, None)
    return df    


# main functions
def ingest_excel_file(file: BinaryIO) -> Tuple[
    List[CandidateDict],
    List[BatchDict]
    ]:
    """Processes Excel file and returns a list of candidate dicts and a list of batch dicts"""
    df = (
        pd.read_excel(file, header=4)
        .pipe(rename_columns)
        .pipe(drop_empty_rows)
        .pipe(strip_prefixes)
        .pipe(strip_strings)
        .pipe(replace_absent_candidates)
    )

    # get version ids & make batch data
    batches_data = []

    for version_id_col in VERSION_ID_COLS:
        version_col_name = version_id_col.replace('_id', '')
        component_id = version_id_col[0].upper()

        # get version id
        if version_id_col != 'listening_version_id':
            version_id = df['paper_sat'] + component_id + df[version_col_name]
        else:
            version_id = component_id + df[version_col_name]
        df[version_id_col] = version_id

        # collect batches data
        for idx, row in df.iterrows():
            if pd.notna(row[version_id_col]):
                batches_data.append((row[version_id_col], component_id))
    
    # make batches df
    batches_df = pd.DataFrame(batches_data, columns=['version_id', 'component_id'])
    batches_df['errors'] = [[] for _ in range(len(batches_df))]
    batches_df = batches_df.dropna(subset=['version_id'])
    batches_df = batches_df.drop_duplicates(subset=['version_id'])
    batches_df = batches_df.sort_values(by=['version_id'], ascending=True)

    # get candidates dict
    candidates_df = df.copy()
    candidates_df['errors'] = [[] for _ in range(len(candidates_df))]
    candidates_list = candidates_df.to_dict(orient="records")
    
    # get batches dict
    batches_list = batches_df.to_dict(orient="records")

    return candidates_list, batches_list
    

def check_lists(centre_num: str, marking_window_id: int, candidates_list: CandidateDict, batches_list: BatchDict) -> Tuple[
    List[CandidateDict],
    List[BatchDict],
    List[ErrorMessage]
]:
    """Checks list against database, attaches error messages, remove certain elements"""
    versions_not_found = []
    errors_list = []
    # check version_id against database
    for batch in batches_list:
        version_id = batch.get('version_id', None)
        version_errors = validate_version(version_id)
        if version_errors:
            versions_not_found.append(version_id)
            errors_list.extend(version_errors)

    # check candidate numbers against database
    for position, candidate in enumerate(candidates_list):
        candidate_errors = validate_candidate(marking_window_id, centre_num, candidate, position)
        for version_id_col in VERSION_ID_COLS:
            if candidate[version_id_col] in versions_not_found:
                error = error_message(version_id_col, "This version could not be found on the database, please double check")
                candidate_errors.append(error)
            candidate.pop(version_id_col)
        candidate['errors'] = candidate_errors

    # cleans batch list of non-existent batches
    filtered_batches_list = [batch for batch in batches_list if not batch.get('errors')]

    # cleans candidate list of duplicates and adds to errors_list
    duplicate_count = sum(
        1
        for candidate in candidates_list
        for error in candidate.get('errors', [])
        if error.get('field') == "duplicate"
    )

    filtered_candidates_list = [
        candidate for candidate in candidates_list
        if not any(error.get('field') == 'duplicate' for error in candidate.get('errors', []))
        ]

    if duplicate_count > 0 and filtered_candidates_list:
        duplicate_error = error_message("candidates", f"We found {duplicate_count} duplicate candidates already on our database, so have removed these candidates")
        errors_list.append(duplicate_error)
    elif not filtered_candidates_list:
        duplicate_error = error_message("candidates", "These candidates have already been uploaded to us.")
        
    return filtered_candidates_list, filtered_batches_list, errors_list


# entry points
def process_register_file(centre_num: str, marking_window_id: int, file: BinaryIO) -> Tuple[
    List[CandidateDict],
    List[BatchDict],
    List[ErrorMessage]
]:
    """First pass process, processes Excel file returns JSON"""
    # convert to list of dicts
    candidates_list, batches_list = ingest_excel_file(file)
    
    # checks list of dicts and returns
    return check_lists(centre_num, marking_window_id, candidates_list, batches_list)