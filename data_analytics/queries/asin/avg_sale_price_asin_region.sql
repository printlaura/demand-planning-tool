-- avg monthly sale price per ASIN/region

select iff(month(date) > 9,
            cast(month(date) as varchar) || '/' || cast(year(date) as varchar),
            '0' || cast(month(date) as varchar) || '/' || cast(year(date) as varchar)
        ) as "month & year",
        asin,
        region,
        round(avg(sale_price), 3) as "average sale price"
from
(
    select asin, date, region, sale_price
    from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
    where asin = '{asin}'
        and region = '{region}'
        {year_filter} -- pass year condition dynamically from python input
)
group by asin, region, "month & year"