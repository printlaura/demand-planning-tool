import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from data_analytics.ad_spent_in_net_sales_per_category_region import PercOfNetSalesSpentInAdCase


@pytest.fixture
def ad_case():
    return PercOfNetSalesSpentInAdCase()

@patch('streamlit.selectbox')
@patch('streamlit.title')
@patch('streamlit.bar_chart')
def test_render(mock_selectbox, mock_title, mock_bar_chart, ad_case):

    mock_selectbox.side_effect = ["US", "2023", "01"]
    mock_title.return_value = None
    mock_bar_chart.return_value = None

    data = [('Electronics', 20.0), ('Books', 15.5)]
    columns = ['CATEGORY', '% of net sales spent in ad']

    ad_case.load_sql_query = MagicMock(return_value='SELECT * FROM TABLE')
    ad_case.run_query = MagicMock(return_value=(data, columns))
    ad_case.data_to_df = MagicMock(
        return_value=pd.DataFrame({'CATEGORY': ['Electronics', 'Books'], '% of net sales spent in ad': [20.0, 15.5]})
    )

    ad_case.render()

    ad_case.load_sql_query.assert_called_once_with(region="US", year_month="202301")

    ad_case.run_query.assert_called_once_with('SELECT * FROM TABLE')

    mock_title.assert_called_once_with("% of Net Sales spent in advertisement per category")

    assert mock_selectbox.call_count == 3

    mock_selectbox.assert_called_with("Select a month:",
                                      ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
    mock_bar_chart.assert_called_once()
