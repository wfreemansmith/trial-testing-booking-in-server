from src.config import FILE_UPLOAD_API_KEY
from src.db import get_db_session
from src.dao import CentreDAO, MarkingWindowDAO
from src.utils import construct_upload_path, construct_upload_filename, format_version_id, get_candidate_range
from src.schemas.upload_schema import BatchDict, CandidateDict
from typing import List
import files_sdk
import urllib.parse
from src.logger import logger

def get_folder_name(centre_id: str, marking_window_id: int) -> str:
    """Returns centre folder name for given centre, when only the centre_id and marking_window_id are known"""
    with get_db_session() as session:
        marking_window_dao = MarkingWindowDAO(session)
        centre_dao = CentreDAO(session)

        centre = centre_dao.select_one(centre_id=centre_id)
        marking_window = marking_window_dao.select_one(marking_window_id=marking_window_id)
    
        return construct_upload_path(marking_window.window_name, centre.partner, centre_id)


def get_file_name(centre_id: str, batch: BatchDict, candidates: List[CandidateDict], component: str) -> str:
    """Receives centre info and batch / candidate info in Pydantic format, returns appropriate file name"""
    component_key = f"{component}_version"
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
    return f"{centre_id}_{batch.version_id}_{candidate_range}_{number_of_candidates} candidates"


class FileHandler():
    def __init__(self):
        files_sdk.set_api_key(FILE_UPLOAD_API_KEY)

    # helper functions
    ## REWRITE so this accepts a file not a local path
    def upload_file(self, source_path: str, destination_folder: str, destination_filename: str) -> None:
        """Uploads a file to Files.com to given file path from temporary path"""
        destination_path = urllib.parse.urljoin(destination_folder, destination_filename)

        try:
            files_sdk.upload_file(source_path, destination_path, params={"mkdir_parents": True})
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            # handle an exception, raise here