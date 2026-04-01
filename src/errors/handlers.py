from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from src.errors.custom_expeptions import FileProcessingError, UnprocessableEntity, StagedFileNotFound

async def http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "status": "error",
            "message": e.detail,
            "code": e.status_code
        }
    )

async def file_processing_error_handler(request: Request, e: FileProcessingError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": "There was an error processing the file you uploaded. Please check that you have used the correct template and it has not been altered.",
            "code": status.HTTP_400_BAD_REQUEST
            }
        )

async def validation_error_handler(request: Request, e: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": e.errors(),
            "code": status.HTTP_400_BAD_REQUEST
            }
        )    

async def unprocessable_error_handler(request: Request, e: UnprocessableEntity):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "data": e.data,
            "message": e.message,
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY
            }
        )

async def staged_file_not_found_handler(request: Request, exc: StagedFileNotFound):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": str(exc) if str(exc) else f"{str(exc)} Please contact support.",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": str(exc),
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )
