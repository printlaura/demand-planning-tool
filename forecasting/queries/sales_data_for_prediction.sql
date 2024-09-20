-- Sales data for prediction
WITH category AS
(
    SELECT DISTINCT asin, category
    FROM STREAMLIT_POC.SANDBOX.DIM_PRODUCT_VIEW
    WHERE asin = upper('{asin}')
),

-- get last 6 months of data available
distinct_months AS
(
    SELECT DISTINCT year(date) AS year, month(date) AS month
    FROM STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
    WHERE asin = upper('{asin}')
      AND region = upper('{region}')
    ORDER BY year DESC, month DESC
    LIMIT 6
),

sales_data AS
(
    SELECT year(date) AS year,
           month(date) AS month,
           region,
           asin,
           IFF(SUM(units_sold) < 0, 0, SUM(units_sold)) AS units_sold
    FROM STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
    WHERE (year(date), month(date)) IN (SELECT year, month FROM distinct_months)
     --   AND LAST_DAY(DATEADD('month', -1, CURRENT_DATE))
        AND asin = upper('{asin}')
        AND region = upper('{region}')
    GROUP BY year, month, region, asin
    ORDER BY year DESC, month DESC
),
sale_price AS
(
    SELECT AVG(sale_price) AS sale_price,
           asin,
           region,
           YEAR(date) AS year,
           MONTH(date) AS month
    FROM
    (
        SELECT asin, date, region, sale_price
        FROM STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
        WHERE asin = '{asin}'
          AND region = '{region}'
          AND date < DATE_TRUNC('month', CURRENT_DATE)
    )
    GROUP BY asin, region, year, month
)
SELECT a.*, b.category, d.sale_price
FROM sales_data a
INNER JOIN category b ON a.asin = b.asin
LEFT JOIN sale_price d ON a.asin = d.asin
    AND a.region = d.region
    AND a.year = d.year
    AND a.month = d.month;


-----------
-------
