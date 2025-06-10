class QueryBuilder:

    @staticmethod
    def get_sql_select_delete(table_name, column_name, criteria=None, action='SELECT'):
        """
        Constructs a parameterised SQL SELECT or DELETE statement for the specified table.

        Args:
            table_name (str): Name of the table to query.
            column_name (str or list): Column(s) to select or delete.
            criteria (list of tuple, optional): A list of 4-tuples specifying WHERE clause conditions.
                Each tuple should be in the format:
                    (logical_operator, column, operator, value)
                where:
                    logical_operator (str): Optional; can be 'AND' or 'OR' (first condition uses an empty string '').
                    column (str): Column name to filter on.
                    operator (str): Comparison operator (e.g. '=', '<', '>', '<>').
                    value (str): Value to compare against.
            action (str, optional): Either 'SELECT' or 'DELETE'. Defaults to 'SELECT'.

        Returns:
            tuple: A tuple containing the SQL statement (str) and a list of parameter values.
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
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"

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
    def get_sql_arrival_times():
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
            fc.Role,
            f.FlightID,
            f.DepartureDate,
            f.DepartureTime,
            ao.AirportCode AS OriginCode,
            ao.AirportName AS OriginName,
            af.AirportCode AS DestinationCode,
            af.AirportName AS DestinationName,
            f.Status
        FROM FlightCrew fc
        JOIN Flights f ON fc.FlightID = f.FlightID
        JOIN Airports ao ON f.Origin = ao.AirportCode
        JOIN Airports af ON f.Destination = af.AirportCode
        JOIN Pilots p ON fc.PilotID = p.PilotID
        WHERE fc.PilotID = ?
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
                COUNT(fc.FlightID) AS NumberOfFlights
            FROM FlightCrew fc
            JOIN Pilots p ON fc.PilotID = p.PilotID
            GROUP BY fc.PilotID
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

#############################
######### Triggers for integrity

    #auto updates flights table if you assign pilot to flight
    @staticmethod
    def sql_create_crew_trigger():
        return """CREATE TRIGGER IF NOT EXISTS trg_update_crew_assigned
        AFTER INSERT ON FlightCrew
        BEGIN
            UPDATE Flights
            SET CrewAssigned = (
                SELECT COUNT(*)
                FROM FlightCrew
                WHERE FlightID = NEW.FlightID
            )
            WHERE FlightID = NEW.FlightID;
        END;
        
        CREATE TRIGGER IF NOT EXISTS trg_update_crew_assigned_delete
        AFTER DELETE ON FlightCrew
        BEGIN
            UPDATE Flights
            SET CrewAssigned = (
                SELECT COUNT(*)
                FROM FlightCrew
                WHERE FlightID = OLD.FlightID
            )
            WHERE FlightID = OLD.FlightID;
        END;
        """


    @staticmethod
    def sql_no_double_bookings():
        return """CREATE TRIGGER IF NOT EXISTS trg_no_double_booking
        AFTER INSERT ON FlightCrew
        BEGIN
            -- Check for conflicting flights
            SELECT
                CASE
                    WHEN (
                        SELECT COUNT(*)
                        FROM FlightCrew fc
                        JOIN Flights f1 ON fc.FlightID = f1.FlightID
                        WHERE
                            fc.PilotID = NEW.PilotID
                            AND f1.DepartureDate = (
                                SELECT DepartureDate
                                FROM Flights
                                WHERE FlightID = NEW.FlightID
                            )
                            AND fc.FlightID != NEW.FlightID
                    ) > 0
                    THEN
                        RAISE(ABORT, 'Pilot is already assigned to another flight on this date.')
                END;
        END;"""

    @staticmethod
    def sql_delete_triggers():
        return """
        DROP TRIGGER IF EXISTS trg_update_crew_assigned;
        DROP TRIGGER IF EXISTS trg_no_double_booking;
        """