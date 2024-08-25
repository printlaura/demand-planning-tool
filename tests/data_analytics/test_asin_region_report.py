import unittest
from unittest.mock import patch, MagicMock
from data_analytics.asin_region_report import AsinRegionCase, display_metric
import pandas as pd


def mock_visualization_data():
    return pd.DataFrame({
        "YEAR_MONTH": ["202301", "202302"],
        "units sold": [100, 150],
        "net sales in EUR": [2000.50, 3500.75],
        "average sale price": [20.05, 22.75],
        "total Out of Stock days": [1, 0]
    })


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
    @patch('data_analytics.asin_region_report.AsinRegionCase.data_to_df')
    def test_units_sold_with_data(self, mock_data_to_df, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("202301", 100),
            ("202302", 150),
        ]
        sample_columns = ['YEAR_MONTH', 'units sold']
        df = pd.DataFrame(sample_data, columns=sample_columns)

        mock_run_query.return_value = (sample_data, sample_columns)
        mock_data_to_df.return_value = df

        self.case.units_sold("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_data_to_df.assert_called_once()
        mock_bar_chart.assert_called_once_with()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.data_to_df')
    def test_net_sales_with_data(self, mock_data_to_df, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("202301", 2000.50),
            ("202302", 3500.75),
        ]
        sample_columns = ['YEAR_MONTH', 'net sales in EUR']

        mock_run_query.return_value = (sample_data, sample_columns)
        mock_data_to_df.return_value = pd.DataFrame(sample_data, columns=sample_columns)

        self.case.net_sales("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_data_to_df.assert_called_once()
        mock_bar_chart.assert_called_once()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.data_to_df')
    def test_avg_sale_price_with_data(self, mock_data_to_df, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("202301", 20.05),
            ("202302", 22.75),
        ]
        sample_columns = ['YEAR_MONTH', 'average sale price']

        mock_run_query.return_value = (sample_data, sample_columns)
        mock_data_to_df.return_value = pd.DataFrame(sample_data, columns=sample_columns)

        self.case.avg_sale_price("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_data_to_df.assert_called_once()
        mock_bar_chart.assert_called_once()

    @patch('streamlit.bar_chart')
    @patch('data_analytics.asin_region_report.AsinRegionCase.load_sql_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.run_query')
    @patch('data_analytics.asin_region_report.AsinRegionCase.data_to_df')
    def test_oos_days_with_data(self, mock_data_to_df, mock_run_query, mock_load_sql_query, mock_bar_chart):
        sample_data = [
            ("202301", 5),
            ("202302", 3),
        ]
        sample_columns = ['YEAR_MONTH', 'total Out of Stock days']

        mock_run_query.return_value = (sample_data, sample_columns)
        mock_data_to_df.return_value = pd.DataFrame(sample_data, columns=sample_columns)

        self.case.oos_days("B07PGL2ZSL", "EU", "")

        mock_load_sql_query.assert_called_once()
        mock_run_query.assert_called_once()
        mock_data_to_df.assert_called_once()
        mock_bar_chart.assert_called_once()

    @patch('data_analytics.asin_region_report.filters_selection', return_value=("B07PGL2ZSL", "EU", ["2023", "2024"]))
    @patch('streamlit.sidebar.button', return_value=True)
    @patch('streamlit.title')
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    @patch('streamlit.spinner')
    @patch('data_analytics.asin_region_report.AsinRegionCase.units_sold')
    @patch('data_analytics.asin_region_report.AsinRegionCase.net_sales')
    @patch('data_analytics.asin_region_report.AsinRegionCase.avg_sale_price')
    @patch('data_analytics.asin_region_report.AsinRegionCase.oos_days')
    def test_render_with_valid_filters(self, mock_oos_days, mock_avg_sale_price, mock_net_sales, mock_units_sold,
                                       mock_spinner, mock_write, mock_subheader, mock_title, mock_button,
                                       mock_filters_selection):
        mock_oos_days.return_value = pd.DataFrame([{"YEAR_MONTH": "202301", "total Out of Stock days": 0}])
        mock_avg_sale_price.return_value = pd.DataFrame([{"YEAR_MONTH": "202301", "average sale price": 20.0}])
        mock_net_sales.return_value = pd.DataFrame([{"YEAR_MONTH": "202301", "net sales in EUR": 1000.0}])
        mock_units_sold.return_value = pd.DataFrame([{"YEAR_MONTH": "202301", "units sold": 50}])

        case = AsinRegionCase(self.mock_connection)
        case.render()

        mock_title.assert_called_once_with("ASIN")
        mock_subheader.assert_any_call("Units sold")
        mock_subheader.assert_any_call("Net sales")
        mock_subheader.assert_any_call("Average sale price")
        mock_subheader.assert_any_call("Out of Stock days")
        mock_units_sold.assert_called_once()
        mock_net_sales.assert_called_once()
        mock_avg_sale_price.assert_called_once()
        mock_oos_days.assert_called_once()

    def test_display_metric(self):

        with patch('streamlit.subheader') as mock_subheader, patch('streamlit.write') as mock_write, \
                patch('streamlit.bar_chart') as mock_bar_chart:

            display_metric("Units sold", "Test ASIN - Test Region", None, "bar", "YEAR_MONTH", "units sold")
            mock_write.assert_called_with("No Units sold data available for Test ASIN - Test Region.")
            mock_bar_chart.assert_not_called()

            mock_write.reset_mock()

            data = mock_visualization_data()
            display_metric("Units sold", "Test ASIN - Test Region", data, "bar", "YEAR_MONTH", "units sold")
            mock_bar_chart.assert_called_once()
            mock_write.assert_not_called()
