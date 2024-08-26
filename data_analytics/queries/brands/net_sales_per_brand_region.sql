-- net sales per month per brand/region

select iff(month(date) > 9,
            cast(year(date) as varchar) || cast(month(date) as varchar),
            cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
        ) as year_month,
        brand,
        region,
        round(iff(sum(net_sales) < 0, 0, sum(net_sales))) as "net sales in EUR"
from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
where region = '{region}'
    and year_month = '{year_month}'
group by brand, region, year_month