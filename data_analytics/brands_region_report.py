from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar
from datetime import datetime


def filters_selection():
    region = st.sidebar.selectbox("Select a region:",
                                  ["select one option", "EU", "US", "UK", "JP"], index=0)
    year = st.sidebar.selectbox("Select a year:", ["select one option", "2023", "2024"], index=0)
    month = st.sidebar.selectbox("Select a month:", ["select one option", "01", "02", "03", "04", "05", "06", "07",
                                                     "08", "09", "10", "11", "12"], index=0)

    if month != "select one option":
        if int(year) == datetime.now().year and int(month) > datetime.now().month:
            st.write("The selected month is incorrect. Please select a previous date.")
            return []
        else:
            month_name = calendar.month_name[int(month)]
            year_month = year + month

        return region, year, month, year_month, month_name
    else:
        return []


class BrandsPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/brands/net_sales_per_brand_region.sql',
                          'data_analytics/queries/brands/units_sold_per_brand_region.sql'
                          ],
                         conn=connection)

    def render(self):
        region, year, month, year_month, month_name = filters_selection()

        st.title(f"Brands - {region}")

        if region == "select one option" or year == "select one option" or month == "select one option":
            st.error("A region, a year and a month must be selected.")
            return
        else:
            st.subheader("Net Sales")
            st.write(month_name, year)
            st.write("")
            st.write("")
            st.write("")
            self.net_sales(region, year_month)
            st.write("")
            st.write("")
            st.subheader("Units sold")
            st.write(month_name, year)
            st.write("")
            st.write("")
            st.write("")
            self.units_sold(region, year_month)

    def net_sales(self, region, year_month):
        query = self.load_sql_query(0, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="BRAND", y="net sales in EUR")

    def units_sold(self, region, year_month):
        query = self.load_sql_query(1, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="BRAND", y="units sold")
