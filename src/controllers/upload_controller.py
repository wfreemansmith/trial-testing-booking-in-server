from src.services.excel_register_processing import ingest_excel_file, check_lists, CandidateDict, BatchDict, ErrorMessage
from typing import List, Tuple, BinaryIO

## NOTE: edit this, it may that as a controller we need to update what it returns

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