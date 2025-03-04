import sqlite3

# note replace this with logic from a config file depending on if prod or dev
DB = "db/test.db"


def run_sql_file(cursor, filename):
    """Executes SQL command from a file."""
    with open(filename, "r") as file:
        sql = file.read()
    cursor.executescript(sql)
    

def setup_database():
    """Sets up and seeds database"""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    run_sql_file(cursor, "db/schema.sql")
    # now run seed data


if __name__ == "__main__":
    setup_database()
