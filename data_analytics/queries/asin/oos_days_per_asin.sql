-- amount of days OOS per asin
with
oos_data as
(
    select iff(month(report_date) > 9,
               cast(year(report_date) as varchar) || cast(month(report_date) as varchar),
               cast(year(report_date) as varchar) || '0' || cast(month(report_date) as varchar)
               ) as year_month,
            asin,
            brand,
            region,
            iff(is_out_of_stock = 'Y', 1, 0) as oos
    from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
    where asin = upper('{asin}')
)

select year_month, asin, brand, region, sum(oos) as "total Out of Stock days"
from oos_data
group by brand, asin, region, year_month