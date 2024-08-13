import pandas as pd
import streamlit as st
from datetime import datetime
from data.sales_data_preprocessor import SalesDataPreprocessor
from lstm_model_handler import LSTMModelHandler
import plotly.express as px
from snowflake_query_executor import SnowflakeQueryExecutor


st.set_page_config(page_title="Demand Plan Tool", layout="wide")

def main():
    st.title("Demand Plan Tool")
    menu = ["Sales Forecast", "Analytics"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Sales Forecast":
        st.header("Sales Forecast")

        asin = st.text_input("Enter ASIN:", "")
        region_options = ["EU", "US", "CA", "UK", "AU", "JP", "MX"]
        region = st.selectbox("Select a region:", region_options)

        # df = pd.read_csv('FOR_TESTING_APP.csv')

        month_today = datetime.now().month
        year_today = datetime.now().year
        if st.button("Get Forecast"):
            if asin and region:
                preprocessor = SalesDataPreprocessor(SnowflakeQueryExecutor(), asin, region)
                preprocessor.load_data()
                df_preprocessed = preprocessor.preprocess_data()

                if not df_preprocessed.empty:
                    model_handler = LSTMModelHandler()
                    predictions = model_handler.predict(df_preprocessed)

                    forecast_data = []

                    for month, sales in enumerate(predictions, start=1):
                        total_months = month_today + month
                        predicted_month = (total_months - 1) % 12 + 1
                        predicted_year = year_today + (total_months - 1) // 12

                        predicted_date = datetime(predicted_year, predicted_month, 1)
                        forecast_data.append({'Date': predicted_date.strftime('%B %Y'), 'Predicted units sold': sales})

                    df_forecast = pd.DataFrame(forecast_data)

                    # visualize
                    st.subheader("Forecasted units sold")
                    fig = px.line(df_forecast, x='Date', y='Predicted units sold', title='Sales Forecast')
                    fig.update_layout(xaxis_title='Date', yaxis_title='Predicted units sold', template='plotly_white')
                    st.plotly_chart(fig)

                    st.subheader("Forecasted units sold")
                    st.write(df_forecast.to_html(index=False), unsafe_allow_html=True)

                else:
                    st.error("No data found for the given ASIN and Region.")
            else:
                st.error("Please enter an ASIN and Region")


"""
    elif choice == "Analytics":
        st.header("Data Analytics")
"""

if __name__ == '__main__':
    main()
