from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


class AvgPricePerASINCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__('data_analytics/queries/avg_sale_price_asin_region.sql')
        self.connection = connection

    def render(self):
        st.title("Average price per ASIN")

        asin = st.text_input("Enter ASIN:", "").upper()
        region = st.selectbox("Select a region:", ["EU", "US", "CA", "UK", "AU", "JP", "MX"])

        query = self.load_sql_query(asin=asin, region=region)
        data, columns = self.run_query(query)

        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="YEAR_MONTH", y="average sale price")
