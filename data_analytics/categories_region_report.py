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


def display_metric(subheader, description, month, year, data, viz_type, x_axis, y_axis):
    st.write(f"#### {subheader}")

    if data is not None:
        st.write(description)

        if viz_type == "bar":
            with st.expander("see table"):
                df = data.drop(columns=['YEAR_MONTH', 'REGION'])
                st.dataframe(df, use_container_width=True)

            fig = px.bar(data, x=x_axis, y=y_axis, text=y_axis, color=x_axis)
            fig.update_layout(width=1000, height=550, showlegend=False, xaxis_title="", yaxis_title=f"{y_axis}")
            fig.update_traces(width=0.7, textposition='outside')
            st.plotly_chart(fig)

            st.write("---")
            st.write("")
            st.write("")

        elif viz_type == "pie":
            with st.expander("see table"):
                df = data.drop(columns=['YEAR_MONTH', 'REGION'])
                st.dataframe(df, use_container_width=True)

            fig = px.pie(data, names=x_axis, values=y_axis)
            fig.update_layout(width=850, height=650, legend=dict(font=dict(size=16)))
            st.plotly_chart(fig)

            st.write("---")
            st.write("")
            st.write("")
    else:
        st.write(f"No {subheader} data available for {month} {year}.")


class CategoriesPerRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/categories/net_sales_per_category_region.sql',
                          'data_analytics/queries/categories/units_sold_per_category_region.sql',
                          'data_analytics/queries/categories/perc_of_sales_spent_in_ad_category.sql'],
                         conn=connection)

    def render(self):
        region, year, month = filters_selection()

        if st.sidebar.button("see report"):
            if not region or not year or not month:
                st.error("Please select region, year and month.")
                return

            if int(year) == datetime.now().year and int(month) > datetime.now().month:
                st.error("The selected date is invalid. Please select a previous date.")
                return

            month_name = calendar.month_name[int(month)]
            year_month = year + month

            st.title(f"Categories overview")
            st.write("---")
            st.subheader(f"region {region}")
            st.write(f"{month_name} {year}")
            st.write("")
            st.write("")

            with st.spinner("Loading data..."):
                net_sales_data = self.net_sales(region, year_month)
                units_sold_data = self.units_sold(region, year_month)
                ad_spent_data = self.perc_of_sales_spent_in_ad(region, year_month)

                st.empty()

                display_metric("Net sales", "Share of the company's total net sales per category.",
                               month_name, year, net_sales_data, "pie", "CATEGORY", "net sales in EUR")
                display_metric("Units sold", "Total units sold.",
                               month_name, year, units_sold_data, "bar", "CATEGORY", "units sold")
                display_metric("Advertisement spends",
                               "Percentage of the total net sales spent in paid advertisement. ",
                               month_name, year, ad_spent_data, "bar", "CATEGORY", "% of net sales spent in ad")

    def net_sales(self, region, year_month):
        return self.query_data(0, region, year_month)

    def units_sold(self, region, year_month):
        return self.query_data(1, region, year_month)

    def perc_of_sales_spent_in_ad(self, region, year_month):
        return self.query_data(2, region, year_month)

    def query_data(self, query_index, region, year_month):
        query = self.load_sql_query(query_index, region=region, year_month=year_month)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)