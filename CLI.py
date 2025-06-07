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

        print("Main Menu")
        print("**********")
        for key, value in menu_options.items():
            print(f"{key}: {value[0]}")

        return self.validation(len(menu_options))

    def add_record(self, dao):
        table_options = {1: "Airports", 2: "Pilots", 3: "Flights", 4: "Return to Main Menu"}
        print("Select Table for new record")
        print("**********")

        for key, value in table_options.items():
            print(f"{key}: {value}")

        first_add_choice = self.validation(4)

        if first_add_choice == 4:
            print("Return to Main Menu")
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



