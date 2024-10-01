select *
from
(
    SELECT 2024 AS year,
           4 AS month,
           'EU' as region,
           'TESTASIN' as asin,
           24 AS units_sold,
           'Hardware' as category,
           11.10 as sale_price
    union
        SELECT 2024 AS year,
           5 AS month,
           'EU' as region,
           'TESTASIN' as asin,
           26 AS units_sold,
           'Hardware' as category,
           10.00 as sale_price
  /*  union
    SELECT 2024 AS year,
           6 AS month,
           'EU' as region,
           'TESTASIN' as asin,
           20 AS units_sold,
            'Hardware' as category,
           8.50 as sale_price
        union
    SELECT 2024 AS year,
           7 AS month,
           'EU' as region,
           'TESTASIN' as asin,
           20 AS units_sold,
            'Hardware' as category,
           8.50 as sale_price
        union
    SELECT 2024 AS year,
           8 AS month,
           'EU' as region,
           'TESTASIN' as asin,
           20 AS units_sold,
            'Hardware' as category,
           8.50 as sale_price
        union
    SELECT 2024 AS year,
           9 AS month,
           'EU' as region,
           'TESTASIN' as asin,
           20 AS units_sold,
            'Hardware' as category,
           8.50 as sale_price*/
)
ORDER BY year DESC, month DESC