from tabulate import tabulate
from QueryBuilder import QueryBuilder as qb
import bcrypt
from User import User
from Schema import Schema

class LogicLayer:
    def __init__(self, dao, cli):
        self.dao = dao
        self.max_attempts = 3
        self.cli = cli
        self.user = None

    def authenticate(self):
        attempts = 0
        while attempts < self.max_attempts:
            username, password = self.cli.prompt_for_login()
            if self.check_credentials(username, password):
                print("Login Successful")
                self.user = User(username=username)

                return self.user

            else:
                attempts += 1
                print(f"Login failed. Attempts remaining: {self.max_attempts - attempts}\n")
        print("Max attempts reached. Exiting program.")
        exit(1)

    def check_credentials(self, username, password):
        def operation(conn):
            cursor = conn.cursor()
            sql_statement = qb.get_sql_user()
            cursor.execute(sql_statement, (username,))
            result = cursor.fetchone()
            if result:
                stored_hash = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    return True
            return False
        return self.dao.transaction_wrapper(operation)

    def convert_update_list(self, update_list):
        update_string = ", ".join(f"{col} {operation} '{value}'" for col, operation, value in update_list)
        return update_string

    def main_menu(self):
        while True:
            main_menu_choice = self.cli.main_menu()
            action = Schema.main_menu.get(main_menu_choice)

            method_name = action[1]

            if method_name == 'exit':
                print("Exiting program.")
                exit(0)

            if main_menu_choice == 1:
                result = self.cli.add_record(self.dao)
                if result:
                    select_table, data, columns = result
                    self.add_record(select_table, data, columns)

            if main_menu_choice == 2:
                selected_table = self.cli.delete_record()
                column_info = self.dao.get_table_columns(selected_table)

                result = self.cli.delete_record_2(column_info, selected_table)
                if result:
                    select_table, value, columns = result
                    data = [('', columns, '=', value)]
                    if self.delete_record(select_table, data):
                        print(f"Successfully deleted {columns} {value} from {select_table}")

            if main_menu_choice == 3:
                selected_table = self.cli.search_all_records()
                if selected_table:
                    rows, columns = self.dao.select_or_delete(selected_table, '*')
                    self.cli.print_results(rows, columns)

            if main_menu_choice == 4:
                selected_table = self.cli.search_all_records()
                if selected_table:
                    column_info = self.dao.get_table_columns(selected_table)
                    criteria = self.cli.search_specific_records(column_info, selected_table)
                    if isinstance(criteria, tuple):
                        criteria = [criteria]
                    rows, columns = self.dao.select_or_delete(selected_table, "*", criteria)
                    self.cli.print_results(rows, columns)

            if main_menu_choice == 5:
                selected_table = self.cli.get_update_or_delete_table('update')
                if selected_table:
                    column_info = self.dao.get_table_columns(selected_table)
                    update_list, where_list = self.cli.get_update_table_value(selected_table, column_info)
                    self.update_record(selected_table, update_list, where_list)


    def convert_update_to_where_list(self, update_list, operator='OR'):
        return [
            ('' if idx == 0 else operator, col, op, val)
            for idx, (col, op, val) in enumerate(update_list)
        ]

    def get_columns(self, selected_table):
        return self.dao.get_table_columns(selected_table)

    def add_record(self, table, data, columns):
        self.dao.add_data(table, data, columns, self.user)

    def delete_record(self, table, data):
        self.dao.select_or_delete(table, '', data, 'DELETE', self.user)

    def update_record(self, selected_table, update_list, where_list):
        update_string = self.convert_update_list(update_list)
        self.dao.update(selected_table, update_string, where_list, self.user)
        update_to_where = self.convert_update_to_where_list(update_list)
        rows, columns = self.dao.select_or_delete(selected_table, "*", update_to_where)
        self.cli.print_results(rows, columns)

