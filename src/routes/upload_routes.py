from fastapi import APIRouter, UploadFile, Form, File, Body, HTTPException, status
from pydantic import ValidationError
from src.controllers import upload_controller
from src.utils import api_response
from src.schemas.upload_schema import parse_preview_data
import json

router = APIRouter()


@router.get("/")
@api_response()
def get_context(token: str):
    """Once users first login to the page retrieves basic information about their centre"""
    print("put logic in here for getting the main info with a token")


@router.post("/preview")
@api_response()
async def preview_upload(
    token: str = Form(...),
    data: str = Form(...),
    file: UploadFile = File(...)
    ):
    """Process register and return data contained within"""
    try:
        parsed_data = parse_preview_data(json.loads(data))
    except ValidationError as e:
        ## maybe pass Validation Errors to a specific handler?
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors()
        )

    if file.filename.endswith('.xlsx'):
        file_bytes = await file.read()
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type .{file.filename.split(".")[-1]} not supported"
        )

    return upload_controller.preview(parsed_data.centre_id, parsed_data.marking_window_id, file_bytes)


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