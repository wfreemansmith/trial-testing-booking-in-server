import uvicorn
from src.app import create_app
from src.config import SERVER_PORT

app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=SERVER_PORT, reload=True)