from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


def filters_selection():
    asin = st.sidebar.text_input("Enter ASIN:", "")
    region = st.sidebar.selectbox("Select a region:", ["EU", "US", "UK", "JP"], index=None, placeholder="...")
    year = st.sidebar.multiselect("Select year(s):", ["2023", "2024"], default=[])

    return asin, region, year


def display_metric(subheader, description, data, viz_type, x_axis, y_axis):
    st.subheader(subheader)
    st.write(description)
    st.write("")
    st.write("")

    if data is not None and subheader == "Out of Stock days" and data["total Out of Stock days"].sum() == 0:
        st.write("This item has never been Out of Stock.")
        return None

    if data is not None:
        if viz_type == 'bar':
            st.bar_chart(data, x=x_axis, y=y_axis)
    else:
        st.write(f"No {subheader} data available for {description}.")

    st.write("")
    st.write("")


class AsinRegionCase(BaseAnalyticsCase):
    def __init__(self, connection):
        super().__init__(['data_analytics/queries/asin/units_sold_per_asin_region.sql',
                          'data_analytics/queries/asin/net_sales_per_asin_region.sql',
                          'data_analytics/queries/asin/avg_sale_price_asin_region.sql',
                          'data_analytics/queries/asin/oos_days_per_asin.sql'
                          ],
                         conn=connection)

    def render(self):
        st.title("ASIN")

        asin, region, year = filters_selection()

        year_filter = ""
        if year:
            year_filter = f"and year(date) in ({', '.join(map(str, year))})"

        if not asin or not region:
            st.error("Please enter ASIN and region.")
            return

        with st.spinner("Loading data..."):
            units_sold_data = self.units_sold(asin, region, year_filter)
            net_sales_data = self.net_sales(asin, region, year_filter)
            avg_sale_price_data = self.avg_sale_price(asin, region, year_filter)
            oos_days_data = self.oos_days(asin, region, year_filter)

            st.empty()

            display_metric("Units sold", f"{asin} - {region}", units_sold_data, "bar", "YEAR_MONTH", "units sold")
            display_metric("Net sales", f"{asin} - {region}", net_sales_data, "bar", "YEAR_MONTH", "net sales in EUR")
            display_metric("Average sale price", f"{asin} - {region}", avg_sale_price_data, "bar", "YEAR_MONTH",
                           "average sale price")
            display_metric("Out of Stock days", f"{asin} - {region}", oos_days_data, "bar", "YEAR_MONTH",
                           "total Out of Stock days")

    def units_sold(self, asin, region, year_filter):
        query = self.load_sql_query(0, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)

    def net_sales(self, asin, region, year_filter):
        query = self.load_sql_query(1, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)

    def avg_sale_price(self, asin, region, year_filter):
        query = self.load_sql_query(2, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)

    def oos_days(self, asin, region, year_filter):
        query = self.load_sql_query(3, asin=asin, region=region, year_filter=year_filter)
        data, columns = self.run_query(query)
        if not data or not columns:
            return None

        return self.data_to_df(data, columns)
