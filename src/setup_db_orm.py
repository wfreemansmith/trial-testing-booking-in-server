from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData, text
from src.logger import logger
from src.db import get_database
from src.models import Base, get_model_by_tablename
import csv
import os


def reset_database(engine):
    """Drops all tables and recreates them"""
    # get all existing tables in database
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # drop all tables
    logger.info("Dropping tables...")
    with engine.begin() as conn:
        for table in reversed(metadata.sorted_tables):
            logger.debug(f"Dropping {table.name}")
            conn.execute(text(f"DROP TABLE IF EXISTS {table.name} CASCADE;"))

    # create all tables
    logger.info('Creating database tables...')
    Base.metadata.create_all(engine)


def seed_data_from_csv(session: Session, tablename: str, csv_filepath: str):
    """Seeds data from a given CSV file to a given table"""
    Model = get_model_by_tablename(tablename)

    if Model:
        with open(csv_filepath, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            data = [Model(**row) for row in reader]
        logger.debug(f"Inserting {len(data)} entries into table '{tablename}'")
        session.add_all(data)
        session.commit()
    else:
        logger.error(f"Cannot find a table by the name '{tablename}' in ORM.")


def setup_database(session: Session):
    """Sets up and seeds database"""
    
    # iterates through all data and inputs
    for root, _, files in os.walk(os.path.join("db", "data")):
        for file in files:
            tablename = os.path.splitext(file)[0].split('.')[1]
            csv_filepath = os.path.join(root, file)
            seed_data_from_csv(
                session=session,
                tablename=tablename,
                csv_filepath=csv_filepath
                )


if __name__ == "__main__":
    engine = get_database()
    new_session = sessionmaker(bind=engine)
    session = new_session()

    reset_database(engine)
    setup_database(session)