from src.services.excel_register_processing import ingest_excel_file, check_lists
from src.services.file_handling import get_folder_name, get_file_name
from typing import List, BinaryIO, Dict
from src.db import get_db_session
from src.dao import UploadDAO, StagedFileDAO
from src.schemas.upload_schema import UploadData, BatchDict, CandidateDict
from src.errors import StagedFileNotFound
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
    destination_filename = f"{get_file_name(centre_id=centre_id, batch=batch, candidates=candidates, component=component)}.pdf"
    destination_folder = urllib.parse.urljoin(centre_folder_name, component.capitalize())

    # add to staged table
    with get_db_session() as session:
        dao = StagedFileDAO(session)
        dao.stage_file(centre_id, marking_window_id, batch.version_id, destination_filename, destination_folder, temp_path)

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
    """Submits data to database and uploads file"""
    # additional step of checking that files have been uploaded - add to errors if not
    # asyncronous operation - get the file from the server and upload, then delete the file
    from src.services.file_handling import FileHandler
    from logger import logger
    import os

    with get_db_session() as session:
        staged_dao = StagedFileDAO(session)
        file_handler = FileHandler()

        # retrieves stored files from server, uploads, rollback if not achieved atomically 
        successful_uploads = []

        for batch in data['batches']:
            try:
                staged = staged_dao.retrieve_file(
                    centre_id=data['centre_id'],
                    marking_window_id=data['marking_window_id'],
                    version_id=batch['version_id']
                    )
                
                if not staged:
                    raise StagedFileNotFound("No record of the file was found on the database.")
                
                if not os.path.exists(staged.temp_path):
                    raise StagedFileNotFound("A file could not be found while attempting to upload.")
                
                
                file_handler.upload_file(
                    source_path=staged.temp_path,
                    destination_filename=staged.destination_filename,
                    destination_folder=staged.destination_folder)
                
                successful_uploads.append(staged)
                batch.setdefault('file_uploads', []).append({'file_name': staged.destination_filename})
            except Exception as e:
                logger.error(f"Upload failed, attempt rollback of {len(successful_uploads)} files")
                for staged in successful_uploads:
                    file_handler.delete_file(staged.destination_folder, staged.destination_filename)
                raise

        # deletes temp files only on successful upload of all files
        for staged in successful_uploads:
            if os.path.exists(staged.temp_path):
                os.remove(staged.temp_path)

        # finally enters record on db
        upload_dao = UploadDAO(session)
        upload_dao.insert_upload(data)