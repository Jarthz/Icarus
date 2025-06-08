
import pandas as pd
import sqlite3
import os
from Schema import Schema
from QueryBuilder import QueryBuilder as qb
import bcrypt



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
                    cursor.execute(qb.get_sql_create_table(table_name, schema))
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
                    placeholders = qb.get_placeholders(columns)
                    statement = qb.get_sql_insert_statement(table_name, columns, placeholders)

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

#learnt this after the above, still will be useful for updates and deletes
    def transaction_wrapper(self, operation):
        conn = self.db_manager.connect()
        if not conn:
            print("No database connection.")
            return None

        result = None
        try:
            result = operation(conn)
            conn.commit()
            print("Operation Complete.")
        except Exception as e:
            print(f"Error performing operation: {e}")
            self.db_manager.rollback(conn)
        finally:
            self.db_manager.close(conn)
        return result

    def get_row_count(self, table_name, conn=None):
        def operation(inner_conn):
            cursor = inner_conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]
        if conn:
            return operation(conn)
        else:
            return self.transaction_wrapper(operation)

    def get_table_columns(self, table_name, conn=None):
        def operation(inner_conn):
            cursor = inner_conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = []
            for row in cursor.fetchall():
                col_name = row[1]
                col_type = row[2]
                is_primary_key = row[5]
                columns.append((col_name, col_type, is_primary_key))
            return columns
        if conn:
            return operation(conn)
        else:
            return self.transaction_wrapper(operation)

    def add_data(self, table, data, table_columns, user=None):
        """

        :param table string:
        :param data tuple of values:
        :param table_columns tuple of columns for the table schema:
        :param user object:
        :return:
        """

        def operation(conn):
            if table_columns is None:
                print(f"No table columns for table {table}.")
                return

            table_size = self.get_row_count(table, conn)

            if len(data) != len(table_columns):
                print(f"Data length mismatch: expected {len(table_columns)}, got {len(data)}.")
                print(f"Columns: {table_columns}")
                return

            cursor = conn.cursor()
            placeholders = qb.get_placeholders(table_columns)
            statement = qb.get_sql_insert_statement(table, table_columns, placeholders)

            cursor.execute(statement, data)
            print(f"Successfully inserted data into {table}.")

            #log transaction
            self.log_transaction(conn, user.username, 'INSERT', table, details=f"Inserted record with values {data}.")

            new_table_size = self.get_row_count(table, conn)
            return print(f"Old table size: {table_size}. New table size: {new_table_size}.")
        return self.transaction_wrapper(operation)

    def select_or_delete(self, table, column, criteria=None, action='SELECT', user=None):
        def operation(conn):
            cursor = conn.cursor()
            statement, values = qb.get_sql_select_delete(table, column, criteria, action)
            print(statement)
            print(values)
            cursor.execute(statement, values)
            if action.upper() == 'SELECT':
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return rows, columns
            elif action.upper() == 'DELETE':
                self.log_transaction(conn, user.username, action, table, details=f"{statement} {values}.")
                return [], []



        return self.transaction_wrapper(operation)

    def get_average_time(self, origin, destination):
        def operation(conn):
            cursor = conn.cursor()
            statement = qb.get_sql_average_time()
            values = (origin, destination)
            cursor.execute(statement, values)
            print(statement)
            print(values)

            result = cursor.fetchone()
            print(result)
            return result
        return self.transaction_wrapper(operation)

    def update(self, table, change, criteria=None):
        def operation(conn):
            cursor = conn.cursor()
            statement, values= qb.get_sql_update(table, change, criteria)
            cursor.execute(statement, values)
            print(f"Successfully updated data from {table} with change {change}.")
        return self.transaction_wrapper(operation)

    def get_pilot_schedule(self, PilotID):
        def operation(conn):
            cursor = conn.cursor()
            statement = qb.get_sql_pilot_schedule()
            cursor.execute(statement, (PilotID,))
            result = cursor.fetchall()
            for row in result:
                print(row)
            return
        return self.transaction_wrapper(operation)

    def get_number_of_flights(self, GroupBy):
        def operation(conn):
            cursor = conn.cursor()
            statement = qb.get_sql_number_of_flights(GroupBy)
            cursor.execute(statement)
            result = cursor.fetchall()
            for row in result:
                print(row)
            return
        return self.transaction_wrapper(operation)

    def add_user(self, username, password):
        def operation(conn):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor = conn.cursor()
            statement = qb.get_sql_add_user()
            cursor.execute(statement, (username, hashed_password.decode('utf-8')))
            print(f"Successfully added user {username}.")
        return self.transaction_wrapper(operation)

    def log_transaction(self, conn, username, action, table_name=None, details=None):
        cursor = conn.cursor()
        sql_statement = qb.get_sql_transaction_log()
        cursor.execute(sql_statement, (username, action, table_name, details))









