from src.db import get_database
from src.utils import serialise_pydantic_list
from src.errors import FileProcessingError
from typing import TypedDict, BinaryIO, List, Tuple
from src.schemas.upload_schema import CandidateDict, ErrorMessage, BatchDict
from io import BytesIO
from src.dao import CandidateDAO, VersionDAO
import pandas as pd
import numpy as np
from pandas import DataFrame


# create database connection
engine = get_database()
version_dao = VersionDAO(engine)
candidate_dao = CandidateDAO(engine)


# constants
VERSION_ID_COLS = ['reading_version_id', 'writing_version_id', 'listening_version_id']


def validate_candidate(marking_window_id: int, centre_num: str, candidate: CandidateDict, position: int) -> List[ErrorMessage]:
    """Checks candidate dict against database, adjusts anything which can be adjusted, returns error messages if any error"""
    candidate_errors = []

    # check for blanks etc
    if not candidate.candidate_name:
        candidate.errors.append(
            ErrorMessage(field="candidate_name", message="Candidate name cannot be blank. Please provide a name for the candidate.")
        )
    
    if not candidate.candidate_number:
        candidate.errors.append(
            ErrorMessage(field="candidate_number", message="Candidate number cannot be blank or zero. Please provide a candidate number that you have not used previously.")
        )

    # check database here
    duplicate = candidate_dao.is_duplicate_candidate(marking_window_id, centre_num, candidate.candidate_name, candidate.candidate_number)
    if duplicate and type(duplicate) is int:
        candidate['candidate_number'] = duplicate + position
        error = ErrorMessage(field="candidate_number", message="Candidate number was already found in our records. We have updated duplicate candidate numbers on your register. Please amend your test materials before scanning and uploading to reflect these changes.")
        candidate_errors.append(error)
    elif duplicate:
        error = ErrorMessage(field="duplicate")
        candidate_errors.append(error)

    return candidate_errors


def validate_version(version_id: str) -> List[ErrorMessage]:
    """Checks version id on database, logs it as problematic, and returns an error if any are found"""
    version_errors = []
    version_exists = version_dao.version_exists(version_id)
    if not version_exists:
        error = ErrorMessage(field="version_id", message=f"Version cannot be found on the database. Please check the version, update your candidates, and try again. If you believe this is an error, please contact Cambridge.")
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
    version_columns = df.columns[3:]
    PREFIXES = ['ACW', 'ACR', 'GTR', 'GTW', 'List', 'LIST', 'L']
    for prefix in PREFIXES:
        df[version_columns] = df[version_columns].apply(
            lambda x: x.str.replace(prefix,'')
        )
    return df

def strip_strings(df: DataFrame) -> DataFrame:
    string_columns = df.columns[1:]
    df[string_columns] = df[string_columns].apply(lambda x: x.str.strip())
    return df

def replace_nans(df: DataFrame) -> DataFrame:
    df = df.replace({np.nan: None})
    return df

def replace_absent_candidates(df: DataFrame) -> DataFrame:
    version_columns = df.columns[3:]
    ABSENT_KEYWORDS = ["ABSENT", "ABS", "-", ""]
    df[version_columns] = df[version_columns].replace(ABSENT_KEYWORDS, None)
    return df

def construct_version_ids(df: DataFrame) -> DataFrame:
    version_columns = df.columns[3:]
    for version_col in version_columns:
        version_id_col = f"{version_col}_id"
        component_id = version_id_col[0].upper()

        if version_col == 'listening_version':
            version_id = component_id + df[version_col]
        else:
            version_id = df['paper_sat'] + component_id + df[version_col]
        df[version_id_col] = version_id
    return df


