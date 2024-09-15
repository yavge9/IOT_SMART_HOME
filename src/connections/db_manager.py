import sqlite3
from src.settings import *
import random
from datetime import datetime
from typing import Tuple, Any

r = random.randrange(1, 100000)
clientname = "IOT_client-Id-" + str(r)

class DbManager():
    def __init__(self, db_name: str, params: str):
        # Add 'timestamp' to the schema
        self.db_name = db_name
        self.db_path = db_path
        self.params = params + ', timestamp TEXT'
        self.init_db()

    def init_db(self) -> None:
        """Initializes the database with the provided table and parameters."""
        conn = sqlite3.connect(self.db_path)
        try:
            print("starting db init for: ", self.db_name)
            command = f"CREATE TABLE IF NOT EXISTS {self.db_name} ({self.params})"
            cursor = conn.cursor()
            cursor.execute(command)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing the database: {e}")
        finally:
            cursor.close()

    def insert_data(self, data: Tuple[Any]) -> None:
        """Inserts data into the table with an automatic timestamp."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            placeholders = ', '.join(['?'] * (len(data) + 1))  # Add one for the timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Generate timestamp
            cursor.execute(f"INSERT INTO {self.db_name} VALUES ({placeholders})", (*data, timestamp))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
        finally:
            if cursor:  # Only close if cursor is initialized
                cursor.close()