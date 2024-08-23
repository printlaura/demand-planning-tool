from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


class PercOfNetSalesSpentInAdCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__('data_analytics/queries/perc_of_sales_spent_in_ad_category.sql', connection)
        self.connection = connection

    def render(self):
        st.title("% of Net Sales spent in advertisement per category")

        st.sidebar.write("")
        st.sidebar.write("")

        region = st.sidebar.selectbox("Select a region:",
                                      ["select one option", "EU", "US", "CA", "UK", "AU", "JP", "MX"],
                                        index=0)
        st.sidebar.write("")
        st.sidebar.write("")

        year = st.sidebar.selectbox("Select a year:", ["select one option", "2023", "2024"], index=0)
        month = st.sidebar.selectbox("Select a month:", ["select one option", "01", "02", "03", "04", "05", "06", "07",
                                                         "08", "09", "10","11", "12"], index=0)

        if region == "select one option" or year == "select one option" or month == "select one option":
            st.error("A region, a year and a month must be selected.")
            return

        else:
            year_month = year + month
            query = self.load_sql_query(region=region, year_month=year_month)
            data, columns = self.run_query(query)

            df = self.data_to_df(data, columns)

            st.bar_chart(df, x="CATEGORY", y="% of net sales spent in ad")
