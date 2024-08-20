-- units sold per category/region

with
category as
(
    select distinct asin, category
    from STREAMLIT_POC.SANDBOX.DIM_PRODUCT_VIEW
)


select year_month, category, region, sum(units_sold) as units_sold
from
(
    select iff(month(report_date) > 9,
                cast(year(report_date) as varchar) || cast(month(report_date) as varchar),
                cast(year(report_date) as varchar) || '0' || cast(month(report_date) as varchar)
            ) as year_month,
            region,
            a.asin,
            iff(units_sold < 0, 0, units_sold) as units_sold,
            b.category
    from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW a
    left join category b
    on a.asin = b.asin
    where region = upper('{region}')
)
group by year_month, category, region
