from LogicLayer import LogicLayer as logic
import tabulate

class CLI:
    def __init__(self):
        pass

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

