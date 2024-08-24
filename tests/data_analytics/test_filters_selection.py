import unittest
from unittest.mock import patch
from datetime import datetime
from data_analytics.brands_region_report import filters_selection, BrandsPerRegionCase


class TestFiltersSelection(unittest.TestCase):

    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.write')
    def test_filters_selection_valid(self, mock_write, mock_selectbox):

        mock_selectbox.side_effect = ["US", "2023", "06"]

        expected_result = ("US", "2023", "06", "202306", "June")
        actual_result = filters_selection()

        self.assertEqual(expected_result, actual_result)
        mock_write.assert_not_called()

    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.write')
    def test_filters_selection_invalid_month(self, mock_write, mock_selectbox):

        future_month = (datetime.now().month + 1) % 12 or 12
        mock_selectbox.side_effect = ["US", str(datetime.now().year), f"{future_month:02}"]

        result = filters_selection()

        self.assertIsNone(result)
        mock_write.assert_called_once_with("The selected month is invalid. Please select a previous date.")

    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.write')
    def test_filters_selection_no_month(self, mock_write, mock_selectbox):

        mock_selectbox.side_effect = ["US", "2023", None]

        result = filters_selection()

        self.assertIsNone(result)
        mock_write.assert_not_called()
