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
    dao.create_triggers()
    files = ['Airports.csv', 'Pilots.csv', 'Flights.csv', 'FlightCrew.csv']
    dao.insert_legacy_data(files)
    dao.add_user("admin", "Password123")
    admin1 = User.User('admin')
    dao.add_data('Flights', ('2025-07-30', 'LHR', 'LAX', '07:00', '19:00', 'Scheduled'), ('DepartureDate', 'Origin', 'Destination', 'DepartureTime', 'ArrivalTime', 'Status'), admin1)



    cli.display_welcome_screen()
    user = logic.authenticate()
    logic.main_menu()
