from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


def filters_selection():
    asin = st.sidebar.text_input("Enter ASIN:", "")
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.multiselect("Select year(s):", ["2023", "2024"], default=[])

    return asin, region, year


def display_metric(subheader, description, method, *method_args):
    st.subheader(subheader)
    st.write(description)
    st.write("")
    st.write("")
    method(*method_args)
    st.write("")
    st.write("")


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

        year_filter = ""
        if year:
            year_filter = f"and year(date) in ({', '.join(map(str, year))})"

        if not asin or not region:
            st.error("Please enter ASIN and region.")
            return
        else:
            display_metric("Units sold", f"{asin} - {region}", self.units_sold, asin, region, year_filter)
            display_metric("Net sales", f"{asin} - {region}", self.net_sales, asin, region, year_filter)
            display_metric("Average sale price", f"{asin} - {region}", self.avg_sale_price, asin, region,
                                year_filter)
            display_metric("Out of Stock days", f"{asin} - {region}", self.oos_days, asin, region, year_filter)

    def units_sold(self, asin, region, year_filter):
        query = self.load_sql_query(0, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            st.write("No units sold data available for this ASIN and region.")
            return

        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="YEAR_MONTH", y="units sold")

    def net_sales(self, asin, region, year_filter):
        query = self.load_sql_query(1, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            st.write("No sales data available for this ASIN and region.")
            return
        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="YEAR_MONTH", y="net sales in EUR")

    def avg_sale_price(self, asin, region, year_filter):
        query = self.load_sql_query(2, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            st.write("No price data available for this ASIN and region.")
            return
        df = self.data_to_df(data, columns)
        if df["average sale price"].isnull().any():
            st.write("No sale price available for this item.")
        else:
            st.bar_chart(df, x="YEAR_MONTH", y="average sale price")

    def oos_days(self, asin, region, year_filter):
        query = self.load_sql_query(3, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            st.write("No OOS data available for this ASIN and region.")
            return
        df = self.data_to_df(data, columns)
        if df["total Out of Stock days"].sum() == 0:
            st.write("This item has never been Out of Stock.")
        else:
            st.bar_chart(df, x="YEAR_MONTH", y="total Out of Stock days")
