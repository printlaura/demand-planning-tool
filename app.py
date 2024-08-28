import logging

import streamlit as st
import re

from db_connector import get_snowflake_connection
from forecasting.predictor import Predictor
from data_analytics.categories_region_report import CategoriesPerRegionCase
from data_analytics.brands_region_report import BrandsPerRegionCase
from data_analytics.asin_region_report import AsinRegionCase

st.set_page_config(page_title="Demand Plan Tool", layout="wide")


def main():
    try:
        if "logged_in" not in st.session_state or st.session_state["logged_in"] is False:
            user_login()
        else:
            page_navigation()
    except Exception as e:
        st.error("Error.")
        st.warning("Try refreshing the page.")


def sanitize_input(input):
    return re.fullmatch(r'^[A-Za-z0-9_]{8,24}$', input) is not None


def sanitize_asin(asin):
    return re.fullmatch(r'^[A-Z0-9_]{10}$', asin) is not None


def user_login():
    st.markdown(f"<h1 style='text-align: right; margin-bottom: 80px; margin-top: 50px; "
                f"font-size: 75px'>Demand Plan Tool</h1>", unsafe_allow_html=True)

    with st.form("Login Form"):
        username = st.text_input("user name")
        st.write("")
        password = st.text_input("password", type="password").strip()
        st.write("")
        st.write("")
        submitted = st.form_submit_button("log in")

        if submitted:
            if not sanitize_input(username) or not password:
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
                    logging.error("An error occurred: %s", str(e))


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
    if st.sidebar.button("Log out"):
        logout()

    st.sidebar.write("---")
    st.sidebar.write("")

    if st.sidebar.button("Home"):
        st.session_state["current_page"] = "Home"
        st.rerun()
        home()

    toggle_page = "Analytics" if st.session_state["current_page"] == "Forecasting" else "Forecasting"
    if st.sidebar.button(f"Go to {toggle_page}"):
        st.session_state["current_page"] = toggle_page
        st.rerun()


def home():
    username = st.session_state['sf_user']

    # styling to make buttons bigger
    st.markdown("""
         <style>
         .stButton button {
             font-size: 20px;
             padding: 30px 45px;
         }
         </style>
         """, unsafe_allow_html=True)

    col_top_left, col_top_right = st.columns([1, 4])

    with col_top_left:
        if st.button("Log out"):
            logout()
            st.rerun()

    st.markdown(f"<h1 style='text-align: right; color: #983352;'>Welcome, {username}.</h1>", unsafe_allow_html=True)

    st.write("---")
    st.write("")
    st.write("")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col2:
        if st.button("Go to Forecasting"):
            st.session_state["current_page"] = "Forecasting"
            st.rerun()

    with col3:
        if st.button("Go to Analytics"):
            st.session_state["current_page"] = "Analytics"
            st.rerun()


def logout():
    if "sf_connection" in st.session_state:
        st.session_state["sf_connection"].close()
        print("Database connection closed.")

    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def sales_predictor():
    if "sf_connection" not in st.session_state:
        st.error("Database connection not found.")
        return

    predictor = Predictor(st.session_state["sf_connection"])
    predictor.render()


def analytics():
    st.sidebar.title("Data Analytics")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.subheader("Select report")

    cases = {
        "select one option": "",
        "Categories overview": CategoriesPerRegionCase,
        "Brands overview": BrandsPerRegionCase,
        "ASIN performance": AsinRegionCase,
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
