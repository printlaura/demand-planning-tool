import pandas as pd
from db_connector import get_snowflake_connection


class SnowflakeQueryExecutor:

    @staticmethod
    def execute_query(query):
        try:
            conn = get_snowflake_connection()
            df = pd.read_sql(query, conn)
            conn.close()

            print("Data successfully loaded.")
            return df

        except Exception as e:
            print(f"Error loading data: {e}")
            return None
