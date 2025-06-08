import CLI
import LogicLayer
import DAO
import DatabaseManager
import User
from QueryBuilder import QueryBuilder as qb

if __name__ == "__main__":

    cli = CLI.CLI()
    dbm = DatabaseManager.DatabaseManager()
    dao = DAO.DAO(dbm)
    logic = LogicLayer.LogicLayer(dao, cli)

    dao.create_table()
    dao.drop_table()
    dao.create_table()
    files = ['Airports.csv', 'Pilots.csv', 'RouteTimes.csv', 'Flights.csv']
    dao.insert_legacy_data(files)
    dao.add_user("admin", "Password123")

    logic.user = User.User("admin")

    print("\nstarting test 1 \n")
    selected_table = 'Flights'
    update_list = [('Origin', '=', 'asdf')]
    where_list = [('', 'Origin', '=', 'LAX')]

    def convert_list(update_list):
        update_string = ", ".join(f"{col} {operation} '{value}'" for col, operation, value in update_list)
        return update_string

    update_string = convert_list(update_list)

    dao.update(selected_table, update_string, where_list)

    rows, columns = dao.select_or_delete(selected_table, "*",)
    cli.print_results(rows, columns)

    def convert_update_to_where_list(update_list, operator='OR'):
        return [
            ('' if idx == 0 else operator, col, op, val)
            for idx, (col, op, val) in enumerate(update_list)
        ]
    where_list2 = convert_to_where_list(update_list, operator='OR')

    rows, columns = dao.select_or_delete(selected_table, "*", where_list2)
    cli.print_results(rows, columns)



