from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar
from datetime import datetime


def filters_selection():
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.selectbox("Select a year:", ["2023", "2024"], index=None, placeholder="...")
    month = st.sidebar.selectbox("Select a month:", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                                     "12"], index=None, placeholder="...")
    if month:
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


class CategoriesPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/categories/perc_of_sales_spent_in_ad_category.sql',
                          'data_analytics/queries/categories/units_sold_per_category_region.sql'],
                         conn=connection)

    def render(self):

        filters = filters_selection()
        if not filters:
            return None
        else:
            region, year, month, year_month, month_name = filters

        st.title(f"Categories - {region}")

        if not region or not year or not month:
            st.error("A region, a year and a month must be selected.")
            return
        else:
            display_metric("Units sold", f"{month_name} {year}", self.units_sold, region, year_month)
            display_metric("% of Net Sales spent in advertisement", f"{month_name} - {year}",
                                self.perc_of_sales_spent_in_ad, region, year_month)

    def perc_of_sales_spent_in_ad(self, region, year_month):
        query = self.load_sql_query(0, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="CATEGORY", y="% of net sales spent in ad")

    def units_sold(self, region, year_month):
        query = self.load_sql_query(1, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="CATEGORY", y="units sold")

