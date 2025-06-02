import sqlite3

class DatabaseManager:

    def __init__(self, db_name="Icarus.db"):
        self.db_name = db_name

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_name)
            print(f"Connected to {self.db_name}.")
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close(self, conn):
        if conn:
            try:
                conn.commit()
                print("Transaction committed.")
            except sqlite3.Error as e:
                print(f"Error committing transaction: {e}")
                try:
                    conn.rollback()
                    print("Transaction rolled back.")
                except sqlite3.Error as e:
                    print(f"Error rollback transaction: {e}")
            finally:
                try:
                    conn.close()
                    print(f"Connection to database {self.db_name} closed.")
                except sqlite3.Error as e:
                    print(f"Error closing connection to database {self.db_name}: {e}")



