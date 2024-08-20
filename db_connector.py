import snowflake.connector
import logging
from config import SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, \
    SNOWFLAKE_SCHEMA


def get_snowflake_connection():
    logging.basicConfig(level=logging.INFO)

    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        logging.info("Successfully connected to Snowflake.")

        return conn

    except Exception as e:
        logging.error(f"Error connecting to SF: {e}")
        raise
