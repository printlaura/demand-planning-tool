import pandas as pd
import streamlit as st
import logging


class SalesDataPreprocessor:
    def __init__(self, sf_query_executor, asin, region, df=None):
        self.sf_query_executor = sf_query_executor
        self.asin = asin
        self.region = region
        self.df = df

    def load_data(self, conn):
        with open('forecasting/queries/sales_data_for_prediction.sql', 'r') as file:
       # with open('forecasting/queries/dummy_sales_data_for_edge_case.sql', 'r') as file:
            query = file.read().format(asin=self.asin, region=self.region)

        self.df = self.sf_query_executor.execute_query(query, conn)

        if self.df is None or self.df.empty:
            raise ValueError("Failed to get prediction: there is no historical data available in Snowflake. "
                             "Try a different combination of ASIN & region.")

    def preprocess_data(self):
        if self.df is None or self.df.empty:
            raise ValueError("Data not loaded. Please load the data first.")

        self.df = self.check_input_dataset_shape(self.df)

        self.df['DATE'] = pd.to_datetime(self.df[['YEAR', 'MONTH']].assign(day=1))
        self.df = self.df.drop(columns=['YEAR'])
        self.df = self.df.sort_values(by=['DATE'])
        self._fill_missing_sale_price()
        self.df['PRICE'] = self.df['SALE_PRICE']
        self.df = self.df.drop(columns=['FILLED_SALE_PRICE', 'SALE_PRICE', 'ASIN', 'REGION', 'DATE'])
        self._convert_data_types()
        self.df = pd.get_dummies(self.df, columns=['CATEGORY'])
        self.df = pd.get_dummies(self.df, columns=['MONTH'])
        self.df = self.df.applymap(lambda x: 1 if x is True else (0 if x is False else x))

        self._add_dummy_columns()

        for column in self.df.columns:
            if self.df[column].dtype == 'bool':
                self.df[column] = self.df[column].astype(int)

        print("Data preprocessed successfully.")
        return self.df

    def _fill_missing_sale_price(self):
        # Fill null price values with the latest available ones
        self.df['FILLED_SALE_PRICE'] = self.df['SALE_PRICE'].ffill()
        self.df['SALE_PRICE'] = self.df['FILLED_SALE_PRICE']

    def _convert_data_types(self):
        self.df['UNITS_SOLD'] = self.df['UNITS_SOLD'].astype('float32')
        self.df['PRICE'] = self.df['PRICE'].astype('float32')

    def _add_dummy_columns(self):
        # manually create categorical columns not present in raw dataset

        category_columns = [
            "CATEGORY_Apparel", "CATEGORY_Art Supplies, Books & Music", "CATEGORY_Beauty & Wellness",
            "CATEGORY_Electronics Others", "CATEGORY_Gadgets & Tech", "CATEGORY_Hardware",
            "CATEGORY_Health Care", "CATEGORY_Home Appliance", "CATEGORY_Home Furnishing",
            "CATEGORY_Home Softgoods", "CATEGORY_Household Chemicals", "CATEGORY_Kids & Baby",
            "CATEGORY_Kitchen & Dining", "CATEGORY_Lighting", "CATEGORY_Nutrition",
            "CATEGORY_Office Organization & Furnishing", "CATEGORY_Pet Supplies", "CATEGORY_Smartphone",
            "CATEGORY_Sports & Outdoor", "CATEGORY_Tablet & eReaders"
        ]

        month_columns = [
            "MONTH_1", "MONTH_2", "MONTH_3", "MONTH_4", "MONTH_5", "MONTH_6", "MONTH_7", "MONTH_8",
            "MONTH_9", "MONTH_10", "MONTH_11", "MONTH_12",
        ]

        for column in category_columns:
            if column not in self.df.columns:
                self.df[column] = 0

        for column in month_columns:
            if column not in self.df.columns:
                self.df[column] = 0

        self.df = self.df[['UNITS_SOLD', 'PRICE'] + category_columns + month_columns]

    def check_input_dataset_shape(self, df, required_months=6):
        df = df.sort_values(by=['YEAR', 'MONTH'])

        # values to duplicate
        category = df['CATEGORY'].iloc[0]
        region = df['REGION'].iloc[0]
        asin = df['ASIN'].iloc[0]

        # check earliest date available in the db
        earlier_year = df['YEAR'].min()
        earlier_month = df['MONTH'].min()

        # check how many rows would be missing to get the expected shape
        additional_rows_needed = required_months - len(df)

        if additional_rows_needed > 0:
            st.warning("There is no sufficient historical data, so the accuracy of the prediction may suffer.")

        new_rows = []

        # calculate year and month to be added to new row
        for i in range(additional_rows_needed):
            if earlier_month == 1:
                earlier_month = 12
                earlier_year -= 1
            else:
                earlier_month -= 1

            new_row = {
                'YEAR': earlier_year,
                'MONTH': earlier_month,
                'REGION': region,
                'ASIN': asin,
                'UNITS_SOLD': 0,
                'CATEGORY': category,
                'SALE_PRICE': 0.0
            }
            new_rows.append(new_row)

        new_rows_df = pd.DataFrame(new_rows)

        df = pd.concat([new_rows_df, df], ignore_index=True)
        df = df.tail(required_months).reset_index(drop=True)

        return df
