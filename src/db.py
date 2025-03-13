from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
import psycopg2


def get_database_connection():
    """Returns connection object to database"""
    DB_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    connection = psycopg2.connect(DB_STRING)

    return connection
