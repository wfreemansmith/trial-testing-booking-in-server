from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

async def http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "status": "error",
            "message": e.detail,
            "code": e.status_code
        }
    )

async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "code": 500
            }
        )