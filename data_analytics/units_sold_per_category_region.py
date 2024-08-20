from data_analytics.base_case import BaseAnalyticsCase
import streamlit as st


class UnitsSoldPerCategoryCase(BaseAnalyticsCase):
    def __init__(self):
        super().__init__('data_analytics/queries/units_sold_per_category_region.sql')

    def render(self):
        st.title("Monthly units sold per category")
        region = st.selectbox("Select a region:", ["EU", "US", "CA", "UK", "AU", "JP", "MX"])
        # date_range = st.date_input("Select Date Range", [start_date, end_date])

        query = self.load_sql_query(region=region)

        """debug
        st.write("Executed Query:", query)
        print("Executed Query:", query)

        data, columns = self.run_query(query)

        st.write("Data Type:", type(data))
        st.write("Number of rows:", len(data))
        st.write("Columns:", columns)
        st.write("Number of columns:", len(columns))

        # Display the first few rows to confirm structure
        if data:
            st.write("Sample Data:", data[:5])
        """

        # Check for length consistency
        inconsistent_lengths = [len(row) != len(columns) for row in data]
        if any(inconsistent_lengths):
            st.error("Mismatch in data rows and column lengths detected.")

            if data and columns and not any(inconsistent_lengths):  # Ensure there's data and columns before converting
                try:
                    df = self.data_to_df(data, columns)  # Pass columns to the method
                    st.dataframe(df)
                    st.bar_chart(df.set_index("Region"))
                except Exception as e:
                    st.error(f"Error converting data to DataFrame: {e}")
            else:
                st.error("No data or columns available to render or detected inconsistent lengths.")
