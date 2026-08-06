import pymysql
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'attendance_db')
        self.port = int(os.getenv('DB_PORT', 3306))
    
    @contextmanager
    def get_connection(self):
       conn = pymysql.connect(
    host=self.host,
    user=self.user,
    password=self.password,
    database=self.database,
    port=self.port,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    ssl={"ssl": {}}
    )
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchone() if fetch_one else cursor.fetchall()
                else:
                    conn.commit()
                    # Return last insert ID for INSERT statements
                    if query.strip().upper().startswith('INSERT'):
                        return cursor.lastrowid
                    return cursor.rowcount
    
    def execute_many(self, query: str, data: list):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, data)
                conn.commit()
                return cursor.rowcount

db = Database()
