from fastapi import APIRouter, UploadFile, Form, File, Body, HTTPException, status
from src.controllers import upload_controller
from src.utils import api_response
from src.schemas.upload_schema import parse_preview_data, parse_upload_data, parse_uploadfile_data, UploadPayload
import json, os, uuid, shutil, tempfile
from src.config import STAGING_DIR
from src.logger import logger

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
    parsed_data = parse_preview_data(json.loads(data))

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
def refresh_data(payload: UploadPayload):
    """Validate user inputted data and returns any error flags"""
    token = payload.token
    data = payload.data
    parsed_data = parse_upload_data(data)
    return upload_controller.check(parsed_data)


@router.post("/file_upload")
@api_response()
async def file_upload(
    token: str = Form(...),
    data: str = Form(...),
    file: UploadFile = File(...)):
    """Upload scanned materials to staging directory for later upload to files.com"""
    parsed_data = parse_uploadfile_data(json.loads(data))

    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type .{file.filename.split(".")[-1]} not supported"
        )
    
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_path = os.path.join(STAGING_DIR, temp_filename)

    file.file.seek(0)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return upload_controller.stage_file(
        centre_id=parsed_data.centre_id,
        marking_window_id=parsed_data.marking_window_id,
        batch=parsed_data.batch,
        candidates=parsed_data.candidates,
        temp_path=temp_path
    )


@router.post("/submit")
@api_response()
def submit_upload(payload: UploadPayload):
    """Checks all data and uploads, and if no errors commits to database"""
    ## STEPS
    # check that a file has been uploaded for each batch
    # check that the data is correct
    token = payload.token
    data = payload.data
    parsed_data = parse_upload_data(data)
    checked_data = upload_controller.check(parsed_data, check_file_upload=True)

    if checked_data['errors']:
        return checked_data
    else:
        upload_controller.submit(data)