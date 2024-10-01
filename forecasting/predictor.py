import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from .sales_data_preprocessor import SalesDataPreprocessor
from .lstm_model_handler import LSTMModelHandler
from snowflake_query_executor import SnowflakeQueryExecutor
import re
import logging
import numpy as np


class Predictor:
    def __init__(self, connection):
        self.connection = connection

    def sanitize_asin(self, asin):
        return re.fullmatch(r'^[A-Z0-9_]{10}$', asin) is not None

    def render(self):
        st.markdown(f"<h1 style='text-align: right; font-size: 50px; color: #983352;'>Sales Predictor</h1>",
                    unsafe_allow_html=True)
        st.write("---")
        st.markdown(
            f"<p style='font-size: 20px'>Enter ASIN & region to get sales predictions for the upcoming six months. </p>",
            unsafe_allow_html=True)
        st.write("")
        st.write("")

        asin = st.text_input("Enter ASIN:", "").strip().upper()
        region = st.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
        st.write("")

        if st.button("Get Forecast"):
            if not self.sanitize_asin(asin) or not region:
                st.error("Please enter valid ASIN and region")
                return

            with st.spinner("Generating forecast. This might take a few seconds ..."):
                self.predict_and_render(asin, region)

    def predict_and_render(self, asin, region):
        month_today = datetime.now().month
        year_today = datetime.now().year

        try:
            preprocessor = SalesDataPreprocessor(SnowflakeQueryExecutor, asin=asin, region=region)
            preprocessor.load_data(self.connection)

            df_preprocessed = preprocessor.preprocess_data()

            if not df_preprocessed.empty:
                model_handler = LSTMModelHandler()
                predictions = model_handler.predict(df_preprocessed)

                if predictions == "Failed to predict. There is no sale price historical data for this ASIN and region.":
                    st.error(predictions)
                    return None

                # create df from list of dicts with predicted data
                forecast_data = [{
                    'Date': datetime(year_today + (month_today + m - 1) // 12,
                                     (month_today + m - 1) % 12 + 1, 1).strftime('%B %Y'),
                    'Units': sales
                } for m, sales in enumerate(predictions, start=1)]

                df_forecast = pd.DataFrame(forecast_data)
                self.render_predictions(df_forecast, asin, region)

            else:
                st.error("No data found for the given ASIN and region.")
        except ValueError as e:
            st.error(f"Unable to get prediction for given ASIN and region. Try a different combination of ASIN & region. "
                     f"If the issue persists, please contact the Data team.")
            logging.error(f"Failed to get prediction: {str(e)}")
        except Exception as e:
            st.error("An error occurred during prediction.")
            logging.error(f"An error occurred during prediction: {str(e)}.")

    def render_predictions(self, df, asin, region):
        st.write("")
        st.write("")

        with st.container():
            st.write("")
            st.write("---")
            st.write(f"### Forecast for **{asin}** / **{region}**")
            st.write("")

            df_pivot = df.T
            df_pivot.columns = df_pivot.iloc[0]
            df_pivot = df_pivot.drop(df_pivot.index[0])

            st.dataframe(df_pivot, use_container_width=True)

            st.write("")

            fig = px.line(df, x='Date', y='Units')
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig, use_container_width=True)