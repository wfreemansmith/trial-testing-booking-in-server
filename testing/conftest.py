import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import sessionmaker
from src.setup_db_orm import setup_database, reset_database
from src.db import get_database
from src.main import app

@pytest.fixture
def setup_teardown():
    """Sets up and tears down test db data"""
    engine = get_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    reset_database(engine)
    setup_database(session)

    yield engine

    session.close()


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac