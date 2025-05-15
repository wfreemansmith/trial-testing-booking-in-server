from fastapi import APIRouter, UploadFile
from src.controllers.upload_controller import process_register_file

router = APIRouter()


@router.get("/upload")
def get_context(token: str):
    print("put logic in here for getting the main info")


@router.post("/upload/preview")
def preview_upload(token: str, data: dict, file: UploadFile):
    """Process register and return data contained within"""
    print("")


@router.post("/upload/refresh")
def refresh_upload(token: str, data: dict):
    """Validate user inputted data"""
    # check centre details
    # run check lists
    print("")


@router.post("/upload/file_upload")
def file_upload(token: str, data: dict, file: UploadFile):
    """Upload scanned materials to files.com"""
    print("")


@router.post("/upload/submit")
def submit_upload(token: str, data: dict):
    print("")