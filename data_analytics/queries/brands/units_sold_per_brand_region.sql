-- units sold per month per brand/region

select *
from
(
    select iff(month(date) > 9,
            cast(year(date) as varchar) || cast(month(date) as varchar),
            cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
        ) as year_month,
        brand,
        region,
        iff(sum(units_sold) < 0, 0, sum(units_sold)) as "units sold"
    from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
    where year(date) > 2022
    group by brand, region, year_month
)
where region = upper(:region)
