import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px
import re

from snowflake_query_executor import SnowflakeQueryExecutor
from db_connector import get_snowflake_connection
from sales_data_preprocessor import SalesDataPreprocessor
from lstm_model_handler import LSTMModelHandler
from data_analytics.categories_region_report import CategoriesPerRegionCase
from data_analytics.brands_region_report import BrandsPerRegionCase
from data_analytics.asin_region_report import AsinRegionCase

st.set_page_config(page_title="Demand Plan Tool", layout="wide")


def main():
    if "logged_in" not in st.session_state or st.session_state["logged_in"] is False:
        user_login()
    else:
        page_navigation()


def sanitize_input(input):
    return re.fullmatch(r'^[A-Za-z0-9_]{8,24}$', input) is not None


def user_login():
    st.title(" log in to DPT")

    with st.form("Login Form"):
        username = st.text_input("user name")
        password = st.text_input("password", type="password")
        submitted = st.form_submit_button("log in")

        if submitted:
            if not sanitize_input(username) or not sanitize_input(password):
                st.error("Invalid username or password.")
                return None

            if username and password:
                try:
                    connection = get_snowflake_connection(user=username, password=password)

                    if connection:
                        st.session_state["logged_in"] = True
                        st.session_state["sf_connection"] = connection
                        st.session_state["sf_user"] = username
                        st.session_state["current_page"] = "Home"
                        st.rerun()
                    else:
                        st.warning("Failed to log in. Either user name or password are incorrect.")

                except Exception as e:
                    st.error("Login failed. Either user name or password are incorrect.")
                    st.exception(e)


def page_navigation():
    current_page = st.session_state.get("current_page", "Home")

    if current_page == "Home":
        home()
    elif current_page in ["Forecasting", "Analytics"]:
        analytics_and_forecasting_sidebar()
        if current_page == "Forecasting":
            sales_predictor()
        elif current_page == "Analytics":
            analytics()


def analytics_and_forecasting_sidebar():
    toggle_page = "Analytics" if st.session_state["current_page"] == "Forecasting" else "Forecasting"
    if st.sidebar.button(f"Go to {toggle_page}"):
        st.session_state["current_page"] = toggle_page
        st.rerun()

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")

    if st.sidebar.button("Log out"):
        logout()


def home():
    st.title(f"welcome, {st.session_state['sf_user']}.")

    if st.button("Go to Forecasting"):
        st.session_state["current_page"] = "Forecasting"
        st.rerun()
    if st.button("Go to Analytics"):
        st.session_state["current_page"] = "Analytics"
        st.rerun()
    if st.button("Log out"):
        logout()
        st.rerun()


def logout():
    if "sf_connection" in st.session_state:
        st.session_state["sf_connection"].close()
        print("Database connection closed.")

    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def sales_predictor():
    st.header("Sales Predictor")

    asin = st.text_input("Enter ASIN:", "").strip().upper()
    region = st.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")

    if st.button("Get Forecast"):
        if not sanitize_input(asin) or not region:
            st.error("Please enter valid ASIN and region")
            return

        with st.spinner("Generating forecast. This might take a few seconds ..."):
            predictor(asin, region)


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

            if predictions == "Failed to predict. There is no sale price historical data for this ASIN and region.":
                st.error(predictions)
                return None

            forecast_data = [{
                'Date': datetime(year_today + (month_today + m - 1) // 12,
                                 (month_today + m - 1) % 12 + 1, 1).strftime('%B %Y'),
                'Units': sales
            } for m, sales in enumerate(predictions, start=1)]

            df_forecast = pd.DataFrame(forecast_data)
            render_predictions(df_forecast, asin, region)

        else:
            st.error("No data found for the given ASIN and region.")
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error("An error occurred during prediction: " + str(e))


def render_predictions(df, asin, region):
    st.write("")
    st.write("")
    st.subheader(f"Forecast for {asin} / {region}")
    st.write("")
    st.write(df.to_html(index=False), unsafe_allow_html=True)
    st.write("")
    fig = px.line(df, x='Date', y='Units')
    st.plotly_chart(fig)


def analytics():
    st.sidebar.title("Data Analytics")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.subheader("Select report")

    cases = {
        "select one option": "",
        "categories analytics": CategoriesPerRegionCase,
        "brands analytics": BrandsPerRegionCase,
        "ASIN analytics": AsinRegionCase,
    }

    case_choice = st.sidebar.selectbox("Click below to select a report", list(cases.keys()), index=0)

    if case_choice != "select one option":
        if "sf_connection" in st.session_state:
            case_class = cases[case_choice](connection=st.session_state["sf_connection"])
            case_class.render()
        else:
            st.error("Snowflake database connection not found.")
    else:
        return None


if __name__ == "__main__":
    main()
