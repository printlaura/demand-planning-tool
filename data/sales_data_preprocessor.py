import pandas as pd
from snowflake_query_executor import SnowflakeQueryExecutor


class SalesDataPreprocessor:
    def __init__(self, snowflake_executor, asin, region, df=None):
        self.snowflake_executor = snowflake_executor
        self.asin = asin
        self.region = region
        self.df = df

    def load_data(self):
        with open('queries.sql', 'r') as file:
            query = file.read().format(asin=self.asin, region=self.region)

        self.df = SnowflakeQueryExecutor.execute_query(query)

    def preprocess_data(self):
        if self.df is None:
            raise ValueError("Data not loaded. Please load the data first.")

        self.df['DATE'] = pd.to_datetime(self.df[['YEAR', 'MONTH']].assign(day=1))
        self.df = self.df.drop(columns=['YEAR'])
        self.df = self.df.sort_values(by=['DATE'])
        self._fill_missing_sale_price()
        self.df['PRICE'] = self.df['SALE_PRICE']
        self.df = self.df.drop(columns=['FILLED_SALE_PRICE', 'SALE_PRICE', 'ASIN', 'REGION', 'DATE'])
        self._convert_data_types()
        self.df = pd.get_dummies(self.df, columns=['CATEGORY'])
        self.df = self.df.map(lambda x: 1 if x == True else (0 if x == False else x))
        self._add_category_columns()
        self.df = pd.get_dummies(self.df, columns=['MONTH'])

        for column in self.df.columns:
            if self.df[column].dtype == 'bool':
                self.df[column] = self.df[column].astype(int)

        print(self.df.columns)
        print("Data preprocessed successfully.")
        return self.df

    def _fill_missing_sale_price(self):
        # Fill null price values with the latest available ones
        self.df['FILLED_SALE_PRICE'] = self.df.groupby(['DATE'])['SALE_PRICE'].ffill()
        self.df['SALE_PRICE'] = self.df['FILLED_SALE_PRICE']

    def _convert_data_types(self):
        self.df['UNITS_SOLD'] = self.df['UNITS_SOLD'].astype('float32')
        self.df['PRICE'] = self.df['PRICE'].astype('float32')

    def _add_category_columns(self):
        category_columns = [
            "CATEGORY_Apparel", "CATEGORY_Art Supplies, Books & Music", "CATEGORY_Beauty & Wellness",
            "CATEGORY_Electronics Others", "CATEGORY_Gadgets & Tech", "CATEGORY_Hardware",
            "CATEGORY_Health Care", "CATEGORY_Home Appliance", "CATEGORY_Home Furnishing",
            "CATEGORY_Home Softgoods", "CATEGORY_Household Chemicals", "CATEGORY_Kids & Baby",
            "CATEGORY_Kitchen & Dining", "CATEGORY_Lighting", "CATEGORY_Nutrition",
            "CATEGORY_Office Organization & Furnishing", "CATEGORY_Pet Supplies", "CATEGORY_Smartphone",
            "CATEGORY_Sports & Outdoor", "CATEGORY_Tablet & eReaders"
        ]

        for column in category_columns:
            if column not in self.df.columns:
                self.df[column] = 0

        self.df = self.df[['MONTH', 'UNITS_SOLD', 'PRICE'] + category_columns]
