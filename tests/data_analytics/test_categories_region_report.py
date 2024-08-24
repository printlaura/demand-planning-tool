import unittest
from unittest.mock import patch, MagicMock
from data_analytics.categories_region_report import CategoriesPerRegionCase, filters_selection


class TestCategoriesPerRegionCase(unittest.TestCase):

    @patch('data_analytics.categories_region_report.filters_selection', return_value=('US', '2024', '05'))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.title')
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    @patch('streamlit.bar_chart')
    def test_render_with_valid_filters(self, mock_bar_chart, mock_write, mock_subheader, mock_title, mock_button, mock_filters_selection):

        mock_connection = MagicMock()
        case = CategoriesPerRegionCase(mock_connection)

        case.perc_of_sales_spent_in_ad = MagicMock()
        case.units_sold = MagicMock()

        case.perc_of_sales_spent_in_ad.return_value = MagicMock()
        case.units_sold.return_value = MagicMock()

        case.render()

        mock_title.assert_called_once_with("Categories - US")
        mock_subheader.assert_any_call("% of net sales spent in advertisement")
        mock_write.assert_any_call("May 2024")
        case.perc_of_sales_spent_in_ad.assert_called_once_with("US", "202405")
        mock_subheader.assert_any_call("Units sold")
        case.units_sold.assert_called_once_with("US", "202405")

    @patch('data_analytics.categories_region_report.filters_selection', return_value=(None, None, None))
    @patch('streamlit.sidebar.button', return_value=False)
    @patch('streamlit.error')
    def test_render_without_filters(self, mock_error, mock_button, mock_filters_selection):

        mock_connection = MagicMock()
        case = CategoriesPerRegionCase(mock_connection)

        result = case.render()

        self.assertIsNone(result)
        mock_error.assert_not_called()

    @patch('data_analytics.categories_region_report.filters_selection', return_value=("US", "2024", None))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.title')
    @patch('streamlit.error')
    def test_render_with_missing_filters(self, mock_error, mock_title, mock_button, mock_filters_selection):

        mock_connection = MagicMock()
        case = CategoriesPerRegionCase(mock_connection)

        result = case.render()

        self.assertIsNone(result)
        mock_error.assert_called_once_with("Please select region, year and month.")