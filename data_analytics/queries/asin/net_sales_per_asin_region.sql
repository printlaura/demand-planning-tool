-- net sales per month per ASIN/region

select iff(month(date) > 9,
            cast(year(date) as varchar) || cast(month(date) as varchar),
            cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
        ) as "year & month",
        asin,
        region,
        iff(sum(net_sales) < 0, 0, sum(net_sales)) as "net sales in EUR"
from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
where asin = '{asin}'
    and region = '{region}'
    {year_filter} -- pass year condition dynamically from python input
group by asin, region, "year & month"