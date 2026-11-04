CREATE DATABASE order_warehouse;
USE order_warehouse;

CREATE TABLE staging_orders (
    order_id VARCHAR(20),
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    email VARCHAR(100),
    order_date VARCHAR(30),
    amount VARCHAR(30),
    status VARCHAR(30)
);

USE order_warehouse;

INSERT INTO staging_orders
(order_id, customer_id, customer_name, email, order_date, amount, status)
VALUES
('101', 'C01', 'Arun', 'arun@gmail.com', '2026-01-01', '1500', 'completed'),

('102', 'C02', 'Priya', 'priya@gmail.com', '2026-01-02', '2500', 'PENDING'),

('103', 'C01', 'Arun', 'arun@gmail.com', '2026-01-03', '1200', 'Completed'),

('104', 'C03', 'Karthik', NULL, '2026-01-04', '1800', 'shipped'),

('105', 'C04', 'Divya', 'divya@gmail.com', '2026-01-05', NULL, 'cancelled'),

('106', 'C02', 'Priya', 'priya@gmail.com', '2026-01-06', '3000', 'completed'),

('107', 'C05', NULL, NULL, '2026-01-07', '900', 'pending');

SELECT * FROM staging_orders;

USE order_warehouse;
CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(20) UNIQUE,
    customer_name VARCHAR(100),
    email VARCHAR(100)
);

USE order_warehouse;

CREATE TABLE fact_orders (
    order_key INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(20) UNIQUE,
    customer_key INT,
    order_date DATE,
    amount DECIMAL(10,2),
    status VARCHAR(30),

    FOREIGN KEY (customer_key)
    REFERENCES dim_customer(customer_key)
);

USE order_warehouse;

INSERT INTO dim_customer (
    customer_id,
    customer_name,
    email
)
SELECT
    TRIM(customer_id),

    COALESCE(
        MAX(NULLIF(TRIM(customer_name), '')),
        'Unknown'
    ),

    COALESCE(
        MAX(NULLIF(TRIM(email), '')),
        'Not Available'
    )

FROM staging_orders

WHERE customer_id IS NOT NULL
AND TRIM(customer_id) <> ''

GROUP BY TRIM(customer_id);

SELECT * FROM dim_customer;




USE order_warehouse;

INSERT INTO fact_orders (
    order_id,
    customer_key,
    order_date,
    amount,
    status
)

SELECT
    TRIM(s.order_id),
    d.customer_key,

    STR_TO_DATE(
        TRIM(s.order_date),
        '%Y-%m-%d'
    ),

    COALESCE(
        CAST(NULLIF(TRIM(s.amount), '') AS DECIMAL(10,2)),
        0
    ),

    CASE
        WHEN LOWER(TRIM(s.status)) IN ('completed', 'complete')
            THEN 'COMPLETED'

        WHEN LOWER(TRIM(s.status)) = 'pending'
            THEN 'PENDING'

        WHEN LOWER(TRIM(s.status)) = 'shipped'
            THEN 'SHIPPED'

        WHEN LOWER(TRIM(s.status)) = 'cancelled'
            THEN 'CANCELLED'

        ELSE 'UNKNOWN'
    END

FROM staging_orders s

JOIN dim_customer d
    ON TRIM(s.customer_id) = d.customer_id

WHERE s.order_id IS NOT NULL
AND TRIM(s.order_id) <> '';


SELECT * FROM fact_orders;

SELECT * FROM staging_orders;
SELECT * FROM dim_customer;

SELECT
    f.order_id,
    d.customer_name,
    d.email,
    f.order_date,
    f.amount,
    f.status
FROM fact_orders f
JOIN dim_customer d
ON f.customer_key = d.customer_key;