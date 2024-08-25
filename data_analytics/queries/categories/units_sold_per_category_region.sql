-- units sold per category/region

with
category as
(
    select distinct asin, category
    from STREAMLIT_POC.SANDBOX.DIM_PRODUCT_VIEW
)


select year_month, category, region, sum(units_sold) as "units sold"
from
(
    select iff(month(date) > 9,
                cast(year(date) as varchar) || cast(month(date) as varchar),
                cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
            ) as year_month,
            region,
            a.asin,
            iff(units_sold < 0, 0, units_sold) as units_sold,
            b.category
    from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW a
    left join category b
    on a.asin = b.asin
    where region =  '{region}'
    and b.category is not null
)
group by year_month, category, region
