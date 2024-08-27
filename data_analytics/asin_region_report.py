import streamlit as st
import re
import plotly.express as px
import pandas as pd
from data_analytics.base_case import BaseAnalyticsCase


def filters_selection():
    asin = st.sidebar.text_input("Enter ASIN:", "").strip().upper()
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.multiselect("Select year(s):", ["2023", "2024"], default=[])

    if asin and region:
        return asin, region, year
    else:
        return None, None, None


def display_metric(subheader, description, asin, region, data, viz_type, x_axis, y_axis):
    st.write(f"#### {subheader}")

    if data is not None and subheader == "OOS days" and data["total Out of Stock days"].sum() == 0:
        st.warning("This item has never been Out of Stock.")
        return None

    if data is not None:
        st.write(description)

        data['date_order'] = pd.to_datetime(data[x_axis], format='%m/%Y')
        data = data.sort_values(by='date_order')
        data = data.drop(columns=['date_order', 'ASIN', 'REGION'])

        if viz_type == "line":
            with st.expander("see table"):
                st.dataframe(data, use_container_width=True)

            fig = px.line(data, x=x_axis, y=y_axis, text=y_axis)
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig)

            st.write("---")
            st.write("")
            st.write("")

        elif viz_type == "bar":
            with st.expander("see table"):
                st.dataframe(data, use_container_width=True)

            fig = px.bar(data, x=x_axis, y=y_axis, text=y_axis, color=x_axis)
            fig.update_layout(width=1000, height=550, showlegend=False)
            fig.update_traces(width=0.7, textposition='outside')
            st.plotly_chart(fig)

            st.write("---")
            st.write("")
            st.write("")
    else:
        st.write(f"No {subheader} data available for {asin} / {region}.")

    st.write("")
    st.write("")
    st.write("")


def validate_asin(asin):
    return re.fullmatch(r'^[A-Z0-9]{8,12}$', asin) is not None


class AsinRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/asin/units_sold_per_asin_region.sql',
                          'data_analytics/queries/asin/net_sales_per_asin_region.sql',
                          'data_analytics/queries/asin/avg_sale_price_asin_region.sql',
                          'data_analytics/queries/asin/oos_days_per_asin.sql'
                          ],
                         conn=connection)

    def render(self):
        asin, region, year = filters_selection()

        if st.sidebar.button("see report"):
            if not asin or not region:
                st.sidebar.error("Please enter ASIN and region.")
                return

            if not validate_asin(asin):
                st.sidebar.error("Invalid ASIN.")
                return None

            st.header(f"ASIN performance")
            st.write("---")
            st.subheader(f"{asin} / {region}")
            st.write("")
            st.write("")

            year_filter = ""
            if year:
                year_filter = f"and year(date) in ({', '.join(map(str, year))})"

            with st.spinner("Loading data..."):
                units_sold_data = self.units_sold(asin, region, year_filter)
                net_sales_data = self.net_sales(asin, region, year_filter)
                avg_sale_price_data = self.avg_sale_price(asin, region, year_filter)
                oos_days_data = self.oos_days(asin, region, year_filter)

                st.empty()

                display_metric("Units sold", "Monthly units sold.", asin, region, units_sold_data, "line",
                               "month & year", "units sold")
                display_metric("Net sales", "Monthly net sales.", asin, region, net_sales_data, "line",
                               "month & year", "net sales in EUR")
                display_metric("Average sale price", "Monthly average sale price.", asin, region, avg_sale_price_data,
                               "bar", "month & year", "average sale price")
                display_metric("OOS days", "Monthly count of Out of Stock days.", asin, region, oos_days_data,
                               "bar", "month & year", "total Out of Stock days")

    def units_sold(self, asin, region, year_filter):
        return self.query_data(0, asin, region, year_filter)

    def net_sales(self, asin, region, year_filter):
        return self.query_data(1, asin, region, year_filter)

    def avg_sale_price(self, asin, region, year_filter):
        return self.query_data(2, asin, region, year_filter)

    def oos_days(self, asin, region, year_filter):
        return self.query_data(3, asin, region, year_filter)

    def query_data(self, query_index, asin, region, year_filter):
        query = self.load_sql_query(query_index, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)
