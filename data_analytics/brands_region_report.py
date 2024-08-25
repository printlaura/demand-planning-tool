from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar
from datetime import datetime

""""
def filters_selection():
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.selectbox("Select a year:", ["2023", "2024"], index=None, placeholder="...")
    month = st.sidebar.selectbox("Select a month:", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                                     "12"], index=None, placeholder="...")
    if month and year:
        if int(year) == datetime.now().year and int(month) > datetime.now().month:
            st.write("The selected month is invalid. Please select a previous date.")
            return None
        else:
            month_name = calendar.month_name[int(month)]
            year_month = year + month

        return region, year, month, year_month, month_name
    else:
        return None


def display_metric(subheader, description, method, *method_args):
    st.subheader(subheader)
    st.write(description)
    st.write("")
    st.write("")
    method(*method_args)
    st.write("")
    st.write("")
"""


def filters_selection():
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.selectbox("Select a year:", ["2023", "2024"], index=None, placeholder="...")
    month = st.sidebar.selectbox("Select a month:", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                                     "12"], index=None, placeholder="...")
    if month and year and region:
        return region, year, month
    else:
        return None, None, None


def display_metric(subheader, description, data, viz_type, x_axis, y_axis):
    st.subheader(subheader)
    st.write(description)
    st.write("")
    st.write("")

    if data is not None:
        if viz_type == 'bar':
            st.bar_chart(data, x=x_axis, y=y_axis)
    else:
        st.write(f"No {subheader} data available for {description}.")

    st.write("")
    st.write("")


class BrandsPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/brands/net_sales_per_brand_region.sql',
                          'data_analytics/queries/brands/units_sold_per_brand_region.sql'
                          ],
                         conn=connection)

    def render(self):

        region, year, month = filters_selection()

        if st.sidebar.button("see report"):
            if not region or not year or not month:
                st.error("Please select region, year and month.")
                return

            if int(year) == datetime.now().year and int(month) > datetime.now().month:
                st.write("The selected month is invalid. Please select a previous date.")
                return

            month_name = calendar.month_name[int(month)]
            year_month = year + month

            st.title(f"Brands - {region}")

            with st.spinner("Loading data..."):
                units_sold_data = self.units_sold(region, year_month)
                net_sales_data = self.net_sales(region, year_month)

                st.empty()

                display_metric("Units sold", f"{month_name} {year}", units_sold_data, "bar", "BRAND", "units sold")
                display_metric("Net sales", f"{month_name} {year}", net_sales_data, "bar", "BRAND",
                               "net sales in EUR")

    def units_sold(self, region, year_month):
        query = self.load_sql_query(1, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)

    def net_sales(self, region, year_month):
        query = self.load_sql_query(0, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)
