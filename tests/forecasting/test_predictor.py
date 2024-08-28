import unittest
from unittest.mock import patch, MagicMock
from forecasting.predictor import Predictor
from datetime import datetime
import pandas as pd


class TestPredictor(unittest.TestCase):

    def setUp(self):
        self.mock_connection = MagicMock()
        self.predictor = Predictor(connection=self.mock_connection)

    def test_sanitize_asin(self):
        valid_asin = "B00TEST123"
        invalid_asin = "B00TEST1234X"

        self.assertTrue(self.predictor.sanitize_asin(valid_asin))
        self.assertFalse(self.predictor.sanitize_asin(invalid_asin))

    @patch("forecasting.predictor.st.text_input")
    @patch("forecasting.predictor.st.selectbox")
    @patch("forecasting.predictor.st.button")
    @patch("forecasting.predictor.st")
    def test_render(self, mock_st, mock_button, mock_selectbox, mock_text_input):
        mock_text_input.return_value = "B00TEST123"
        mock_selectbox.return_value = "US"
        mock_button.return_value = True

        self.predictor.render()

        mock_st.markdown.assert_called()
        mock_st.text_input.assert_called_once_with("Enter ASIN:", "")
        mock_st.selectbox.assert_called_once_with("Select a region:", ["EU", "US", "UK", "JP"], index=None,
                                                  placeholder="...")
        mock_st.button.assert_called_once_with("Get Forecast")

    @patch("forecasting.predictor.st.spinner")
    @patch("forecasting.predictor.SalesDataPreprocessor")
    @patch("forecasting.predictor.LSTMModelHandler")
    @patch("forecasting.predictor.st.text_input")
    @patch("forecasting.predictor.st.selectbox")
    @patch("forecasting.predictor.st.button")
    def test_predict_and_render(self, mock_button, mock_selectbox, mock_text_input, mock_model_handler_cls,
                                mock_preprocessor_cls, mock_spinner):

        mock_text_input.return_value = "B00TEST123"
        mock_selectbox.return_value = "US"
        mock_button.return_value = True

        mock_spinner.return_value.__enter__.return_value = None

        mock_preprocessor = MagicMock()
        mock_preprocessor_cls.return_value = mock_preprocessor

        mock_model_handler = MagicMock()
        mock_model_handler_cls.return_value = mock_model_handler

        df_preprocessed = pd.DataFrame({'some_column': [1, 2, 3]})
        mock_preprocessor.preprocess_data.return_value = df_preprocessed

        predictions = [100, 200, 300, 400, 500, 600]
        mock_model_handler.predict.return_value = predictions

        self.predictor.render()

        mock_preprocessor.load_data.assert_called_with(self.mock_connection)
        mock_model_handler.predict.assert_called_with(df_preprocessed)
        mock_spinner.assert_called_once()

    @patch("forecasting.predictor.st")
    def test_render_predictions(self, mock_st):
        df = pd.DataFrame({
            'Date': [datetime(2023, i, 1).strftime('%B %Y') for i in range(1, 7)],
            'Units': [100, 200, 300, 400, 500, 600]
        })

        self.predictor.render_predictions(df, "B00TEST123", "US")

        mock_st.write.assert_any_call("---")
        mock_st.dataframe.assert_called_once()
        mock_st.plotly_chart.assert_called_once()
