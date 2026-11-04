

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL
);



INSERT INTO Products VALUES
(101, 'Bamboo Toothbrush', 'Personal Care', 50, 100),
(102, 'Cotton Bag', 'Accessories', 120, 50),
(103, 'Steel Bottle', 'Kitchen', 350, 30),
(104, 'Paper Notebook', 'Stationery', 80, 75);
