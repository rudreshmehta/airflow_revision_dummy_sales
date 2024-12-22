CREATE TABLE IF NOT EXISTS staging_sales (
    id SERIAL PRIMARY KEY,
    order_id INT,
    customer_name TEXT,
    product TEXT,
    quantity INT,
    price NUMERIC,
    order_date DATE
);
CREATE TABLE IF NOT EXISTS analytics_sales_summary (
    product TEXT PRIMARY KEY,
    total_quantity INT,
    total_revenue NUMERIC
);