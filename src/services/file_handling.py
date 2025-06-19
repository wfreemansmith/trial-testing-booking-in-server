from src.config import FILE_UPLOAD_API_KEY
from src.db import get_database
from src.dao import CentreDAO, MarkingWindowDAO
from src.utils import construct_upload_path, construct_upload_filename, format_version_id, get_candidate_range
from src.schemas.upload_schema import BatchDict, CandidateDict
from typing import List
import files_sdk

def get_folder_name(centre_id: str, marking_window_id: int) -> str:
    """Returns centre folder name for given centre"""
    session = get_database()
    marking_window_dao = MarkingWindowDAO(session)
    centre_dao = CentreDAO(session)

    centre = centre_dao.select_one(centre_id=centre_id)
    marking_window = marking_window_dao.select_one(marking_window_id=marking_window_id)
    centre_dao.close()
    marking_window_dao.close()
    return construct_upload_path(marking_window.window_name, centre.partner, centre_id)


def get_file_name(centre_id: str, batch: BatchDict, candidates: List[CandidateDict]) -> str:
    """Returns file name"""
    component_dict = {
        'R': 'reading_version',
        'W': 'writing_version',
        'L': 'listening_version'
    }
    component_key = component_dict[batch.component_id]
    filtered_candidate_list = [
        candidate for candidate in candidates
        if batch.version_id == format_version_id(
            candidate.paper_sat,
            batch.component_id,
            getattr(candidate, component_key)
        )
    ]
    number_of_candidates = len(filtered_candidate_list)
    candidate_range = get_candidate_range([candidate.candidate_number for candidate in filtered_candidate_list])
    return f"{centre_id}_{batch.version_id}_{candidate_range}_{number_of_candidates}"

class FileHandler():
    def __init__(self):
        files_sdk.set_api_key(FILE_UPLOAD_API_KEY)

    # helper functions
    ## REWRITE so this accepts a file not a local path
    def upload_file(self, local_path: str, destination: str) -> None:
        """Uploads a file to Files.com to given file path"""
        try:
            files_sdk.upload_file(local_path, destination)
        except Exception as e:
            print(f"Error uploading file: {e}")
            # handle an exception, raise here