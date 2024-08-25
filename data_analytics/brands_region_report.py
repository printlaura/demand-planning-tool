from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st
import calendar
from datetime import datetime
import plotly.express as px


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
    st.write("")
    st.write("")

    if data is not None:
        if viz_type == 'bar':
            st.bar_chart(data, x=x_axis, y=y_axis)

        if viz_type == "pie":
            fig = px.pie(data, names=x_axis, values=y_axis)
            fig.update_layout(width=800, height=600, legend=dict(font=dict(size=14)))
            st.write("Click or unclick brand names to filter out brands.")
            st.plotly_chart(fig)
            st.write("")
            st.write("")
    else:
        st.write(f"No {subheader} data available for {description}.")

    st.write("")
    st.write("")


class BrandsPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/brands/units_sold_per_brand_region.sql',
                          'data_analytics/queries/brands/net_sales_per_brand_region.sql',
                          ],
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

            st.title(f"Brands - {region}")

            with st.spinner("Loading data..."):
                units_sold_data = self.units_sold(region, year_month)
                net_sales_data = self.net_sales(region, year_month)

                st.empty()

                display_metric("Units sold", f"{month_name} {year}", units_sold_data, "bar", "BRAND", "units sold")
                display_metric("Net sales", f"{month_name} {year}", net_sales_data, "pie", "BRAND",
                               "net sales in EUR")

    def units_sold(self, region, year_month):
        return self.query_data(0, region, year_month)

    def net_sales(self, region, year_month):
        return self.query_data(1, region, year_month)

    def query_data(self, query_index, region, year_month):
        query = self.load_sql_query(query_index, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)
