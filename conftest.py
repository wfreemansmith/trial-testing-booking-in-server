import pytest
from sqlalchemy.orm import sessionmaker
from src.setup_db_orm import setup_database, reset_database
from src.db import get_database

@pytest.fixture
def db_session():
    """Sets up and tears down test db data"""
    engine = get_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    reset_database(engine)
    setup_database(session)

    yield engine

    session.close()

