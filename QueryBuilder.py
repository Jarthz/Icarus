from prometheus_client import values


class QueryBuilder:

    @staticmethod
    def get_sql_select_delete(table_name, column_name, criteria=None, action='SELECT'):
        """
        :param table_name (str):
        :param column_name (str or list):
        :param criteria (4 tuple , 1: optional'AND/OR, 2:Column, 3:operator, 4:Value):
        :param action optional(str) SELECT or DELETE only:
        """
        if isinstance(column_name, list):
            columns_str = ', '.join(column_name)
        else:
            columns_str = column_name

        sql_statement = f"{action} {columns_str} FROM {table_name}"

        values = []
        if criteria:
            sql_statement, values = QueryBuilder.get_sql_where(criteria, sql_statement)
        return sql_statement, values

    #use paramatisation to defend from sql injection
    @staticmethod
    def get_sql_where(criteria, sql_statement):
        values = []
        where_clause = []
        for row in criteria:
            where_clause.append(f"{row[0]} {row[1]} {row[2]} ?")
            values.append(row[3])

        sql_statement += " WHERE "
        sql_statement += "".join(where_clause)
        return sql_statement, values

    @staticmethod
    def get_sql_create_table(table_name, schema):
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({schema}) STRICT"

    #for paramatisation
    @staticmethod
    def get_placeholders(columns):
        return ",".join(['?'] * len(columns))

    @staticmethod
    def get_sql_insert_statement(table_name, columns, placeholders):
        return f"""
            INSERT INTO {table_name} ({','.join(columns)})
            VALUES ({placeholders})
            """
    @staticmethod
    def get_sql_average_time(self):
        return f"""
            SELECT AverageJourneyTime AS avg_time
            FROM RouteTimes
            WHERE Origin = ? AND Destination = ?
            """
    @staticmethod
    def get_sql_arrival_times(self):
        return f"""
            SELECT ArrivalTime
            FROM Flights
            WHERE Origin = ? AND Destination = ?
            """

    @staticmethod
    def get_sql_update(table_name, change, criteria):
        sql_statement =f"""UPDATE {table_name} SET {change}"""
        values = []
        if criteria:
            sql_statement, values = QueryBuilder.get_sql_where(criteria, sql_statement)
        return sql_statement, values

#####################################
### authentication section #########

    @staticmethod
    def get_sql_validate_user():
        return f"""
        SELECT UserID, Password
        FROM Users
        WHERE Username = ?
        """

    @staticmethod
    def get_sql_add_user():
        return f"""
        INSERT INTO Users (Username, Password) VALUES (?, ?)
        """

    @staticmethod
    def get_sql_user():
        return f"""
        SELECT Password FROM Users WHERE Username = ?
        """

    @staticmethod
    def get_sql_transaction_log():
        return f"""
        INSERT INTO AuditLog (Username, Action, TableName, Details)
        VALUES (?, ?, ?, ?)
        """

######################################
###### canned reports section ########


    @staticmethod
    def get_sql_pilot_schedule():
        sql_statement = f"""
        SELECT
            p.FirstName || ' ' || p.LastName AS PilotName,
            f.FlightID,
            f.DepartureDate,
            f.DepartureTime,
            ao.AirportCode AS OriginCode,
            ao.AirportName AS OriginName,
            af.AirportCode AS DestinationCode,
            af.AirportName AS DestinationName,
            f.Status
        FROM Flights f
        JOIN Airports ao ON f.Origin = ao.AirportCode
        JOIN Airports af ON f.Destination = af.AirportCode
        JOIN Pilots p ON f.PilotID = p.PilotID
        WHERE f.PilotID = ?
        ORDER BY f.DepartureDate, f.DepartureTime;
        """
        return sql_statement

    @staticmethod
    def get_sql_number_of_flights(GroupBy):
        if GroupBy == 'Destination':
            return f"""
            SELECT 
                a.AirportCode,
                a.AirportName,
                COUNT(f.FlightID) AS NumberOfFlights
            FROM Flights f
            JOIN Airports a ON f.Destination = a.AirportCode
            GROUP BY f.Destination
            ORDER BY NumberOfFlights DESC;
            """
        elif GroupBy == 'Pilot':
            return f"""
            SELECT 
                p.FirstName || ' ' || p.LastName AS Pilot,
                p.PilotID,
                p.LicenseNumber,
                COUNT(f.FlightID) AS NumberOfFlights
            FROM Flights f
            JOIN Pilots p ON f.PilotID = p.PilotID
            GROUP BY f.PilotID
            ORDER BY NumberOfFlights DESC;
            """
        elif GroupBy == 'Origin':
            return f"""
            SELECT 
                a.AirportCode,
                a.AirportName,
                COUNT(f.FlightID) AS NumberOfFlights
            FROM Flights f
            JOIN Airports a ON f.Origin = a.AirportCode
            GROUP BY f.Origin
            ORDER BY NumberOfFlights DESC;
            """
        else:
            raise ValueError("Invalid GroupBy parameter. Use 'Destination', 'Pilot' or 'Origin'.")

