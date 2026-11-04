-- 1. Create Product Dimension
CREATE OR REPLACE TABLE
`sales-etl-assignment.sales_warehouse.dim_product` AS
SELECT DISTINCT
    product_id,
    product_name,
    category
FROM
`sales-etl-assignment.sales_warehouse.stg_sales_raw`;


-- 2. Create Sales Fact
CREATE OR REPLACE TABLE
`sales-etl-assignment.sales_warehouse.fact_sales` AS
SELECT
    sale_id,
    sale_date,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price AS sales_amount
FROM
`sales-etl-assignment.sales_warehouse.stg_sales_raw`
WHERE
    quantity > 0
    AND unit_price > 0;