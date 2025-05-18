from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from src.routes import upload_router
from src.errors import http_exception_handler, server_error_handler

def create_app() -> FastAPI:
    app = FastAPI()

    # add middleware
    
    # add routes
    @app.get("/")
    async def hello():
        return {"message": "hello"}
    app.include_router(upload_router, prefix="/upload")

    # add handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, server_error_handler)

    return app