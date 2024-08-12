-- Sales data for prediction
WITH category AS
(
    SELECT DISTINCT asin, category
    FROM DWH_PROD.CORE.DIM_PRODUCT
    WHERE asin = upper('{asin}')
),

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
        AND asin = upper('{asin}')
        AND region = upper('{region}')
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
        WHERE asin = upper('{asin}')
          AND region = upper('{region}')
          AND date < DATE_TRUNC('month', CURRENT_DATE)
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


-----------
-------

