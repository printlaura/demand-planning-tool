import pytest
from unittest.mock import patch, MagicMock
import app


@pytest.fixture(scope='module')
def mock_snowflake_connection():
    with patch('app.get_snowflake_connection', return_value=MagicMock()) as mock_conn:
        yield mock_conn


def test_sanitize_input_valid():
    assert app.sanitize_input("ValidInput123") == True


def test_sanitize_input_invalid():
    assert app.sanitize_input("Invalid!Input") == False


def test_sanitize_asin_valid():
    assert app.sanitize_asin("B000123456") == True


def test_sanitize_asin_invalid():
    assert app.sanitize_asin("123!ASIN@") == False


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
    with patch.dict('app.st.session_state', {'logged_in': True, 'current_page': "Home"}, clear=True), \
            patch('app.home') as mock_home:
        app.page_navigation()
        mock_home.assert_called_once()


def test_page_navigation_to_forecasting():
    with patch.dict('app.st.session_state', {'logged_in': True, 'current_page': "Forecasting"}, clear=True), \
            patch('app.sales_predictor') as mock_forecasting:
        app.page_navigation()
        mock_forecasting.assert_called_once()


def test_page_navigation_to_analytics():
    with patch.dict('app.st.session_state', {'logged_in': True, 'current_page': "Analytics"}, clear=True), \
            patch('app.analytics') as mock_analytics:
        app.page_navigation()
        mock_analytics.assert_called_once()


def test_analytics_selection_valid():
    with patch('app.st.sidebar.selectbox', return_value="ASIN performance"), \
            patch('app.AsinRegionCase.render'), \
            patch.dict('app.st.session_state', {'sf_connection': MagicMock()}, clear=True):
        app.analytics()


def test_analytics_selection_invalid():
    with patch('app.st.sidebar.selectbox', return_value="select one option"), \
            patch('app.st.error') as mock_error:
        app.analytics()
        mock_error.assert_not_called()
