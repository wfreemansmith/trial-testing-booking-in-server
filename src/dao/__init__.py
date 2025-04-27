from typing import List
from src.logger import logger

## NB probably replace this all with SQLalchemy eventually

class DAO():
    def __init__(self, conn):
        self.conn = conn
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def run_sql_file(self, filename):
        """Executes raw SQL command from a file"""
        with open(filename, "r") as file:
            queries = file.read().split(';')

        result = None

        for sql in queries:
            if sql.strip():
                command_str = sql.split("(")[0].strip()
                logger.info(f"Running query from file '{command_str}'")
                result = self.cursor.execute(sql)
        
        return result
                

    def select(self, tablename: str, select_columns: List[str] = None, where: List[tuple] = []):
        """Selects columns from given table. If no columns given return all.
        Search conditions presented as a list of tuples (x, y) where x = y"""

        columns = ', '.join(select_columns) if select_columns else "*"
        where_str = ""
        for i, item in enumerate(where):
            if i == 0:
                where_str += "WHERE "
            else:
                where_str += "\nAND "
            if isinstance(item[1], str):
                value = f"'{item[1]}'"
            else:
                value = f"{item[1]}"

            where_str += f"{item[0]} = {value}"

        sql = f"SELECT {columns} FROM {tablename} {where_str}"
        result = self.cursor.execute(sql)
        return result.fetchall()

    def insert(self, tablename: str, headers: List[str], data: tuple):
        """Inserts single entry into SQL database"""
        columns = ', '.join(headers)
        placeholders = ', '.join(['%s'] * len(headers))
        sql = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, data)

    def insert_many(self, tablename: str, headers: List[str], data: List[tuple]):
        """Inserts many into SQL database"""
        columns = ', '.join(headers)
        placeholders = ', '.join(['%s'] * len(headers))
        sql = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
        self.cursor.executemany(sql, data)
        logger.info(f"Inserting {len(data)} rows into '{tablename}'")


    def close(self):
        """Closes database connection"""
        self.cursor.close()
        self.conn.close()