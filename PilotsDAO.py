import pandas as pd
import sqlite3

class PilotsDAO:

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self):
        conn = self.db_manager.connect()

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Pilots (
                        Pilot_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT NOT NULL,
                        LastName TEXT NOT NULL,
                        LicenseNumber TEXT UNIQUE NOT NULL,
                        LicenseCountry TEXT NOT NULL,
                        ExperienceYears INTEGER NOT NULL,
                        Rank TEXT NOT NULL,
                        Email TEXT
                    )
                """)
                conn.commit()
                print("Pilot table created successfully")
            except Exception as e:
                print(f"Failed to create Pilot table: {e}")
                self.db_manager.rollback(conn)
            finally:
                self.db_manager.close(conn)



    def insert_data(self):
        try:
            df = pd.read_csv("Pilots.csv")
        except Exception as e:
            print(f"Failed to read Pilots.csv: {e}")
            return

        conn = self.db_manager.connect()
        if conn:
            try:
                cursor = conn.cursor()
                for index, row in df.iterrows():
                    FirstName = row["FirstName"].strip()
                    LastName = row["LastName"].strip()
                    LicenseNumber = row["LicenseNumber"].strip()
                    LicenseCountry = row["LicenseCountry"].strip()
                    ExperienceYears = int(row["ExperienceYears"])
                    Rank = row["Rank"].strip()
                    Email = row["Email"].strip()

                    cursor.execute("""
                    INSERT INTO Pilots (FirstName, LastName, LicenseNumber, LicenseCountry, ExperienceYears, Rank, Email)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (FirstName, LastName, LicenseNumber, LicenseCountry, ExperienceYears, Rank, Email))
                    print(f"inserted Pilot {FirstName} into Pilots table")
                conn.commit()
                print("Pilots table inserted successfully")
            except (sqlite3.Error, KeyError, ValueError) as e:
                print(f"Failed to insert {FirstName}: {e}. Rolling back")
                self.db_manager.rollback(conn)
            finally:
                self.db_manager.close(conn)

