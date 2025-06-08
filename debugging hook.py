import CLI
import LogicLayer
import DAO
import DatabaseManager
import User
from QueryBuilder import QueryBuilder as qb
from Schema import Schema

if __name__ == "__main__":

    cli = CLI.CLI()
    dbm = DatabaseManager.DatabaseManager()
    dao = DAO.DAO(dbm)
    logic = LogicLayer.LogicLayer(dao, cli)

    dao.create_table()
    dao.drop_table()
    dao.create_table()
    files = ['Airports.csv', 'Pilots.csv', 'Flights.csv']
    dao.insert_legacy_data(files)
    dao.add_user("admin", "Password123")

    logic.user = User.User("admin")

    selected_table1 = cli.get_add_table()
    print("1", selected_table1)

    selected_table2 = cli.get_update_or_delete_table('Add')
    print("2", selected_table2)







