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
    admin1 = User.User('admin')
    dao.add_data('Flights', ('21/07/2025', 'LHR', 'LAX', 11, '07:00', '19:00', 'Scheduled'), ('DepartureDate', 'Origin', 'Destination','PilotID', 'DepartureTime', 'ArrivalTime', 'Status'), admin1)



    cli.display_welcome_screen()
    user = logic.authenticate()
    logic.main_menu()
