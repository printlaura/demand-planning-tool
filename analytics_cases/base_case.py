import pandas as pd
from db_connector import get_snowflake_connection


class BaseAnalyticsCase:
    def __init__(self, sql_file):
        self.sql_file = sql_file
        self.conn = get_snowflake_connection()

    def load_sql_query(self):
        with open(self.sql_file, 'r') as file:
            query = file.read()
        return query

    def run_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
        return data