# main functions
def ingest_excel_file(file: BinaryIO) -> Tuple[
    List[CandidateDict],
    List[BatchDict]
    ]:
    """Processes Excel file and returns two lists of validated pydantic candidates and batches"""
    # Suppress specific openpyxl UserWarnings
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, message="Data Validation extension is not supported and will be removed")

    try:
        df = (
            pd.read_excel(BytesIO(file), header=4)
            .pipe(rename_columns)
            .pipe(drop_empty_rows)
            .pipe(strip_prefixes)
            .pipe(strip_strings)
            .pipe(replace_absent_candidates)
            .pipe(construct_version_ids)
            .pipe(replace_nans)
        )
    except KeyError as e:
        raise FileProcessingError(str(e.args[0]))

    # construct list of candidate and batch dicts
    candidates_df = df.copy()
    candidates_df['errors'] = [[] for _ in range(len(candidates_df))]
    candidates_list = candidates_df.to_dict(orient="records")
    parsed_candidates = [CandidateDict.model_validate(row) for row in candidates_list]
    
    seen_versions = set()
    parsed_batches = []

    for _, row in df.iterrows():
        for version_id_col in VERSION_ID_COLS:
            version_id = row[version_id_col]

            if version_id not in seen_versions and pd.notna(version_id):
                parsed_batches.append(
                    BatchDict(
                        version_id=version_id,
                        component_id=version_id_col[0].upper()
                    )
                )
                seen_versions.add(version_id)

    # sorts batch_list
    parsed_batches.sort(key=lambda batch: batch.version_id)

    return parsed_candidates, parsed_batches


def parse_lists(candidates_list: List[dict], batches_list: List[dict]) -> Tuple[
        List[CandidateDict],
        List[BatchDict]
]:
    """Converts a list of candidate and batch dicts into validated pydantic lists"""
    parsed_candidates = [CandidateDict.model_validate(row) for row in candidates_list]
    parsed_batches = [BatchDict.model_validate(row) for row in batches_list]
    return parsed_candidates, parsed_batches
  

def check_lists(centre_id: str, marking_window_id: int, candidates_list: List[CandidateDict], batches_list: List[BatchDict]) -> Tuple[
    List[dict],
    List[dict],
    List[dict]
]:
    """
    Accepts a list of pydantic candidates and batches, returns a list of cleanded dicts.
    Checks lists against database, attaches any relevant error messages, remove duplicates and unnecesarry fields
    """
    versions_not_found = set()
    errors_list = []
    # check version_id against database
    for batch in batches_list:
        version_errors = validate_version(batch.version_id)
        if version_errors:
            versions_not_found.add(batch.version_id)
            errors_list.extend(version_errors)

    # check candidate numbers against database
    for position, candidate in enumerate(candidates_list):
        validate_candidate(marking_window_id, centre_id, candidate, position)
        for version_id_col in VERSION_ID_COLS:
            if getattr(candidate, version_id_col) in versions_not_found:
                candidate.errors.append(
                    ErrorMessage(field=version_id_col, message="This version could not be found on the database, please double check")
                )

    # cleans batch list of non-existent batches
    filtered_batches_list = [batch for batch in batches_list if not batch.errors]

    # cleans candidate list of duplicates and adds to errors_list
    duplicate_count = sum(
        1
        for candidate in candidates_list
        for error in candidate.errors
        if error.field == "duplicate"
    )

    filtered_candidates_list = [
        candidate for candidate in candidates_list
        if not any(error.field == 'duplicate' for error in candidate.errors)
        ]

    if duplicate_count > 0 and filtered_candidates_list:
        errors_list.append(
            ErrorMessage(field="candidates", message=f"We found {duplicate_count} duplicate candidates already on our database, so have removed these candidates")
        )
    elif not filtered_candidates_list:
        errors_list.append(
            ErrorMessage(field="candidates", message="These candidates have already been uploaded to us.")
        )

    checked_candidate_list = serialise_pydantic_list(filtered_candidates_list)
    for cand in checked_candidate_list:
        for version_id in VERSION_ID_COLS:
            cand.pop(version_id)
    checked_batches_list = serialise_pydantic_list(filtered_batches_list)
    checked_errors_list = serialise_pydantic_list(errors_list)
        
    return checked_candidate_list, checked_batches_list, checked_errors_list