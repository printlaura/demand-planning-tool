from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar


def filters_selection():
    asin = st.sidebar.text_input("Enter ASIN:", "")
    region = st.sidebar.selectbox("Select a region:",
                                  ["select one option", "EU", "US", "CA", "UK", "AU", "JP", "MX"], index=0)
    year = st.sidebar.multiselect("Select one or more years:", options=["2023", "2024"])

    return asin, region, year


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

        asin, region, year = filters_selection()
        if year:
            year_filter = f"and year(date) in ({', '.join(map(str, year))})"
        else:
            year_filter = ""

        if not asin or not region:
            st.error("Please enter ASIN and region.")
            return
        else:
            st.subheader("Units sold")
            st.write(f"{asin} - {region}")
            st.write("")
            st.write("")
            st.write("")
            self.units_sold(asin, region, year_filter)
            st.write("")
            st.write("")
            st.write("")
            st.subheader("Net sales")
            st.write(f"{asin} - {region}")
            st.write("")
            st.write("")
            self.net_sales(asin, region, year_filter)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader("Average sale price")
            st.write(f"{asin} - {region}")
            st.write("")
            st.write("")
            self.avg_sale_price(asin, region, year_filter)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader("Out of Stock days")
            st.write(f"{asin} - {region}")
            st.write("")
            st.write("")
            self.oos_days(asin, region, year_filter)

    def units_sold(self, asin, region, year_filter):
        query = self.load_sql_query(0, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="YEAR_MONTH", y="units sold")

    def net_sales(self, asin, region, year_filter):
        query = self.load_sql_query(1, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="YEAR_MONTH", y="net sales in EUR")

    def avg_sale_price(self, asin, region, year_filter):
        query = self.load_sql_query(2, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        if df["average sale price"].isnull().any():
            st.write("No sale price available for this item.")
        else:
            st.bar_chart(df, x="YEAR_MONTH", y="average sale price")

    def oos_days(self, asin, region, year_filter):
        query = self.load_sql_query(3, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="YEAR_MONTH", y="total Out of Stock days")
