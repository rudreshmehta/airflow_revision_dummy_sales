INSERT INTO analytics_sales_summary (product, total_quantity, total_revenue)
SELECT
    product,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_revenue
FROM
    staging_sales
GROUP BY
    product
ON CONFLICT (product) DO UPDATE
SET
    total_quantity = analytics_sales_summary.total_quantity + EXCLUDED.total_quantity,
    total_revenue = analytics_sales_summary.total_revenue + EXCLUDED.total_revenue;
