from logger import logger
from db import get_legacy_database_connection
from dao import DAO
import csv
import os


def read_csv(csv_file_path):
    """Reads a CSV and returns a list of headers, and a list of tuples containing data"""

    with open(csv_file_path, "r", encoding='utf-8-sig') as file:
        reader = csv.reader(file)

        headers = next(reader)
        data = [tuple(row) for row in reader]

        return headers, data


def setup_database():
    """Sets up and seeds database"""
    dao = DAO()

    # creates schema
    dao.run_sql_file("db/schema.sql")

    # adds data from csv files
    for root, _, files in os.walk(os.path.join("db", "data")):
        for file in files:
            tablename = os.path.splitext(file)[0].split('.')[1]
            filepath = os.path.join(root, file)
            headers, data = read_csv(filepath)
            logger.info(f"importing {len(headers)} columns and {len(data)} rows for table '{tablename}'")

            dao.insert_many(tablename, headers, data)
    
    # gets data from legacy database
    legacy_conn = get_legacy_database_connection()
    legacy_cursor = legacy_conn.cursor()

    run_sql_file(legacy_cursor, "db/legacy_db_queries/select_centres.sql")
    # centre_rows = legacy_cursor.fetchall()

    # USE DAO TO INSERT HERE

    # commit changes to db & close connection
    dao.close()


def seed_test_database():
    """Runs queries to input test data into database"""


if __name__ == "__main__":
    setup_database()
