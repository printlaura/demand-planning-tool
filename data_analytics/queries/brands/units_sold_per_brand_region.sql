-- units sold per month per brand/region

select iff(month(report_date) > 9,
            cast(year(report_date) as varchar) || cast(month(report_date) as varchar),
            cast(year(report_date) as varchar) || '0' || cast(month(report_date) as varchar)
        ) as year_month,
        brand,
        region,
        iff(sum(units_sold) < 0, 0, sum(units_sold)) as "units sold"
from STREAMLIT_POC.SANDBOX.STOCK_PERFORMANCE_TEST_VIEW
where region = upper('{region}')
group by brand, region, year_month