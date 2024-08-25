-- % of net sales spent in ad per category per region per year_month

with
category as
(
    select distinct asin, category
    from STREAMLIT_POC.SANDBOX.DIM_PRODUCT_VIEW
),

net_sales as
(
    select a.*, b.category
    from
    (
        select iff(month(date) > 9,
                    cast(year(date) as varchar) || cast(month(date) as varchar),
                    cast(year(date) as varchar) || '0' || cast(month(date) as varchar)
                ) as year_month,
                asin,
                region,
                sum(net_sales) as net_sales,
                sum(ad_spend) as ad_spend
        from STREAMLIT_POC.SANDBOX.ASIN_TRACKING_DETAILED_VIEW
        where year(date) > 2022
        group by asin, region, year_month
    ) a
    left join category b
    on a.asin = b.asin
    where b.category is not null
)

select category,
        region,
        year_month,
        round(div0(sum(ad_spend) * 100,sum(net_sales)), 2) as "% of net sales spent in ad"
from net_sales a
where region = upper(:region)
    and year_month = :year_month
group by category, region, year_month