import pandas as pd


class BaseAnalyticsCase:
    def __init__(self, sql_file, conn):
        self.sql_file = sql_file
        self.conn = conn

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

        return pd.DataFrame(data, columns=columns)

    def __del__(self):
        self.conn.close()
