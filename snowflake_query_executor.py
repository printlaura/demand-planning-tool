import pandas as pd


class SnowflakeQueryExecutor:

    @staticmethod
    def execute_query(query, conn):
        try:
            df = pd.read_sql(query, conn)

            print("Data successfully loaded.")
            return df

        except Exception as e:
            print(f"Error loading data: {e}")
            return None
