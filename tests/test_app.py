import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import app


@pytest.fixture(scope='module')
def mock_snowflake_connection():
    with patch('app.get_snowflake_connection', return_value=MagicMock()) as mock_conn:
        yield mock_conn


def test_user_login_successful():
    with patch('app.st.text_input', side_effect=["test_user", "test_pass"]), \
            patch('app.st.form_submit_button', return_value=True), \
            patch('app.get_snowflake_connection', return_value="Dummy_Connection"), \
            patch.dict('app.st.session_state', {}, clear=True):
        app.user_login()

        assert app.st.session_state['logged_in'] == True
        assert 'sf_connection' in app.st.session_state
        assert app.st.session_state.get('sf_user') == "test_user"


def test_user_login_failure():
    with patch('app.st.text_input', side_effect=["wrong_user", "wrong_pass"]), \
            patch('app.st.form_submit_button', return_value=True), \
            patch('app.st.warning') as mock_warning, \
            patch('app.get_snowflake_connection', return_value=None), \
            patch.dict('app.st.session_state', {}, clear=True):
        app.user_login()

        assert not app.st.session_state.get('logged_in', False)
        mock_warning.assert_called_once()


def test_logout():
    with patch.dict('app.st.session_state', {'logged_in': True, 'sf_connection': MagicMock()}, clear=True):
        app.logout()

        assert 'logged_in' not in app.st.session_state
        assert 'sf_connection' not in app.st.session_state


def test_page_navigation_to_home():
    with patch.dict('app.st.session_state', {'logged_in': True, 'current_page': 'Home'}, clear=True), \
            patch('app.home') as mock_home:
        app.page_navigation()
        mock_home.assert_called_once()


def test_sales_predictor_without_input():
    with patch('app.st.text_input', return_value=None), \
            patch('app.st.selectbox', return_value="EU"), \
            patch('app.st.button', return_value=True), \
            patch('app.st.error') as mock_error:
        app.sales_predictor()
        mock_error.assert_called_once_with("Please enter ASIN and region")


def test_predictor_with_valid_data():
    mock_data = pd.DataFrame({'sales': [100, 200, 150]})

    with patch('app.SalesDataPreprocessor.load_data'), \
            patch('app.SalesDataPreprocessor.preprocess_data', return_value=mock_data), \
            patch('app.LSTMModelHandler.predict', return_value=[120, 180, 130]), \
            patch.dict('app.st.session_state', {'sf_connection': MagicMock()}, clear=True):
        app.predictor('test_asin', 'EU')


def test_analytics_selection_valid():
    with patch('app.st.sidebar.selectbox', return_value="ASIN analytics"), \
            patch('app.AsinRegionCase.render'), \
            patch.dict('app.st.session_state', {'sf_connection': MagicMock()}, clear=True):
        app.analytics()
