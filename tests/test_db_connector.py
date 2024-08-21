import pytest
from unittest import mock
import logging
from ..db_connector import get_snowflake_connection
from snowflake.connector.errors import DatabaseError
import sys

sys.modules['config'] = mock.Mock()
from config import SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, \
    SNOWFLAKE_SCHEMA


@pytest.fixture
def mock_snowflake_connect(monkeypatch):

    mock_conn = mock.Mock()
    monkeypatch.setattr('snowflake.connector.connect', mock.Mock(return_value=mock_conn))

    return mock_conn


def test_get_snowflake_connection_success(mock_snowflake_connect):

    conn = get_snowflake_connection()

    assert conn is not None
    assert mock_snowflake_connect.called

    mock_snowflake_connect.assert_called_with(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )


def test_get_snowflake_connection_failure(monkeypatch):

    with mock.patch('snowflake.connector.connect') as mock_connect:
        mock_connect.side_effect = DatabaseError("Failed to connect")

        with mock.patch.object(logging, 'error') as mock_log_error:
            with pytest.raises(DatabaseError):
                get_snowflake_connection()
            assert mock_log_error.called
            mock_log_error.assert_called_with('Error connecting to Snowflake: Failed to connect')
