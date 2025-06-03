import pandas as pd
import sqlite3

class AirportDAO:

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self):
        conn = self.db_manager.connect()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Airports (
                        Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        AirportCode TEXT NOT NULL UNIQUE,        
                        AirportName TEXT NOT NULL,               
                        AirportCountry TEXT NOT NULL,            
                        Runways INTEGER NOT NULL                 
                    )
                """)
                conn.commit()
                print("Aiport table created successfully")
            except Exception as e:
                print(f"Failed to create Aiport table: {e}")
                self.db_manager.rollback(conn)
            finally:
                self.db_manager.close(conn)



    def insert_data(self):
        try:
            df = pd.read_csv("Airports.csv")
        except Exception as e:
            print(f"Failed to read Airports.csv: {e}")
            return

        conn = self.db_manager.connect()
        if conn:
            try:
                cursor = conn.cursor()
                for index, row in df.iterrows():
                    airport_code = row["AirportCode"].strip()
                    airport_name = row["AirportName"].strip()
                    airport_country = row["AirportCountry"].strip()
                    runways = int(row["Runways"])

                    cursor.execute("""
                    INSERT INTO Airports (AirportCode, AirportName, AirportCountry, Runways)
                    VALUES (?, ?, ?, ?) 
                    """, (airport_code, airport_name, airport_country, runways))
                    print(f"Inserted Airport: {airport_code}, {airport_name}")
                conn.commit()
                print("All airports inserted successfully")
            except (sqlite3.Error, KeyError, ValueError) as e:
                print(f"Failed to insert Airport: {e}. Rolling back.")
                self.db_manager.rollback(conn)
            finally:

                self.db_manager.close(conn)

