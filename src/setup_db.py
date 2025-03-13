from db import get_database_connection
import csv
import os

## NB probably replace this all with SQLalchemy eventually

def run_sql_file(cursor, filename):
    """Executes SQL command from a file."""
    with open(filename, "r") as file:
        queries = file.read().split(';')

    for sql in queries:
        if sql.strip():
            cursor.execute(sql)

def read_csv(csv_file_path):
    """Reads a CSV and returns a list of headers, and a list of tuples containing data"""

    with open(csv_file_path, "r", encoding='utf-8-sig') as file:
        reader = csv.reader(file)

        headers = next(reader)
        data = [tuple(row) for row in reader]

        return headers, data


def setup_database():
    """Sets up and seeds database"""
    conn = get_database_connection()
    cursor = conn.cursor()

    # creates schema
    # run_sql_file(cursor, "db/schema.sql")

    # adds data from csv files
    for root, _, files in os.walk(os.path.join("db", "data")):
        for file in files:
            tablename = os.path.splitext(file)[0]
            filepath = os.path.join(root, file)
            headers, data = read_csv(filepath)
            print(f"importing {len(headers)} columns and {len(data)} rows for table '{tablename}'")

            # USE DAO TO INSERT HERE
    
    # gets data from legacy database

    conn.commit()

    cursor.close()
    conn.close()


def seed_test_database():
    """Runs queries to input test data into database"""


if __name__ == "__main__":
    setup_database()
