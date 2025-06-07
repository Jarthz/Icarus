from prometheus_client import values


class QueryBuilder:

    def get_sql_select_all(table_name):
        return f"SELECT * FROM {table_name}"

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

    def get_sql_where(criteria, sql_statement):
        values = []
        where_clause = []
        for row in criteria:
            where_clause.append(f"{row[0]} {row[1]} {row[2]} ?")
            values.append(row[3])

        sql_statement += " WHERE "
        sql_statement += "".join(where_clause)
        return sql_statement, values

    def get_sql_create_table(table_name, schema):
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"

    def get_placeholders(columns):
        return ",".join(['?'] * len(columns))

    def get_sql_insert_statement(table_name, columns, placeholders):
        return f"""
            INSERT INTO {table_name} ({','.join(columns)})
            VALUES ({placeholders})
            """

    def get_sql_average_time(self):
        return f"""
            SELECT AverageJourneyTime AS avg_time
            FROM RouteTimes
            WHERE Origin = ? AND Destination = ?
            """

    def get_sql_arrival_times(self):
        return f"""
            SELECT ArrivalTime
            FROM Flights
            WHERE Origin = ? AND Destination = ?
            """

    def get_sql_update(table_name, change, criteria):
        sql_statement =f"""UPDATE {table_name} SET {change}"""
        values = []
        if criteria:
            sql_statement, values = QueryBuilder.get_sql_where(criteria, sql_statement)
        return sql_statement, values

    @staticmethod
    def get_sql_pilot_schedule():
        sql_statement = f"""
        SELECT
            p.FirstName || ' ' || p.LastName AS PilotName,
            f.FlightID,
            f.DepartureDate,
            f.ArrivalTime,
            ao.AirportCode AS OriginCode,
            ao.AirportName AS OriginName,
            af.AirportCode as DestinationCode,
            af.AirportName AS DestinationName,
            f.Status
        FROM Flights f
        JOIN Airports ao ON f.Origin = ao.AirportID
        JOIN Airports af ON f.Destination = af.AirportID
        JOIN Pilots p ON f.PilotID = p.PilotID
        WHERE f.PilotID = ?
        ORDER BY f.DepartureDate, f.DepartureTime;
"""
        return sql_statement


