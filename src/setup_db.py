from logger import logger
from db import get_legacy_database_connection, get_database_connection
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
    

def clean_centre_data(data):
    """Cleans centre data from legacy DB for SQL upload"""

    centre_data = []

    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item == '.':
                data[i][j] = None
        centre_data.append(row[:10])

    return centre_data

def clean_contact_data(data):
    """Prepares centre contact data from legacy DB for SQL upload"""

    contact_data = []

    filtered_data = [(row[0], *row[10:]) for row in data]
    for row in filtered_data:
        centre_id = row[0]

        # add primary and secondary contacts
        if row[1] and row[2]:
            name = row[1].strip().strip('\xa0')
            email = row[2].strip().strip('\xa0')
            contact_data.append(tuple([centre_id, name, email, True]))
        if row[3] and row[4]:
            name = row[3].strip().strip('\xa0')
            email = row[4].strip().strip('\xa0')
            contact_data.append(tuple([centre_id, name, email, False]))
    
    return contact_data


def setup_database():
    """Sets up and seeds database"""
    conn = get_database_connection()
    dao = DAO(conn)

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
    
    # gets centre data from legacy database
    # legacy_conn = get_legacy_database_connection()
    # legacy_dao = DAO(legacy_conn)
    # result = legacy_dao.run_sql_file("db/legacy_db_queries/select_centres.sql")
    # data = result.fetchall()

    # centre_data = clean_centre_data(data)
    # center_headers = ['centre_id', 'live_centre_number', 'centre_name', 'partner', 'address_1', 'address_2', 'address_3', 'address_4', 'address_5', 'country_id', 'phone_number']
    # dao.insert_many('centres', center_headers, centre_data)
    
    # contact_data = clean_contact_data(data)
    # contact_headers = ['centre_id', 'contact_name', 'contact_email', 'primary_contact']
    # dao.insert_many('centre_contacts', contact_headers, contact_data)

    # commit changes to db & close connection
    dao.close()


def seed_test_database():
    """Runs queries to input test data into database"""


if __name__ == "__main__":
    setup_database()
