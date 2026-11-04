CREATE OR REPLACE TABLE
`sales-etl-assignment.sales_warehouse.sales_report` AS

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(f.sale_id) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_revenue

FROM
`sales-etl-assignment.sales_warehouse.fact_sales` f

JOIN
`sales-etl-assignment.sales_warehouse.dim_product` p

ON f.product_id = p.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category;