import unittest
from unittest.mock import patch
from data_analytics.brands_region_report import filters_selection, BrandsPerRegionCase


class TestFiltersSelection(unittest.TestCase):

    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.write')
    def test_filters_selection_valid(self, mock_write, mock_selectbox):

        mock_selectbox.side_effect = ["US", "2023", "06"]

        expected_result = ("US", "2023", "06",)
        actual_result = filters_selection()

        self.assertEqual(expected_result, actual_result)
        mock_write.assert_not_called()


    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.write')
    def test_filters_selection_incomplete(self, mock_write, mock_selectbox):

        mock_selectbox.side_effect = ["US", "2023", None]

        result = filters_selection()

        assert result == (None, None, None)
        mock_write.assert_not_called()
