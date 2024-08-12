-- amount of days OOS per ASIN/region
with
oos_data as
(
    select iff(month(report_date) > 9,
               cast(year(report_date) as varchar) || cast(month(report_date) as varchar),
               cast(year(report_date) as varchar) || '0' || cast(month(report_date) as varchar)
               ) as year_month,
            asin,
            region,
            iff(is_out_of_stock = 'Y', 1, 0) as oos
    from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
    where asin = upper('{asin}')
        and region = upper('{region}')
)

select year_month, asin, region, sum(oos)
from oos_data
group by year_month, asin, region