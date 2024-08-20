from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


class AdSpendsCase(BaseAnalyticsCase):
    def __init__(self):
        super().__init__('data_analytics/queries/ad_spend_per_unit_sold.sql')

    def render(self):
        st.title("Monthly advertisement spends per unit sold per ASIN & region")
        asin = st.text_input("Enter ASIN:", "").upper()
        region = st.selectbox("Select a region:", ["EU", "US", "CA", "UK", "AU", "JP", "MX"])
       # date_range = st.date_input("Select Date Range", [start_date, end_date])

        query = self.load_sql_query(asin=asin, region=region)
        data, columns = self.run_query(query)

        df = self.data_to_df(data, columns)
        st.dataframe(df)
        st.bar_chart(df.set_index("ASIN"))
