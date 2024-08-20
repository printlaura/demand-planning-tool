import pandas as pd
from db_connector import get_snowflake_connection


class BaseAnalyticsCase:
    def __init__(self, sql_file):
        self.sql_file = sql_file
        self.conn = get_snowflake_connection()

    def load_sql_query(self, **filters):
        with open(self.sql_file, 'r') as file:
            query = file.read()

        if filters:
            query = query.format(**filters)

        return query

    def run_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            columns = [col[0] for col in cur.description] if cur.description else []
        return data, columns

    def data_to_df(self, data, columns):
        if not data or not columns:
            raise ValueError("No data or columns available to convert to DataFrame")

        if isinstance(data, list) and all(isinstance(row, tuple) for row in data):
            if isinstance(columns, list) and all(isinstance(col, str) for col in columns):
                return pd.DataFrame(data, columns=columns)
            else:
                raise ValueError("Columns should be a list of string column names")
        else:
            raise ValueError("Data should be a list of tuples")

    def __del__(self):
        self.conn.close()
