from tabulate import tabulate
from QueryBuilder import QueryBuilder as qb
import bcrypt

class LogicLayer:
    def __init__(self, dao):
        self.dao = dao
        self.max_attempts = 3

    def authenticate(self, cli):
        attempts = 0
        while attempts < self.max_attempts:
            username, password = cli.prompt_for_login()
            if self.check_credentials(username, password):
                print("Login Successful")
                return True
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