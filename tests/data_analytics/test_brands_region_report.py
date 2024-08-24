import unittest
from unittest.mock import patch, MagicMock
from data_analytics.brands_region_report import BrandsPerRegionCase, filters_selection


class TestBrandsPerRegionCase(unittest.TestCase):

    @patch('data_analytics.brands_region_report.filters_selection', return_value=('US', '2023', '06', '202306', 'June'))
    @patch('streamlit.title')
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    @patch('streamlit.bar_chart')
    def test_render_with_valid_filters(self, mock_bar_chart, mock_write, mock_subheader, mock_title, mock_filters_selection):

        mock_connection = MagicMock()
        case = BrandsPerRegionCase(mock_connection)

        case.net_sales = MagicMock()
        case.units_sold = MagicMock()

        case.render()

        mock_title.assert_called_once_with("Brands - US")
        mock_subheader.assert_any_call("Net sales")
        mock_write.assert_any_call("June 2023")
        case.net_sales.assert_called_once_with('US', '202306')
        mock_subheader.assert_any_call("Units sold")
        case.units_sold.assert_called_once_with('US', '202306')

    @patch('data_analytics.brands_region_report.filters_selection', return_value=None)
    @patch('streamlit.title')
    @patch('streamlit.error')
    def test_render_without_filters(self, mock_error, mock_title, mock_filters_selection):

        mock_connection = MagicMock()
        case = BrandsPerRegionCase(mock_connection)

        result = case.render()

        self.assertIsNone(result)
        mock_error.assert_not_called()
