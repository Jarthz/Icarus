from pandas.core.interchange import column
from pandas.io.sas.sas_constants import column_type_length

from LogicLayer import LogicLayer as logic
import tabulate
from Schema import Schema

class CLI:
    def __init__(self):
        self.username = None

    def display_welcome_screen(self):
        print("=" * 50)
        print("Welcome to Icarus")
        print("=" * 50)
        print("")

    def prompt_for_login(self):
        username = input('Enter username: ')
        password = input('Enter password: ')
        return username, password


    def print_results(rows, columns):
        print(tabulate(rows, headers=columns, tablefmt="grid"))

    def validation(self, max_value):
        while True:
            try:
                menu_choice = int(input("\nEnter your choice: "))
                if 1 <= menu_choice <= max_value:
                    return menu_choice
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input, please choose a valid integer")

    def main_menu(self):
        menu_options = Schema.main_menu

        print("\nMain Menu")
        print("**********")
        for key, value in menu_options.items():
            print(f"{key}: {value[0]}")

        return self.validation(len(menu_options))

    def add_record(self, dao):
        table_options = {1: "Airports", 2: "Pilots", 3: "Flights", 4: "Return to Main Menu"}
        print("\nSelect Table for new record")
        print("**********")

        for key, value in table_options.items():
            print(f"{key}: {value}")

        first_add_choice = self.validation(4)

        if first_add_choice == 4:
            print("\nReturning to Main Menu\n")
            return

        selected_table = table_options[first_add_choice]

        # Retrieve columns dynamically using PRAGMA
        columns_info = dao.get_table_columns(selected_table)
        if not columns_info:
            print(f"Error: Could not retrieve columns for table '{selected_table}'.")
            return

        # Skip auto-increment PKs (assume PK == 1)
        columns_to_prompt = tuple(
            (col_name, col_type)
            for col_name, col_type, pk in columns_info
            if pk == 0
        )

        if not columns_to_prompt:
            print(f"No columns available for data entry in '{selected_table}'.")
            return

        print("\nPlease enter values for the following fields:")
        data = tuple(
            (input(f"Enter {col_name} in format {col_type}: ").strip())
            for col_name, col_type in columns_to_prompt
        )

        cols = tuple(col_name for col_name, _ in columns_to_prompt)

        # Insert record via DAO
        return selected_table, data, cols

    def delete_record(self):
        table_options = {1: "Airports", 2: "Pilots", 3: "Flights", 4: "Return to Main Menu"}
        print("\nSelect Table to delete record")
        print("**********")

        for key, value in table_options.items():
            print(f"{key}: {value}")

        choice = self.validation(4)

        if choice == 4:
            print("\nReturning to Main Menu\n")
            return

        selected_table = table_options[choice]
        return selected_table

    def delete_record_2(self, columns_info, selected_table):

        if not columns_info:
            print(f"Error: Could not retrieve columns for table '{selected_table}'.")
            return

        columns_dict = {index: col_name for index, (col_name,_,_) in enumerate(columns_info, start=1)}
        next_key = max(columns_dict.keys()) + 1
        columns_dict[next_key] = 'Exit'

        print("\n choose a number to select input column for record deletion from table")
        print("**********")
        for index, col_name in columns_dict.items():
            print(f"{index}: {col_name}")

        column_choice = self.validation(len(columns_dict))
        column = columns_dict[column_choice]
        if column_choice == next_key:
            print("\nReturning to Main Menu\n")
            return

        value = int(input(f"Enter value to delete from {column} =: "))

        return selected_table, value, column

    def search_all_records(self):
        table_options, next_key = self.get_table_dictionary()

        choice = self.validation(len(table_options))

        if choice == next_key:
            print("\nReturning to Main Menu\n")
            return

        column = table_options[choice]

        return column

    def print_results(self, rows, columns):
        print(tabulate.tabulate(rows, headers=columns, tablefmt='fancy_grid'))

    def get_table_dictionary(self):
        table_options = {index: key for index, key in enumerate(Schema.Tables, start=1)}
        next_key = max(table_options.keys()) + 1
        table_options[next_key] = 'Exit'

        print("\nSelect Table to view")
        print("**********")

        for key, value in table_options.items():
            print(f"{key}: {value}")

        return table_options, next_key

    def search_specific_records(self, columns_info, selected_table):
        if not columns_info:
            print(f"Error: Could not retrieve columns for table '{selected_table}'.")
            return

        criteria_list = []

        columns_dict = {index: col_name for index, (col_name, _, _) in enumerate(columns_info, start=1)}
        next_key = max(columns_dict.keys()) + 1
        columns_dict[next_key] = 'Exit'

        while True:

            #first input doesn't need an and/or operator so loop only when the list has a value
            if criteria_list:
                logical_operator = input("Optional: Enter logicial (AND/OR) to chain conditions, or press enter to skip: ").strip().upper()
                if logical_operator not in ['AND', 'OR']:
                    print("No logical operator, not chaining conditions.")
                    return criteria_list
            else:
                logical_operator = ''


            print("\n choose a number to select column to search specific criteria from table")
            print("**********")
            for index, col_name in columns_dict.items():
                print(f"{index}: {col_name}")

            column_choice = self.validation(len(columns_dict))
            column = columns_dict[column_choice]
            if column_choice == next_key:
                print("\nReturning to Main Menu\n")
                return

            comparison_operator = input(f"Enter comparison operator to search from {column} =, <>, <, >, etc : ").strip()
            value = input(f'Enter value to search from {column}: ').strip()



            criteria_list.append((logical_operator, column, comparison_operator, value))


        return criteria_list

    def get_update_or_delete_table(self, type):
        table_options = {1: "Airports", 2: "Pilots", 3: "Flights", 4: "Return to Main Menu"}
        print(f"\nSelect Table to {type} record")
        print("**********")

        for key, value in table_options.items():
            print(f"{key}: {value}")

        choice = self.validation(4)

        if choice == 4:
            print("\nReturning to Main Menu\n")
            return

        selected_table = table_options[choice]
        return selected_table

    def get_update_table_value(self, selected_table, columns_info):
        """
        to do,
        1) get columns to update
        2) get column values to update to
        3) make list for multi updates
        4) criteria list like specific search
        5) get AND/OR
        6) get columns
        7) get operator =><
        8) get value
        :param columns_info:
        :param selected_table:
        :return:
        """

        if not columns_info:
            print(f"Error: Could not retrieve columns for table '{selected_table}'.")
            return

        # Skip auto-increment PKs (assume PK == 1)
        columns = tuple(
            col_name
            for col_name, col_type, pk in columns_info
            if pk == 0
        )

        #remove the primary key from available choices
        columns_dict = {index: col_name for index, col_name in enumerate(columns, start=1)}

        #add an exit choice
        next_key = max(columns_dict.keys()) + 1
        columns_dict[next_key] = 'Finish selecting columns'

        change_list = []
        columns_dict_reduced = columns_dict.copy()

        while True:
            if change_list:
                print(f"\n Enter a number to select an ADDITIONAL column to update")
            else:
                print("\n Enter a number to select a column to update")
            print("**********")
            for index, col_name in columns_dict_reduced.items():
                print(f"{index}: {col_name}")

            column_choice_int = self.validation(len(columns_dict_reduced))
            print("col choice: ", column_choice_int)

            #exit out on exit choice
            if column_choice_int == len(columns_dict_reduced):
                if not change_list:
                    print("\nNo columns selected, returning to Main Menu\n")
                    return [], []
                break ## need to handle this better

            #convert integer choice to string
            column_update = columns_dict_reduced[column_choice_int]

            value_update = input(f"Enter new value for {column_update}: ").strip()
            change_list.append((column_update, "=", value_update))

            del columns_dict_reduced[column_choice_int]
            columns_dict_reduced = {new_index: value for new_index, value in enumerate(columns_dict_reduced.values(), start=1)}

        criteria_list = []
        while True:

            # first input doesn't need an and/or operator so loop only when the list has a value
            if criteria_list:
                logical_operator = input(
                    "Optional: Enter logicial (AND/OR) to chain conditions, or press enter to skip: ").strip().upper()
                if logical_operator not in ['AND', 'OR']:
                    print("No logical operator, not chaining conditions.")
                    return change_list, criteria_list
            else:
                logical_operator = ''

            print("\n You MUST enter a number to select a column and specify a condition for WHERE updates take place")
            print("**********")
            for index, col_name in columns_dict.items():
                print(f"{index}: {col_name}")

            column_choice = self.validation(len(columns_dict))
            column_where = columns_dict[column_choice]
            if column_choice == next_key:
                if not criteria_list:
                    print("\nError, you didn't input any criteria. Returning to Main Menu\n")
                    return [], []
                break

            comparison_operator = input(
                f"Enter comparison operator to search from {column_where} =, <>, <, >, etc : ").strip()
            value_where = input(f'Enter value to search from {column_where}: ').strip()

            criteria_list.append((logical_operator, column_where, comparison_operator, value_where))

        #add change and criteria list of tuples
        return change_list, criteria_list





