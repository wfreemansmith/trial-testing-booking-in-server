from src.config import SQL_DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, LEGACY_DB_HOST, LEGACY_DB_NAME, USERDOMAIN, USERNAME
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from src.logger import logger

DB_STRING = f"{SQL_DB}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    """Returns an SQL alchemy database engine and session"""
    return SessionLocal()
    

def get_db():
    """Yields an SQL alchemy database engine and session, close and rollback"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"{e}")
        logger.info("Rolling back current session...")
        session.rollback()
    finally:
        session.close()


@contextmanager
def get_db_session():
    """Context manager for database sessions, ensuring proper closure and cleanup"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"{e}")
        logger.info("Rolling back current session...")
        session.rollback()
    finally:
        session.close()


def get_legacy_database_connection():
    """Returns connection object to legacy SQL Server database"""
    connection = pyodbc.connect(
        driver = "{ODBC Driver 11 for SQL Server}",
        host = LEGACY_DB_HOST,
        database = LEGACY_DB_NAME,
        user = f"{USERDOMAIN}\\{USERNAME}",
        Trusted_Connection="yes"
    )

    return connection