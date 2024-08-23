import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from data_analytics.ad_spent_in_net_sales_per_category_region import PercOfNetSalesSpentInAdCase


@pytest.fixture
def ad_case():
    mock_conn = MagicMock()
    return PercOfNetSalesSpentInAdCase(mock_conn)


@patch('streamlit.selectbox')
@patch('streamlit.title')
@patch('streamlit.bar_chart')
@patch('streamlit.error')
def test_render_with_valid_selection(mock_error, mock_bar_chart, mock_title, mock_selectbox, ad_case):
    mock_title.return_value = None
    mock_bar_chart.return_value = None
    mock_error.return_value = None

    mock_selectbox.side_effect = ["US", "2023", "01"]

    data = [('Electronics', 20.0), ('Books', 15.5)]
    columns = ['CATEGORY', '% of net sales spent in ad']

    ad_case.load_sql_query = MagicMock(return_value='SELECT * FROM TABLE')
    ad_case.run_query = MagicMock(return_value=(data, columns))
    ad_case.data_to_df = MagicMock(
        return_value=pd.DataFrame({'CATEGORY': ['Electronics', 'Books'], '% of net sales spent in ad': [20.0, 15.5]})
    )

    ad_case.render()

    assert mock_selectbox.call_count == 3
    assert mock_selectbox.call_args_list == [
        (("Select a region:", ["select one option", "EU", "US", "CA", "UK", "AU", "JP", "MX"]), {'index': 0}),
        (("Select a year:", ["select one option", "2023", "2024"]), {'index': 0}),
        (("Select a month:",
          ["select one option", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]), {'index': 0}),
    ]

    region, year, month = ["US", "2023", "01"]
    year_month = year + month
    assert year_month == "202301"

    ad_case.load_sql_query.assert_called_once_with(region="US", year_month="202301")
    ad_case.run_query.assert_called_once_with('SELECT * FROM TABLE')

    mock_title.assert_called_once_with("% of Net Sales spent in advertisement per category")
    mock_bar_chart.assert_called_once()


@patch('streamlit.selectbox')
@patch('streamlit.title')
@patch('streamlit.error')
def test_render_with_missing_selection(mock_error, mock_title, mock_selectbox, ad_case):
    mock_title.return_value = None
    mock_error.return_value = None

    # test missing year
    mock_selectbox.side_effect = ["US", "select one option", "01"]

    ad_case.render()

    mock_error.assert_called_once_with("A region, a year and a month must be selected.")
    mock_title.assert_called_once()
    assert mock_selectbox.call_count == 3

    mock_error.reset_mock()
    mock_title.reset_mock()
    mock_selectbox.reset_mock()

    # test missing month
    mock_selectbox.side_effect = ["US", "2023", "select one option"]

    ad_case.render()

    mock_error.assert_called_once_with("A region, a year and a month must be selected.")
    mock_title.assert_called_once()
    assert mock_selectbox.call_count == 3
