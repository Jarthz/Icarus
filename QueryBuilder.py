class QueryBuilder:

    def get_sql_select_all(table_name):
        return f"SELECT * FROM {table_name}"

    def get_sql_select_delete(table_name, column_name, criteria=None, action='SELECT'):
        """
        :param table_name (str):
        :param column_name (str or list0:
        :param criteria (dict, optional):
        :return: tuple (sql_statment, params)
        """
        if isinstance(column_name, list):
            columns_str = ', '.join(column_name)
        else:
            columns_str = column_name

        sql_statement = f"{action} {columns_str} FROM {table_name}"

        values = []
        if criteria:
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