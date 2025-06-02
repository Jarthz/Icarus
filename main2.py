import DatabaseManager
import sqlite3

def create_tables():
    db_manager = DatabaseManager.DatabaseManager()
    conn = db_manager.connect()
    if conn:
        try:
            cursor = conn.cursor()

            # Create Airports table
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Airports (
                        Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        AirportCode TEXT NOT NULL UNIQUE,        
                        AirportName TEXT NOT NULL,               
                        AirportCountry TEXT NOT NULL,            
                        Runways INTEGER NOT NULL                 
                    )
                """)
                print("Created Airports table.")
            except sqlite3.Error as e:
                print(f"Error creating Airports table: {e}")
                raise

            # Create Pilots table
            try:
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
                print("Created Pilots table.")
            except sqlite3.Error as e:
                print(f"Error creating Pilots table: {e}")
                raise

            db_manager.close(conn)

        except Exception as e:
            print(f"Error during table creation: {e}")
            db_manager.rollback(conn)
            db_manager.close(conn)

if __name__ == '__main__':
    create_tables()