import pandas as pd
# from .db_connection import get_engine
# import snowflake.connector


class SalesDataPreprocessor:
    """
    def __init__(self, snowflake_config, asin, region):
        self.snowflake_config = snowflake_config
        self.asin = asin
        self.region = region
        self.df = None
"""

    def __init__(self, df):
        self.df = df

        """
    def load_data(self):
        # load data from snowflake""""""

        query = f # comillas triples
                WITH category AS
                (SELECT DISTINCT asin, category 
                FROM DWH_PROD.CORE.DIM_PRODUCT
                WHERE asin = upper('{self.asin}'),

                sales_data AS
                (
                    SELECT year(report_date) AS year,
                            month(report_date) AS month,
                            region,
                            asin,
                            IFF(SUM(units_sold) < 0, 0, SUM(units_sold)) AS units_sold
                    FROM DATAMARTS.BRAND_MGMT.STOCK_PERFORMANCE_TEST
                    WHERE report_date BETWEEN DATE_TRUNC('month', DATEADD('month', -6, CURRENT_DATE))
                        AND LAST_DAY(DATEADD('month', -1, CURRENT_DATE))
                        AND channel = 'AMZN'
                        AND asin = upper('{self.asin}')
                        AND region = upper('{self.region}')
                    GROUP BY year, month, region, asin
                    ORDER BY year DESC, month DESC
                ),

                sale_price AS
                (
                    SELECT AVG(sale_price_eur) AS sale_price_eur, 
                            asin, 
                            region, 
                            YEAR(date) AS year, 
                            MONTH(date) AS month
                    FROM 
                    (
                        SELECT asin, date, region, sale_price_eur
                        FROM DATAMARTS.BRAND_MGMT.ASIN_TRACKING_DETAILED_HISTORY
                        WHERE asin = upper('{self.asin}')
                            AND region = upper('{self.region}')
                            date < DATE_TRUNC('month', CURRENT_DATE)
                    )
                    GROUP BY asin, region, year, month
                )

                SELECT a.*, b.category, d.sale_price_eur
                FROM sales_data a
                INNER JOIN category b ON a.asin = b.asin 
                LEFT JOIN sale_price d ON a.asin = d.asin 
                    AND a.region = d.region
                    AND a.year = d.year
                    AND a.month = d.month;
                """

    """
        conn = snowflake.connector.connect(**self.snowflake_config)
        self.df = pd.read_sql(query, conn)
        conn.close()
        print("Data successfully loaded from Snowflake.")

    """

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
        self.df.map(lambda x: 1 if x == True else (0 if x == False else x))
        self._add_category_columns()
        self.df = pd.get_dummies(self.df, columns=['MONTH'])

        for column in self.df.columns:
            if self.df[column].dtype == 'bool':
                self.df[column] = self.df[column].astype(int)

        print(self.df.columns)
        print("Data preprocessed successfully.")
        return self.df

    def _fill_missing_sale_price(self):
        # fill null price values with the latest available ones

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
