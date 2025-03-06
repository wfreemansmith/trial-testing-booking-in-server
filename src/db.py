from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import pyodbc


def get_database_connection():
    """Returns connection object to database"""
    connection = pyodbc.connect(
        driver = "{ODBC Driver 11 for SQL Server}",
        host = DB_NAME,
        database = DB_NAME,
        user = f"{USERDOMAIN}\\{USERNAME}",
        Trusted_Connection="yes"
        )

    return connection
