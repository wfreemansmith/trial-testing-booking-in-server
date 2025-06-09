import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import clear_mappers
from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker
from src.setup_db import setup_database, reset_database
from src.db import DB_STRING, get_database, engine
from src.main import app

@pytest.fixture
def db_session():
    """Sets up and tears down test db data"""

    session = get_database()

    # Drop and recreate tables
    reset_database(engine)
    setup_database(session)
    session.flush()

    yield session

    session.close()


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac