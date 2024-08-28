import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, mock_open
from forecasting.lstm_model_handler import LSTMModelHandler


@pytest.fixture
def lstm_model_handler():
    with patch('forecasting.lstm_model_handler.load_model') as mock_load_model, \
            patch('builtins.open', mock_open()) as mock_file, \
            patch('pickle.load') as mock_pickle_load:

        model_mock = Mock(name='model_mock')
        model_mock.predict.return_value = np.array([[1.0]])
        mock_load_model.return_value = model_mock

        scaler_mock = Mock(name='scaler_mock')
        scaler_mock.transform.side_effect = lambda x: x
        scaler_mock.inverse_transform.side_effect = lambda x: x
        mock_pickle_load.return_value = scaler_mock

        handler = LSTMModelHandler()

        for _ in range(6):
            handler.models.append(model_mock)
            handler.scalers_price.append(scaler_mock)
            handler.scalers_units_sold.append(scaler_mock)

        yield handler


def test_process_input(lstm_model_handler):
    df = pd.DataFrame({
        'PRICE': [10, 20, 20, 30, 20, 20],
        'UNITS_SOLD': [1, 2, 3, 4, 5, 6]
    })

    sequence = lstm_model_handler.process_input(df)

    assert sequence.shape == (1, 6, 2), "Processed sequence shape should match expected shape."


def test_predict(lstm_model_handler):
    extra_columns = [
        "CATEGORY_Apparel", "CATEGORY_Art Supplies, Books & Music", "CATEGORY_Beauty & Wellness",
        "CATEGORY_Electronics Others", "CATEGORY_Gadgets & Tech", "CATEGORY_Hardware",
        "CATEGORY_Health Care", "CATEGORY_Home Appliance", "CATEGORY_Home Furnishing",
        "CATEGORY_Home Softgoods", "CATEGORY_Household Chemicals", "CATEGORY_Kids & Baby",
        "CATEGORY_Kitchen & Dining", "CATEGORY_Lighting", "CATEGORY_Nutrition",
        "CATEGORY_Office Organization & Furnishing", "CATEGORY_Pet Supplies", "CATEGORY_Smartphone",
        "CATEGORY_Sports & Outdoor", "CATEGORY_Tablet & eReaders", "MONTH_7", "MONTH_8", "MONTH_9", "MONTH_10",
        "MONTH_11", "MONTH_12"
    ]

    df = pd.DataFrame(0, index=range(6), columns=extra_columns)
    df["CATEGORY_Apparel"] = 1

    df["MONTH_1"] = [1, 0, 0, 0, 0, 0]
    df["MONTH_2"] = [0, 1, 0, 0, 0, 0]
    df["MONTH_3"] = [0, 0, 1, 0, 0, 0]
    df["MONTH_4"] = [0, 0, 0, 1, 0, 0]
    df["MONTH_5"] = [0, 0, 0, 0, 1, 0]
    df["MONTH_6"] = [0, 0, 0, 0, 0, 1]
    df["PRICE"] = [10, 20, 20, 30, 20, 20]
    df["UNITS_SOLD"] = [1, 2, 3, 4, 5, 6]

    predictions = lstm_model_handler.predict(df)

    assert len(predictions) == 6, "Should predict a value for each model."
