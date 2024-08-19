-- units sold per month per ASIN/region

select iff(month(report_date) > 9,
            cast(year(report_date) as varchar) || cast(month(report_date) as varchar),
            cast(year(report_date) as varchar) || '0' || cast(month(report_date) as varchar)
        ) as year_month,
        region,
        asin,
        iff(sum(units_sold) < 0, 0, sum(units_sold)) as units_sold
from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
where asin = upper('{asin}')
    and region = upper('{region}')
group by asin, region, year_month