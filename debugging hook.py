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
    files = ['Airports.csv', 'Pilots.csv', 'Flights.csv', 'FlightCrew.csv']
    dao.insert_legacy_data(files)
    dao.create_triggers()
    dao.add_user("admin", "Password123")

    logic.user = User.User("admin")

