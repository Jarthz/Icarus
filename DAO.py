import pandas as pd
import sqlite3
import os
import Schema


class DAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self, table=Schema.Tables):
        conn = self.db_manager.connect()
        if table is None:
            print("No table specified. Please provide a dictionary {\"table name\": \"columns TYPE,\"}.")
            return
        if conn:
            try:
                cursor = conn.cursor()
                for table_name, schema in table.items():
                    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
                    print(f"Table {table_name} created.")
                conn.commit()
                print("Success! All tables created, committed to DB.")
            except Exception as e:
                print(f"Failed to create table {table_name} rolling back entire transaction: {e}")
                self.db_manager.rollback(conn)
            finally:
                self.db_manager.close(conn)

#polymorphism to make this generic
    def drop_table(self, table=Schema.Tables):
        """
        Drops tables in database
        Accepts:
        single table name (string)
        list of table names (list)
        default dictonary of all tables if not argument

        """
        conn = self.db_manager.connect()
        if table is None:
            print("No table specified.")
            return

        tables_to_drop = []

        if isinstance(table, str):
            tables_to_drop.append(table)
        elif isinstance(table, list):
            tables_to_drop.extend(table)
        elif isinstance(table, dict):
            tables_to_drop.extend(table.keys())
        else:
            print(f"Invalid table name {table}. Valid types: Single table string, list, dictionary")
            return

        if conn:
            try:
                cursor = conn.cursor()
                for table_name in tables_to_drop:
                    try:
                        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                        print(f"Success! Table {table_name} dropped.")
                    except Exception as e:
                        print(f"Error dropping table {table_name}: {e}")
                        raise
                conn.commit()
                print("All tables dropped, committed to DB.")
            except Exception as e:
                print(f"Error dropping a table, rolling back entire transaction: {e}")
                self.db_manager.rollback(conn)
            finally:
                self.db_manager.close(conn)

    def insert_legacy_data(self, files):
        for file in files:
            table_name = os.path.splitext(os.path.basename(file))[0]
            print(f"Inserting {table_name}...")

            try:
                df = pd.read_csv(file)
            except Exception as e:
                print(f"Error reading file {file}: {e}")
                raise

            conn = self.db_manager.connect()
            if conn:
                try:
                    cursor = conn.cursor()

                    columns = list(df.columns)
                    placeholders = ",".join(['?'] * len(columns))
                    statement = f"""
                        INSERT INTO {table_name} ({','.join(columns)})
                        VALUES ({placeholders})
                        """

                    for index, row in df.iterrows():
                        values = tuple(row[col] for col in columns)
                        cursor.execute(statement, values)

                    print(f"Success! Inserted data from {file} into {table_name}.")
                    conn.commit()
                except Exception as e:
                    print(f"Error inserting data from {file} check that columns = schema: {e}")
                    self.db_manager.rollback(conn)
                finally:
                    self.db_manager.close(conn)





