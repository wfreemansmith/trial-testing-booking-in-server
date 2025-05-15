from functools import wraps
from fastapi.responses import JSONResponse
from fastapi import HTTPException

def api_response(success_message = "Request successful"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs) if callable(getattr(func, '__await__', None)) else func(*args, **kwargs)
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "data": result,
                        "message": success_message
                    }
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "message": str(e),
                        "code": 500
                })
        return wrapper
    return decorator