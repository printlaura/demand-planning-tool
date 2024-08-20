from analytics_cases.base_case import BaseAnalyticsCase
import streamlit as st


class UnitsSoldCase(BaseAnalyticsCase):
    def __init__(self):
        super().__init__('queries/units_sold_per_asin_region.sql')

    def render(self):
        st.title("Monthly units sold per ASIN & region")
        asin = st.text_input("Enter ASIN:", "").upper()
        region = st.selectbox("Select a region:", ["EU", "US", "CA", "UK", "AU", "JP", "MX"])
       # date_range = st.date_input("Select Date Range", [start_date, end_date])
        min_units_sold = st.slider("Minimum Units Sold", 0, 200, 100)

        query = self.load_sql_query().format(product=asin, region=region, min_units=min_units_sold)
        data = self.run_query(query)

        df = self.data_to_df(data)
        st.dataframe(df)
        st.bar_chart(df.set_index("ASIN"))
