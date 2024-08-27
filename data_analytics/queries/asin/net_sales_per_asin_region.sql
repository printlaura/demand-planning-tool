-- net sales per month per ASIN/region

select iff(month(date) > 9,
            cast(month(date) as varchar) || '/' || cast(year(date) as varchar) ,
            '0' || cast(month(date) as varchar) || '/' || cast(year(date) as varchar)
        ) as "month & year",
        asin,
        region,
        round(iff(sum(net_sales) < 0, 0, sum(net_sales)), 2) as "net sales in EUR"
from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
where asin = '{asin}'
    and region = '{region}'
    {year_filter} -- pass year condition dynamically from python input
group by asin, region, "month & year"