import os
import sqlite3


class Database:
    """
    Database:
        - First Iteration using a sqlite connection to the database
        - Second Iteration using Connection Pooling if we still got time. 
    """
    def __init__(self, path: str):
        self.path = path
        self.scheme = """
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
        """

    def initialize_database(self):
        if not os.path.exists(self.path):
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            cursor.execute(self.scheme)
            conn.commit()
            conn.close()
