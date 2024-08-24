-- avg monthly sale price per ASIN/region

select avg(sale_price) as "average sale price",
        asin,
       region,
       iff(month(date) > 9,
            cast(year(date) as varchar) || cast(month(date) as varchar),
            cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
        ) as year_month,
from
(
    select asin, date, region, sale_price
    from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
    where asin = upper('{asin}')
        and region = upper('{region}')
        and year(date) > 2022
        {year_filter} -- pass year condition dynamically from python input
)
group by asin, region, year_month