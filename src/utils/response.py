from functools import wraps
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import inspect

def api_response(success_message = "Request successful"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "data": result,
                        "message": success_message
                    }
                )
            except Exception as e:
                raise e
        return wrapper
    return decorator