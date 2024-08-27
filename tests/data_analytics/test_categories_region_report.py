import pandas as pd
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from data_analytics.categories_region_report import CategoriesPerRegionCase


class TestCategoriesPerRegionCase(unittest.TestCase):

    def setUp(self):
        self.mock_connection = MagicMock()
        self.case = CategoriesPerRegionCase(self.mock_connection)

        self.df_units_sold = pd.DataFrame({
            'YEAR_MONTH': '202405',
            'REGION': 'US',
            'CATEGORY': ['Electronics', 'Books'],
            'units sold': [100, 150]
        })
        self.df_ad_spent = pd.DataFrame({
            'YEAR_MONTH': '202405',
            'REGION': 'US',
            'CATEGORY': ['Electronics', 'Books'],
            '% of net sales spent in ad': [20, 25]
        })

    @patch('data_analytics.categories_region_report.filters_selection', return_value=("US", "2024", "05"))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.subheader')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.error')
    @patch('streamlit.plotly_chart')
    def test_render_with_valid_filters(self, mock_plotly_chart, mock_error, mock_markdown, mock_title, mock_subheader,
                                       mock_button, mock_filters_selection):
        self.case.units_sold = MagicMock(return_value=self.df_units_sold)
        self.case.perc_of_sales_spent_in_ad = MagicMock(return_value=self.df_ad_spent)

        self.case.render()

        mock_title.assert_any_call("US / May 2024")
        self.case.units_sold.assert_called_once_with("US", "202405")
        self.case.perc_of_sales_spent_in_ad.assert_called_once_with("US", "202405")
        mock_plotly_chart.assert_called()

    @patch('data_analytics.categories_region_report.filters_selection', return_value=(None, None, None))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.error')
    def test_render_without_filters(self, mock_error, mock_button, mock_filters_selection):
        self.case.render()
        mock_error.assert_called_once_with("Please select region, year and month.")

    @patch('data_analytics.categories_region_report.filters_selection', return_value=("US", "2024", None))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.error')
    def test_render_with_missing_filters(self, mock_error, mock_button, mock_filters_selection):
        self.case.render()
        mock_error.assert_called_once_with("Please select region, year and month.")

    @patch('data_analytics.categories_region_report.filters_selection',
           return_value=("EU", str(datetime.now().year), str(datetime.now().month + 1)))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.error')
    def test_render_with_future_date_selection(self, mock_error, mock_button, mock_filters_selection):
        self.case.render()
        mock_error.assert_called_with("The selected date is invalid. Please select a previous date.")
