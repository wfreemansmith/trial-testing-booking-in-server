from src.services.excel_register_processing import ingest_excel_file, check_lists
from typing import List, BinaryIO, Dict
from src.db import get_database
from src.dao import UploadDAO
from src.schemas.upload_schema import UploadData


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