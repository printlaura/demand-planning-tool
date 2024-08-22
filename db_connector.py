import snowflake.connector
import logging
from config import SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA


def get_snowflake_connection(user, password, account=SNOWFLAKE_ACCOUNT, warehouse=SNOWFLAKE_WAREHOUSE,
                             database=SNOWFLAKE_DATABASE, schema=SNOWFLAKE_SCHEMA):
    logging.basicConfig(level=logging.INFO)

    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        logging.info("Successfully connected to Snowflake.")

        return conn

    except Exception as e:
        logging.error(f"Error connecting to SF: {e}")
        raise
