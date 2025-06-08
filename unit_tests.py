import CLI
import LogicLayer
import DAO
import DatabaseManager
import User

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


    """
    selected_table = cli.search_all_records()
    if selected_table:
        column_info = dao.get_table_columns(selected_table)
        criteria_list = cli.search_specific_records(column_info, selected_table)
        dao.select_or_delete(selected_table, '*', criteria_list)
    """
    print("\nstarting test 1 \n")

    selected_table = 'Flights'
    criteria_list = [('', 'Origin', '=', 'LAX'), ('AND', 'Status', '=', 'Scheduled')]
    rows, column = dao.select_or_delete(selected_table, '*', criteria_list)
    cli.print_results(rows, column)

    print("\nstarting test 2 \n")

    selected_table = 'Flights'
    criteria_list = ('', 'Origin', '=', 'LAX')
    if isinstance(criteria_list, tuple):
        criteria_list = [criteria_list]
    rows, column = dao.select_or_delete(selected_table, '*', criteria_list)
    cli.print_results(rows, column)

