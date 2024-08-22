from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


class PercOfNetSalesSpentInAdCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__('data_analytics/queries/perc_of_sales_spent_in_ad_category.sql', connection)
        self.connection = connection

    def render(self):
        st.title("% of Net Sales spent in advertisement per category")
        region = st.selectbox("Select a region:", ["EU", "US", "CA", "UK", "AU", "JP", "MX"])
        year = st.selectbox("Select a year:", ["2023", "2024"])
        month = st.selectbox("Select a month:",
                             ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        year_month = year + month

        query = self.load_sql_query(region=region, year_month=year_month)
        data, columns = self.run_query(query)

        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="CATEGORY", y="% of net sales spent in ad")
