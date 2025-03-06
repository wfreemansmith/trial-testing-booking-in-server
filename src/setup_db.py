from db import get_database_connection


def run_sql_file(cursor, filename):
    """Executes SQL command from a file."""
    with open(filename, "r") as file:
        sql = file.read()
    cursor.executescript(sql)
    

def setup_database():
    """Sets up and seeds database"""
    conn = get_database_connection()
    cursor = conn.cursor()

    # creates schema
    run_sql_file(cursor, "db/schema.sql")
    # now run seed data


if __name__ == "__main__":
    setup_database()
