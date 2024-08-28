import pytest
from unittest.mock import patch, Mock
from snowflake.connector.errors import DatabaseError
from db_connector import get_snowflake_connection

SNOWFLAKE_USER = 'test_user'
SNOWFLAKE_PASSWORD = 'test_password'
SNOWFLAKE_ACCOUNT = 'test_account'
SNOWFLAKE_WAREHOUSE = 'test_warehouse'
SNOWFLAKE_DATABASE = 'test_database'
SNOWFLAKE_SCHEMA = 'test_schema'


def test_get_snowflake_connection_success():

    with patch('snowflake.connector.connect') as mock_connect:
        mock_connection_instance = Mock()
        mock_connect.return_value = mock_connection_instance

        conn = get_snowflake_connection(
            SNOWFLAKE_USER,
            SNOWFLAKE_PASSWORD,
            SNOWFLAKE_ACCOUNT,
            SNOWFLAKE_WAREHOUSE,
            SNOWFLAKE_DATABASE,
            SNOWFLAKE_SCHEMA
        )

        assert conn == mock_connection_instance, "The connection object should be returned from the connect method."
        mock_connect.assert_called_once_with(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )


def test_get_snowflake_connection_failure():

    with patch('snowflake.connector.connect', side_effect=DatabaseError("Failed to connect")) as mock_connect:
        with pytest.raises(DatabaseError, match="Failed to connect"):
            get_snowflake_connection(
                SNOWFLAKE_USER,
                SNOWFLAKE_PASSWORD,
                SNOWFLAKE_ACCOUNT,
                SNOWFLAKE_WAREHOUSE,
                SNOWFLAKE_DATABASE,
                SNOWFLAKE_SCHEMA
            )

        mock_connect.assert_called_once_with(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
