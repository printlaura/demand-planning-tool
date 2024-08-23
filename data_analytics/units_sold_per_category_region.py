from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


class UnitsSoldPerCategoryCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__('data_analytics/queries/units_sold_per_category_region.sql', connection)
        self.connection = connection

    def render(self):
        st.title("Monthly units sold per category")

        st.sidebar.write("")
        st.sidebar.write("")

        region = st.sidebar.selectbox("Select a region:", ["select one option", "EU", "US", "CA", "UK", "AU", "JP",
                                                           "MX"], index=0)

        query = self.load_sql_query(region=region)
        data, columns = self.run_query(query)

        df = self.data_to_df(data, columns)
        st.bar_chart(df, x="CATEGORY", y="% of net sales spent in ad") #change axes
