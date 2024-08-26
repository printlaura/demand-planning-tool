-- units sold per month per ASIN/region

select iff(month(date) > 9,
            cast(month(date) as varchar) || '/' || cast(year(date) as varchar) ,
            '0' || cast(month(date) as varchar) || '/' || cast(year(date) as varchar)
        ) as year_month,
        region,
        asin,
        iff(sum(units_sold) < 0, 0, sum(units_sold)) as "units sold"
from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
where asin = '{asin}'
    and region = '{region}'
    {year_filter} -- pass year condition dynamically from python input
group by asin, region, year_month