from src.db import get_database
from typing import TypedDict, BinaryIO, List
import pandas as pd
import json

class CandidateDict(TypedDict):
    candidate_number: int
    candidate_name: str
    paper_sat: str
    writing_version: str
    reading_version: str
    listening_version: str
    errors: list

class BatchDict(TypedDict):
    version_id: str
    component_id: str
    errors: list

# read file
# check candidate details are complete
# check candidate numbers are not already in database
## flag errors if numbers are repeated, if number & candidate are repeated do not proceed
# check versions are in the database
# format dataframe as a dict


def append_error():
    """Appends an error to relevant array in dataframe, indicating which row and field is problematic"""


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

    # get candidates dict
    candidates_df = df.copy()
    candidates_df['errors'] = [[] for _ in range(len(candidates_df))]
    candidates_list = candidates_df.to_dict(orient="records")
    
    # get version ids & make batch data
    batches_data = []

    for version_id in ['reading_version_id', 'writing_version_id', 'listening_version_id']:
        version_col_name = version_id.replace('_id', '')
        component_id = version_id[0].upper()

        # get version id
        if version_id != 'listening_version_id':
            df[version_id] = df['paper_sat'] + component_id + df[version_col_name]
        else:
            df[version_id] = component_id + df[version_col_name]

        # collect batches data
        for idx, row in df.iterrows():
            if pd.notna(row[version_id]):
                batches_data.append((row[version_id], component_id))
    
    # make batches df
    batches_df = pd.DataFrame(batches_data, columns=['version_id', 'component_id'])
    batches_df = batches_df.dropna(subset=['version_id'])
    batches_df = batches_df.drop_duplicates(subset=['version_id'])
    batches_df = batches_df.sort_values(by=['version_id'], ascending=True)

    # Start doing checks against the database here
    engine = get_database()

    # check candidate numbers against database
    ## DO THIS HERE

    # check versions against database
    ## version_dao = Version()
    for version_id in batches_df['version_id']:
        print(version_id)
        # version_exists = version_dao.version_exists(version_id)
        # if not version_exists:
        #   append_error()

    # get batches dict
    batches_df['errors'] = [[] for _ in range(len(batches_df))]
    batches_list = batches_df.to_dict(orient="records")

    return candidates_list, batches_list
