from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar


def filters_selection():
    asin = st.text_input("Enter ASIN:", "")

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

    return asin, region, year, month, year_month, month_name


class AsinRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/asin/units_sold_per_asin_region.sql',
                          'data_analytics/queries/asin/net_sales_per_asin_region.sql',
                          'data_analytics/queries/asin/avg_sale_price_asin_region.sql',
                          'data_analytics/queries/asin/oos_days_per_asin.sql'
                          ],
                         conn=connection)

    def render(self):
        st.title("ASIN")

        asin, region, year, month, year_month, month_name = filters_selection()

        if not asin or not region:
            st.error("Please enter ASIN and region.")
            return
        else:
            st.subheader("Units sold")
            st.write(region)
            self.units_sold(asin, region)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader("Net sales")
            st.write(region)
            st.write("")
            st.write("")
            self.net_sales(asin, region)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader("Average sale price")
            st.write(region)
            st.write("")
            st.write("")
            self.avg_sale_price(asin, region)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader("Out of Stock days")
            st.write(region)
            st.write("")
            st.write("")
            self.oos_days(asin, region)

    def units_sold(self, asin, region):
        query = self.load_sql_query(0, asin=asin, region=region)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="year_month", y="units sold")

    def net_sales(self, asin, region):
        query = self.load_sql_query(1, asin=asin, region=region)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="year_month", y="net sales in EUR")

    def avg_sale_price(self, asin, region):
        query = self.load_sql_query(2, asin=asin, region=region)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="year_month", y="average sale price")

    def oos_days(self, asin, region):
        query = self.load_sql_query(3, asin=asin, region=region)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="year_month", y="total Out of Stock days")
