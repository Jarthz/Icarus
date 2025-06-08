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
                selected_table = self.cli.get_limited_tables('add')
                if selected_table:
                    column_info = self.dao.get_table_columns(selected_table)
                    columns_to_prompt = self.get_columns_to_prompt(column_info)
                    if not columns_to_prompt:
                        continue
                    inputs = self.cli.add_record(columns_to_prompt)
                    if inputs:
                        data, columns = inputs
                        self.add_record(selected_table, data, columns)

            if main_menu_choice == 2:
                selected_table = self.cli.get_limited_tables('delete')
                column_info = self.dao.get_table_columns(selected_table)
                if not column_info:
                    continue

                column_dict = self.menu_dict_builder(column_info)
                criteria = self.cli.search_specific_records(column_dict)
                if criteria:
                    self.delete_record(selected_table, criteria)

            if main_menu_choice == 3:
                selected_table = self.cli.search_all_records()
                if selected_table:
                    result = self.dao.select_or_delete(selected_table, '*')
                    self.safely_print(result)

            if main_menu_choice == 4:
                selected_table = self.cli.search_all_records()
                if selected_table:
                    column_info = self.dao.get_table_columns(selected_table)
                    if not column_info:
                        continue
                    column_dict = self.menu_dict_builder(column_info)
                    criteria = self.cli.search_specific_records(column_dict)
                    if criteria:
                        if isinstance(criteria, tuple):
                            criteria = [criteria]
                        result = self.dao.select_or_delete(selected_table, "*", criteria)
                        self.safely_print(result)

            if main_menu_choice == 5:
                selected_table = self.cli.get_limited_tables('update')
                if selected_table:
                    column_info = self.dao.get_table_columns(selected_table)
                    update_list, where_list = self.cli.get_update_table_value(column_info)
                    if not update_list or not where_list:
                        continue
                    self.update_record(selected_table, update_list, where_list)

            #this can be done in menu 3
            #will eventually abstract away that option in menu 3 based on
            if main_menu_choice == 6:
                selected_table = 'AuditLog'
                result = self.dao.select_or_delete(selected_table, "*")
                self.safely_print(result)

            if main_menu_choice == 7:
                selected_report = self.cli.get_report()
                if selected_report == 1:
                    pilot_id = self.cli.get_pilot_id()
                    result = self.dao.get_pilot_schedule(pilot_id)
                    self.safely_print(result)
                elif selected_report == 2:
                    result = self.dao.get_number_of_flights('Destination')
                    self.safely_print(result)
                elif selected_report == 3:
                    result = self.dao.get_number_of_flights('Pilot')
                    self.safely_print(result)
                elif selected_report == 4:
                    result = self.dao.get_number_of_flights('Origin')
                    self.safely_print(result)


    def safely_print(self, result):
        if result:
            row, coluns = result
            self.cli.print_results(row, coluns)

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

    def get_columns_to_prompt(self, columns_info):
        columns_to_prompt = tuple(
            (col_name, col_type)
            for col_name, col_type, pk in columns_info
            if pk == 0
        )
        if not columns_to_prompt:
            print("No columns available for table")
            return []
        return columns_to_prompt

    def menu_dict_builder(self, columns_info):
        columns_dict = {index: col_name for index, (col_name, _, _) in enumerate(columns_info, start=1)}
        next_key = max(columns_dict.keys()) + 1
        columns_dict[next_key] = 'Exit'
        return columns_dict



