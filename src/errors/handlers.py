from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.errors.custom_expeptions import FileProcessingError

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

async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": str(exc),
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )