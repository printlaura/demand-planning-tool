import os
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

if SNOWFLAKE_WAREHOUSE is None or SNOWFLAKE_SCHEMA is None or SNOWFLAKE_DATABASE is None or SNOWFLAKE_ACCOUNT is None:
    raise ValueError("Environment variables for SF credentials are not set.")
