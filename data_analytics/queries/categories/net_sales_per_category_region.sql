with
category as
(
    select distinct asin, category
    from STREAMLIT_POC.SANDBOX.DIM_PRODUCT_VIEW
)

select year_month, category, region, round(sum(net_sales)) as net_sales_in_eur
from
(
    select iff(month(date) > 9,
                cast(year(date) as varchar) || cast(month(date) as varchar),
                cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
            ) as year_month,
            a.asin,
            region,
            b.category,
            iff(net_sales < 0, 0, net_sales) as net_sales
    from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW a
    left join category b
    on a.asin = b.asin
    where region = '{region}'
        and year_month = '{year_month}'
        and b.category is not null
)
group by category, region, year_month