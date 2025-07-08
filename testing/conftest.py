import sys
import os
from src.config import STAGING_DIR

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.setup_db import setup_database, reset_database
from src.db import engine, get_db_session
from src.main import app

@pytest.fixture
def db_session():
    """Sets up and tears down test db data"""
    with get_db_session() as session:
        reset_database(engine)
        setup_database(session)

        session.flush()

        yield session  


@pytest.fixture
def cleanup_tmp_files():
    def cleanup():
        for filename in os.listdir(STAGING_DIR):
            file_path = os.path.join(STAGING_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    cleanup()
    yield
    cleanup()

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac