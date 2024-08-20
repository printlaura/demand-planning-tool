-- ad spend per unit sold per month per ASIN/region

select year_month, asin, region, div0(ad_spend, units_sold) as ad_spend_per_unit_sold
from
(
    select iff(month(date) > 9,
                cast(year(date) as varchar) || cast(month(date) as varchar),
                cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
            ) as year_month,
            asin,
            region,
            sum(units_sold_total) as units_sold,
            sum(ad_spend) as ad_spend
    from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
    group by asin, region, year_month
)
where asin = upper('{asin}')
    and region = upper('{region}')
