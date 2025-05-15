from fastapi import APIRouter, UploadFile, Form, File, Body
from src.controllers import upload_controller
from src.utils.response import api_response
import json

router = APIRouter()


@router.get("/")
@api_response()
def get_context(token: str):
    """Once users first login to the page retrieves basic information about their centre"""
    print("put logic in here for getting the main info with a token")


@router.post("/preview")
@api_response()
def preview_upload(
    token: str = Form(...),
    data: str = Form(...),
    file: UploadFile = File(...)
    ):
    """Process register and return data contained within"""
    data_dict = json.loads(data)
    centre_id = data_dict.get('centre_id')
    marking_window_id = data_dict.get('marking_window_id')
    return upload_controller.preview(centre_id, marking_window_id, file)


@router.post("/refresh")
@api_response()
def refresh_data(token: str, data: dict = Body(...)):
    """Validate user inputted data and returns any error flags"""
    return upload_controller.check(data)


@router.post("/file_upload")
@api_response()
def file_upload(token: str, data: dict, file: UploadFile):
    """Upload scanned materials to files.com"""
    print("")


@router.post("/submit")
@api_response()
def submit_upload(token: str, data: dict):
    """Checks all data and uploads, and if no errors commits to database"""
    ## STEPS
    # check that a file has been uploaded for each batch
    # check that the data is correct
    checked_data = upload_controller.check(data)
    if checked_data['errors']:
        return checked_data
    else:
        upload_controller.submit(data)