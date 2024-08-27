import unittest
from unittest.mock import patch, MagicMock
from data_analytics.asin_region_report import AsinRegionCase, display_metric, filters_selection
import pandas as pd


def mock_visualization_data():
    return pd.DataFrame({
        "ASIN": "B07PGL2ZSL",
        "REGION": "EU",
        "year & month": ["01/2023", "02/2023"],
        "units sold": [100, 150],
        "net sales in EUR": [2000.50, 3500.75],
        "average sale price": [20.05, 22.75],
        "total Out of Stock days": [1, 0]
    })


class TestAsinRegionCase(unittest.TestCase):
    def setUp(self):
        self.mock_connection = MagicMock()
        self.case = AsinRegionCase(self.mock_connection)
        self.mock_data = mock_visualization_data()

    @patch('streamlit.plotly_chart')
    @patch('streamlit.expander')
    @patch('streamlit.warning')
    @patch('streamlit.write')
    def test_display_metric(self, mock_write, mock_warning, mock_expander, mock_plotly_chart):
        display_metric("Units sold", "Monthly units sold.", "Test ASIN", "Test Region", self.mock_data, "line",
                       "year & month", "units sold")

        mock_write.assert_called()
        mock_expander.assert_called_once()
        mock_plotly_chart.assert_called_once()

        display_metric("Average sale price", "Monthly average sale price.", "Test ASIN", "Test Region", self.mock_data,
                       "bar", "year & month", "average sale price")

        mock_expander.assert_called()
        mock_write.assert_called()
        mock_plotly_chart.assert_called()

    @patch('streamlit.plotly_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query', return_value="dummy_query")
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.data_to_df', return_value=mock_visualization_data())
    @patch('data_analytics.asin_region_report.filters_selection', return_value=("B07PGL2ZSL", "EU", ["2023"]))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.spinner')
    def test_render(self, mock_spinner, mock_button, mock_filters_selection, mock_data_to_df, mock_run_query,
                    mock_load_sql_query, mock_plotly_chart):

        mock_run_query.return_value = (self.mock_data.values.tolist(), list(self.mock_data.columns))
        self.case.render()
        mock_plotly_chart.assert_called()
