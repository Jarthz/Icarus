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

    print("\nstarting test 1 \n")
    selected_table = cli.search_all_records()
    print(selected_table)
