from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar


def filters_selection():
    region = st.sidebar.selectbox("Select a region:",
                                  ["select one option", "EU", "US", "CA", "UK", "AU", "JP", "MX"], index=0)
    year = st.sidebar.selectbox("Select a year:", ["select one option", "2023", "2024"], index=0)
    month = st.sidebar.selectbox("Select a month:", ["select one option", "01", "02", "03", "04", "05", "06", "07",
                                                     "08", "09", "10", "11", "12"], index=0)
    year_month = year + month

    if month == "select one option":
        month_name = None
    else:
        month_name = calendar.month_name[int(month)]

    return region, year, month, year_month, month_name


class CategoriesPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/categories/perc_of_sales_spent_in_ad_category.sql',
                          'data_analytics/queries/categories/units_sold_per_category_region.sql'],
                         conn=connection)

    def render(self):
        st.title("Categories")

        region, year, month, year_month, month_name = filters_selection()

        if region == "select one option" or year == "select one option" or month == "select one option":
            st.error("A region, a year and a month must be selected.")
            return
        else:
            st.subheader("% of Net Sales spent in advertisement")
            st.write(month_name, year)
            self.perc_of_sales_spent_in_ad(region, year_month)
            st.sidebar.write("")
            st.sidebar.write("")
            st.subheader("Units sold")
            st.sidebar.write("")
            st.write(month_name, year)
            st.sidebar.write("")
            self.units_sold(region, year_month)

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
