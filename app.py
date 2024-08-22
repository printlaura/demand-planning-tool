import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px
from snowflake_query_executor import SnowflakeQueryExecutor
from db_connector import get_snowflake_connection
from sales_data_preprocessor import SalesDataPreprocessor
from lstm_model_handler import LSTMModelHandler
from data_analytics.units_sold_case import UnitsSoldCase
from data_analytics.units_sold_per_category_region import UnitsSoldPerCategoryCase
from data_analytics.ad_spent_in_net_sales_per_category_region import PercOfNetSalesSpentInAdCase
from data_analytics.avg_price_per_asin_region import AvgPricePerASINCase

st.set_page_config(page_title="Demand Plan Tool", layout="wide")


def main():
    if "logged_in" not in st.session_state or st.session_state["logged_in"] is False:
        user_login()
    else:
        user_interaction()


def user_login():
    st.title("log in to DPT")

    with st.form("Login Form"):
        username = st.text_input("user name")
        password = st.text_input("password", type="password")
        submitted = st.form_submit_button("log in")

        if submitted and username and password:
            try:
                connection = get_snowflake_connection(user=username, password=password)

                if connection:
                    st.session_state["logged_in"] = True
                    st.session_state["sf_connection"] = connection
                    st.session_state["sf_user"] = username
                    st.rerun()
                else:
                    st.warning("Failed to log in. Either user name or password are incorrect.")

            except Exception as e:
                st.error("Failed to log in. Either user name or password are incorrect.")
                st.exception(e)


def user_interaction():
    st.title(f"welcome, {st.session_state['sf_user']}.")

    menu = ["Forecasting", "Analytics"]
    choice = st.sidebar.selectbox("Select option", menu)

    if choice == "Forecasting":
        sales_predictor()
    elif choice == "Analytics":
        analytics()


def sales_predictor():
    st.header("Sales Predictor")

    asin = st.text_input("Enter ASIN:", "")
    region_options = ["EU", "US", "CA", "UK", "AU", "JP", "MX"]
    region = st.selectbox("Select a region:", region_options)
    month_today = datetime.now().month
    year_today = datetime.now().year

    if st.button("Get Forecast"):
        if asin and region:
            predictor(asin, region)
        else:
            st.error("Please enter an ASIN and Region")


def predictor(asin, region):
    month_today = datetime.now().month
    year_today = datetime.now().year

    try:
        conn = st.session_state["sf_connection"]

        preprocessor = SalesDataPreprocessor(SnowflakeQueryExecutor, asin=asin, region=region)
        preprocessor.load_data(conn)

        df_preprocessed = preprocessor.preprocess_data()

        if not df_preprocessed.empty:
            model_handler = LSTMModelHandler()
            predictions = model_handler.predict(df_preprocessed)
            forecast_data = [{
                'Date': datetime(year_today + (month_today + m - 1) // 12,
                                 (month_today + m - 1) % 12 + 1, 1).strftime('%B %Y'),
                'Predicted sales in units': sales
            } for m, sales in enumerate(predictions, start=1)]

            df_forecast = pd.DataFrame(forecast_data)
            fig = px.line(df_forecast, x='Date', y='Predicted sales in units', title='Forecast')
            st.plotly_chart(fig)
        else:
            st.error("No data found for the given ASIN and Region.")
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error("An error occurred during prediction: " + str(e))


def analytics():
    st.title("Data Analytics")
    cases = {
        "Monthly units sold per ASIN & region": UnitsSoldCase,
        "Monthly units sold per category": UnitsSoldPerCategoryCase,
        "% of net sales spent in ads per category": PercOfNetSalesSpentInAdCase,
        "Average sale price per ASIN & region": AvgPricePerASINCase
    }
    case_choice = st.selectbox("Select analysis report", list(cases.keys()))
    if case_choice:
        case_class = cases[case_choice](connection=st.session_state["sf_connection"])
        case_class.render()


if __name__ == "__main__":
    main()
