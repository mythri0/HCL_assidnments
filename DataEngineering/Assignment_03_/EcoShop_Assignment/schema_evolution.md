
# EcoShop Inventory System
## SQL vs NoSQL Database Comparison

### 1. Introduction
EcoShop is an inventory management system
that stores product details using SQL and NoSQL databases.

### 2. SQL Database - SQLite
SQLite is a relational database that stores data
in tables with predefined columns and data types.

We created a Products table containing:
- product_id
- product_name
- category
- price
- stock_quantity

The product_id is the Primary Key.

### 3. NoSQL Database - MongoDB
MongoDB is a document-oriented NoSQL database.
It stores information in JSON-like documents.

We created:
- Database: EcoShopDB
- Collection: Products

The same four product records were inserted
as JSON documents.

### 4. Adding material_type in SQL
In SQLite, we used ALTER TABLE to add a new column.

ALTER TABLE Products
ADD COLUMN material_type TEXT;

We then used UPDATE to assign material values
to the existing product records.

### 5. Adding material_type in NoSQL
In MongoDB, we directly added a new field called
material_type to each existing document.

No table structure modification was required.

### 6. SQL vs NoSQL Comparison

| Feature | SQL | NoSQL |
| Schema | Fixed | Flexible |
| Storage | Tables | Documents |
| Adding fields | ALTER TABLE | Add field to documents |
| Schema changes | More structured | More flexible |

### 7. Conclusion
SQL provides a structured and consistent way
to store inventory data.

MongoDB provides flexibility when product
attributes change frequently.

Both databases can be used for EcoShop inventory
management depending on the requirements.
