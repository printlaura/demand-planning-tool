import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from sales_data_preprocessor import SalesDataPreprocessor


@pytest.fixture
def setup_snowflake_executor():
    executor = MagicMock()
    executor.execute_query = MagicMock(return_value=pd.DataFrame({
        'YEAR': [2021, 2021],
        'MONTH': [1, 2],
        'SALE_PRICE': [20, 30],
        'UNITS_SOLD': [100, 150],
        'CATEGORY': ['Electronics', 'Gadgets']
    }))

    return executor


@pytest.mark.parametrize("asin, region", [("B001234", "US"), ("B002345", "EU")])
def test_load_data(setup_snowflake_executor, asin, region):
    query = f"SELECT * FROM sales WHERE ASIN='{asin}' AND REGION='{region}';"

    with patch("builtins.open", mock_open(read_data=query)):
        processor = SalesDataPreprocessor(setup_snowflake_executor, asin, region)
        processor.load_data()

        assert processor.df is not None, "Dataframe should not be None after loading data"
        assert not processor.df.empty, "Dataframe should not be empty after loading data"

        setup_snowflake_executor.execute_query.assert_called_once()


def test_preprocess_data_without_load(setup_snowflake_executor):
    processor = SalesDataPreprocessor(setup_snowflake_executor, "B001234", "US")
    with pytest.raises(ValueError):
        processor.preprocess_data()


def test_preprocess_data_success(setup_snowflake_executor):
    processor = SalesDataPreprocessor(setup_snowflake_executor, "B001234", "US", df=pd.DataFrame({
        'ASIN': "B001234",
        'REGION': "US",
        'YEAR': [2021],
        'MONTH': [1],
        'SALE_PRICE': [100],
        'UNITS_SOLD': [200],
        'CATEGORY': ['Electronics']
    }))
    processed_df = processor.preprocess_data()

    assert 'PRICE' in processed_df.columns, "PRICE column should exist after preprocessing"
    assert all(
        isinstance(processed_df[col].dtype, pd.api.types.CategoricalDtype) or processed_df[col].dtype in [int, float]
        for col in processed_df.columns), "Data types should be properly converted or categorized"


def test_fill_missing_sale_price(setup_snowflake_executor):
    processor = SalesDataPreprocessor(setup_snowflake_executor, "TESTASIN", "TESTREGION", pd.DataFrame({
        'DATE': pd.date_range(start='1/1/2021', periods=3, freq='M'),
        'SALE_PRICE': [20, None, 30]
    }))
    processor._fill_missing_sale_price()

    assert all(
        processor.df['SALE_PRICE'] == pd.Series([20, 20, 30])), "Missing SALE_PRICE should be filled by forward fill"


def test_convert_data_types(setup_snowflake_executor):
    processor = SalesDataPreprocessor(setup_snowflake_executor, "TESTASIN", "TESTREGION", pd.DataFrame({
        'UNITS_SOLD': ['100', '200'],
        'PRICE': ['50', '150']
    }))
    processor._convert_data_types()

    assert processor.df['UNITS_SOLD'].dtype == 'float32', "UNITS_SOLD should be converted to float32"
    assert processor.df['PRICE'].dtype == 'float32', "PRICE should be converted to float32"


def test_add_dummy_columns(setup_snowflake_executor):
    processor = SalesDataPreprocessor(setup_snowflake_executor, "TESTASIN", "TESTREGION", pd.DataFrame({
        'UNITS_SOLD': [100, 150],
        'PRICE': [20, 25],
        'CATEGORY_Apparel': [1, 1],
        'MONTH_6': [1, 0],
        'MONTH_7': [0, 1],
    }))

    processor._add_dummy_columns()

    assert 'CATEGORY_Apparel' in processor.df.columns, "Dummy category columns must be added"

    assert processor.df[
               'CATEGORY_Apparel'].sum() == 2, "Dummy category column for Apparel should reflect correct counts"
    assert processor.df['MONTH_6'].sum() == 1 and processor.df[
        'MONTH_7'].sum() == 1, "Dummy month columns must be added and set properly"
