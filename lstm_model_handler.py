import numpy as np
import math
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import register_keras_serializable
from tensorflow.keras.layers import LSTM


import pickle


# custom LSTM class to remove an argument from the imported LSTM model.
# This is necessary because the keras version that the model was trained with, varies from the version used in this app.
@register_keras_serializable(package='Custom', name='LSTM')
class CustomLSTM(LSTM):
    def __init__(self, *args, **kwargs):
        kwargs.pop('time_major', None)  # remove time_major argument
        super().__init__(*args, **kwargs)


class LSTMModelHandler:

    def __init__(self, n_past=6):
        self.n_past = n_past
        self.models = []
        self.scalers_price = []
        self.scalers_units_sold = []

        for i in range(1, 7):
            model = load_model(f'models/model_rf_{i}.h5', compile=True, custom_objects={'LSTM': CustomLSTM})
            self.models.append(model)
            with open(f'scalers/price/scaler_price_rf_{i}.pkl', 'rb') as f:
                self.scalers_price.append(pickle.load(f))
            with open(f'scalers/units_sold/scaler_units_sold_rf_{i}.pkl', 'rb') as f:
                self.scalers_units_sold.append(pickle.load(f))

    def process_input(self, df):
        # scale values
        df[['PRICE']] = self.scalers_price[0].transform(df[['PRICE']])
        df[['UNITS_SOLD']] = self.scalers_units_sold[0].transform(df[['UNITS_SOLD']])

        df = df.astype(np.float32)

        # get n_past observations for model input
        sequence = df.tail(self.n_past).values

        # create a sequence for prediction
        sequence = sequence.reshape((1, self.n_past, df.shape[1]))

        if df['PRICE'].isnull().any():
            return None

        return sequence

    def predict(self, df):
        sequence = self.process_input(df)
        predictions = []

        if sequence is None:
            return "Failed to predict. There is no sale price historical data for this ASIN and region."

        for i in range(6):
            model = self.models[i]
            prediction = model.predict(sequence)
            prediction = self.scalers_units_sold[i].inverse_transform(prediction)
            predictions.append(prediction[0][0])

        return list(map(math.ceil, predictions))
