from src.services.excel_register_processing import ingest_excel_file, check_lists
from src.services.file_handling import get_folder_name, get_file_name
from typing import List, BinaryIO, Dict
from src.db import get_database
from src.dao import UploadDAO, StagedFileDAO
from src.schemas.upload_schema import UploadData, BatchDict, CandidateDict
import urllib.parse


## NOTE: edit this, it may that as a controller we need to update what it returns

def preview(centre_id: str, marking_window_id: int, file: BinaryIO) -> Dict[str, List[dict]]:
    """First pass process, processes Excel file returns JSON"""
    # read Excelconvert to list of pydantic models
    parsed_candidates, parsed_batches = ingest_excel_file(file)
    
    # applies checks list and returns as list of dicts
    checked_candidates_list, checked_batches_list, error_list = check_lists(centre_id, marking_window_id, parsed_candidates, parsed_batches)
    
    # returns dict
    return {
        "candidates": checked_candidates_list,
        "batches": checked_batches_list,
        "errors": error_list
        }

def stage_file(centre_id: str, marking_window_id: int, batch: BatchDict, candidates: List[CandidateDict], temp_path: str):
    """Gets information from database for temporary file"""
    # construct file names
    component_dict = {'R': 'reading', 'W': 'writing', 'L': 'listening'}
    component = component_dict[batch.component_id]
    centre_folder_name = get_folder_name(centre_id=centre_id, marking_window_id=marking_window_id)
    destination_filename = get_file_name(centre_id=centre_id, batch=batch, candidates=candidates, component=component)
    destination_folder = urllib.parse.urljoin(centre_folder_name, component.capitalize())

    # add to staged table
    session = get_database()
    stage_dao = StagedFileDAO(session)
    stage_dao.stage_file(centre_id, marking_window_id, batch.version_id, destination_filename, destination_folder, temp_path)
    stage_dao.close()

    # returns dict
    return {
        "filename": destination_filename
    }

def check(data: UploadData, check_file_upload: bool = False) -> Dict[str, List[dict]]:
    """Checks user inputted data and returns updated data and list of errors"""
    checked_candidates_list, checked_batches_list, error_list = check_lists(
        centre_id=data.centre_id,
        marking_window_id=data.marking_window_id,
        candidates_list=data.candidates,
        batches_list=data.batches,
        test_date=data.test_date,
        check_file_upload=check_file_upload
        )

    return {
        "candidates": checked_candidates_list,
        "batches": checked_batches_list,
        "errors": error_list
        }

def submit(data: dict):
    """Submits data to database"""
    # additional step of checking that files have been uploaded - add to errors if not
    # check dict with check()
    # if results have any errors, return errors
    session = get_database()
    dao = UploadDAO(session)
    dao.insert_upload(data)