import unittest
from datetime import datetime
import pandas as pd
from unittest.mock import patch, MagicMock
from data_analytics.brands_region_report import BrandsPerRegionCase, filters_selection


class TestBrandsPerRegionCase(unittest.TestCase):

    @patch('data_analytics.brands_region_report.filters_selection', return_value=('US', '2023', '06'))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.title')
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    @patch('streamlit.plotly_chart')
    def test_render_with_valid_filters(self, mock_plotly_chart, mock_write, mock_subheader, mock_title, mock_button,
                                       mock_filters_selection):

        mock_net_sales_data = pd.DataFrame({
            'BRAND': ['A', 'B', 'C'],
            'net sales in EUR': [1000, 1500, 2000],
            'YEAR_MONTH': ["202306", "202307", "202308"],
            'REGION': ["US", "US", "US"]
        })

        mock_units_sold_data = pd.DataFrame({
            'BRAND': ['A', 'B', 'C'],
            'units sold': [100, 150, 200],
            'YEAR_MONTH': ["202306", "202307", "202308"],
            'REGION': ["US", "US", "US"]
        })

        case = BrandsPerRegionCase(MagicMock())

        case.net_sales = MagicMock(return_value=mock_net_sales_data)
        case.units_sold = MagicMock(return_value=mock_units_sold_data)

        case.render()

        mock_write.assert_any_call("#### Net sales")
        case.net_sales.assert_called_once_with("US", "202306")
        mock_write.assert_any_call("#### Units sold")
        case.units_sold.assert_called_once_with("US", "202306")

    @patch('data_analytics.brands_region_report.filters_selection', return_value=(None, None, None))
    @patch('streamlit.sidebar.button', return_value=False)
    @patch('streamlit.error')
    def test_render_without_filters(self, mock_error, mock_button, mock_filters_selection):
        mock_connection = MagicMock()
        case = BrandsPerRegionCase(mock_connection)

        result = case.render()

        self.assertIsNone(result)
        mock_error.assert_not_called()

    @patch('data_analytics.brands_region_report.filters_selection', return_value=("US", "2023", None))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.title')
    @patch('streamlit.error')
    def test_render_with_missing_filters(self, mock_error, mock_title, mock_button, mock_filters_selection):
        mock_connection = MagicMock()
        case = BrandsPerRegionCase(mock_connection)

        result = case.render()

        self.assertIsNone(result)
        mock_error.assert_called_once_with("Please select region, year and month.")

    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.sidebar.button')
    @patch('streamlit.error')
    def test_render_with_future_date_selection(self, mock_error, mock_button, mock_selectbox):
        mock_selectbox.side_effect = ["EU", str(datetime.now().year), str(datetime.now().month + 1)]
        mock_button.return_value = True

        mock_connection = MagicMock()
        case = BrandsPerRegionCase(mock_connection)

        case.render()

        mock_error.assert_called_with("The selected date is invalid. Please select a previous date.")
