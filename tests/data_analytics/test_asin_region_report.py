import unittest
from unittest.mock import patch, MagicMock
from data_analytics.asin_region_report import AsinRegionCase


class TestAsinRegionCase(unittest.TestCase):

    def setUp(self):
        self.mock_connection = MagicMock()
        self.case = AsinRegionCase(self.mock_connection)

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query', return_value=([], []))
    def test_units_sold_without_data(self, mock_run_query, mock_load_sql_query, mock_bar_chart):
        self.case.units_sold("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_bar_chart.assert_not_called()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    def test_units_sold_with_data(self, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("2023-01", 100),
            ("2023-02", 150),
        ]
        sample_columns = ['YEAR_MONTH', 'units sold']

        mock_run_query.return_value = (sample_data, sample_columns)
        self.case.units_sold("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_bar_chart.assert_called_once()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    def test_net_sales_with_data(self, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("2023-01", 2000.50),
            ("2023-02", 3500.75),
        ]
        sample_columns = ['YEAR_MONTH', 'net sales in EUR']

        mock_run_query.return_value = (sample_data, sample_columns)
        self.case.net_sales("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_bar_chart.assert_called_once()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    def test_avg_sale_price_with_data(self, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("2023-01", 20.05),
            ("2023-02", 22.75),
        ]
        sample_columns = ['YEAR_MONTH', 'average sale price']

        mock_run_query.return_value = (sample_data, sample_columns)
        self.case.avg_sale_price("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_bar_chart.assert_called_once()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    def test_oos_days_with_data(self, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("2023-01", 5),
            ("2023-02", 3),
        ]
        sample_columns = ['YEAR_MONTH', 'total Out of Stock days']

        mock_run_query.return_value = (sample_data, sample_columns)
        self.case.oos_days("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_bar_chart.assert_called_once()
