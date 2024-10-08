-- amount of days OOS per asin
with
oos_data as
(
    select iff(month(date) > 9,
            cast(month(date) as varchar) || '/' || cast(year(date) as varchar) ,
            '0' || cast(month(date) as varchar) || '/' || cast(year(date) as varchar)
        ) as "month & year",
            asin,
           brand,
            region,
            iff(is_out_of_stock = 'Y', 1, 0) as oos
    from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
    where asin = '{asin}'
      and region = '{region}'
    {year_filter} -- pass year condition dynamically from python input
)

select "month & year", asin, region, sum(oos) as "total Out of Stock days"
from oos_data
group by asin, region, "month & year"