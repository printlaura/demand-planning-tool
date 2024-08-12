import pandas as pd
from db_connector import get_snowflake_connection  # Import the function from db_connector


class SnowflakeQueryExecutor:

    @staticmethod
    def execute_query(query):
        try:
            # Use the imported function to get a Snowflake connection
            conn = get_snowflake_connection()
            df = pd.read_sql(query, conn)
            conn.close()

            print("Data successfully loaded.")
            return df

        except Exception as e:
            print(f"Error loading data: {e}")
            return None
