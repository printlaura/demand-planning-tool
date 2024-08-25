from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import plotly.express as px
import calendar
from datetime import datetime


def filters_selection():
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.selectbox("Select a year:", ["2023", "2024"], index=None, placeholder="...")
    month = st.sidebar.selectbox("Select a month:", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                                     "12"], index=None, placeholder="...")
    if month and year and region:
        return region, year, month
    else:
        return None, None, None


def display_metric(subheader, description, data, viz_type, x_axis, y_axis):
    st.subheader(subheader)
    st.write(description)

    if data is not None:
        if viz_type == "bar":
            fig = px.bar(data, x=x_axis, y=y_axis, color=x_axis)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title='% of net sales')
            st.plotly_chart(fig)
            st.write("")
            st.write("")

        if viz_type == "pie":
            fig = px.pie(data, names=x_axis, values=y_axis)
            fig.update_layout(width=800, height=600, legend=dict(font=dict(size=14)))
            st.write("Click or unclick Category names to display specific values.")
            st.plotly_chart(fig)
            st.write("")
            st.write("")
    else:
        st.write(f"No {subheader} data available for {description}.")


class CategoriesPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/categories/units_sold_per_category_region.sql',
                          'data_analytics/queries/categories/perc_of_sales_spent_in_ad_category.sql'],
                         conn=connection)

    def render(self):
        region, year, month = filters_selection()

        if st.sidebar.button("see report"):
            if not region or not year or not month:
                st.error("Please select region, year and month.")
                return

            if int(year) == datetime.now().year and int(month) > datetime.now().month:
                st.error("The selected month is invalid. Please select a previous date.")
                return

            month_name = calendar.month_name[int(month)]
            year_month = year + month

            st.title(f"Categories - {region}")
            st.write("")
            st.write("")

            with st.spinner("Loading data..."):
                units_sold_data = self.units_sold(region, year_month)
                net_sales_data = self.perc_of_sales_spent_in_ad(region, year_month)

                st.empty()

                display_metric("Units sold", f"{month_name} {year}", units_sold_data, "pie", "CATEGORY", "units sold")
                display_metric("% of net sales spent in advertisement", f"{month_name} {year}", net_sales_data, "bar",
                               "CATEGORY",
                               "% of net sales spent in ad")

    def units_sold(self, region, year_month):
        return self.query_data(0, region, year_month)

    def perc_of_sales_spent_in_ad(self, region, year_month):
        return self.query_data(1, region, year_month)

    def query_data(self, query_index, region, year_month):
        query = self.load_sql_query(query_index, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)
