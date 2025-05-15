from src.services import ingest_excel_file, check_lists
from typing import List, BinaryIO, Dict
from src.db import get_database
from src.dao import UploadDAO

## NOTE: edit this, it may that as a controller we need to update what it returns

def preview(centre_id: str, marking_window_id: int, file: BinaryIO) -> Dict[str, List[dict]]:
    """First pass process, processes Excel file returns JSON"""
    # convert to list of dicts
    candidates_list, batches_list = ingest_excel_file(file)
    
    # checks list of dicts and returns
    checked_candidates_list, checked_batches_list, error_list = check_lists(centre_id, marking_window_id, candidates_list, batches_list)
    
    # returns dict
    return {
        "candidates": checked_candidates_list,
        "batches": checked_batches_list,
        "errors": error_list
        }

def check(data: dict) -> Dict[str, List[dict]]:
    """Checks user inputted data and returns updated data and list of errors"""
    ## ALSO CHECK OTHER DATA besides Candidates and Batch
    centre_id = data.get("centre_id", None)
    marking_window_id = data.get("marking_window_id", None)
    candidates_list = data.get("candidates", [])
    batches_list = data.get("batches", [])

    checked_candidates_list, checked_batches_list, error_list = check_lists(centre_id, marking_window_id, candidates_list, batches_list)
    
    return {
        "candidates": checked_candidates_list,
        "batches": checked_batches_list,
        "errors": error_list
        }

def submit(data: dict):
    """Submits data to database"""
    #does some data uploading and stuff
    engine = get_database()
    dao = UploadDAO(engine)
    dao.insert_upload(data)