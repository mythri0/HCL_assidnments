
import sqlite3
from pathlib import Path

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_NAME = BASE_DIR / "monthly_sales.db"


# ==========================================
# 1. CREATE STAR SCHEMA AND INSERT SAMPLE DATA
# ==========================================

def create_database():

    print("\n========== DATABASE SETUP ==========")

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Create product dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Create date dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY,
            sale_date TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL
        )
    """)

    # Create sales fact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_sales (
            sale_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            date_id INTEGER,
            quantity INTEGER,
            sales_amount REAL,
            FOREIGN KEY (product_id)
                REFERENCES dim_product(product_id),
            FOREIGN KEY (date_id)
                REFERENCES dim_date(date_id)
        )
    """)

    # Insert sample product records
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_product
        VALUES (?, ?, ?)
    """, [
        (1, "Laptop", "Electronics"),
        (2, "Mouse", "Accessories"),
        (3, "Keyboard", "Accessories"),
        (4, "Monitor", "Electronics")
    ])

    # Insert sample date records
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_date
        VALUES (?, ?, ?, ?)
    """, [
        (20260101, "2026-01-15", 1, 2026),
        (20260102, "2026-01-20", 1, 2026),
        (20260201, "2026-02-10", 2, 2026),
        (20260202, "2026-02-18", 2, 2026),
        (20260301, "2026-03-05", 3, 2026)
    ])

    # Insert sample sales transactions
    cursor.executemany("""
        INSERT OR IGNORE INTO fact_sales
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, 1, 20260101, 2, 100000),
        (2, 2, 20260102, 5, 2500),
        (3, 3, 20260201, 3, 3600),
        (4, 1, 20260202, 1, 50000),
        (5, 4, 20260301, 2, 24000)
    ])

    connection.commit()
    connection.close()

    print("Star schema created successfully.")
    print("Sample records inserted successfully.")


# ==========================================
# 2. COPILOT-GENERATED MONTHLY SALES REPORT
# ==========================================

def generate_monthly_report():

    print("\n========== MONTHLY SALES REPORT ==========")

    connection = sqlite3.connect(DATABASE_NAME)

    # Copilot-generated SQL:
    # Join fact_sales with dim_product to retrieve
    # product names and categories.
    # Join fact_sales with dim_date to retrieve month and year.
    # Calculate total quantity and total sales amount.
    # Group the results by product, category, month and year.
    # Sort the results by year, month and product name.

    query = """
        SELECT
            dp.product_name,
            dp.category,
            dd.month,
            dd.year,
            SUM(fs.quantity) AS total_quantity,
            SUM(fs.sales_amount) AS total_sales_amount
        FROM fact_sales AS fs
        INNER JOIN dim_product AS dp
            ON fs.product_id = dp.product_id
        INNER JOIN dim_date AS dd
            ON fs.date_id = dd.date_id
        GROUP BY
            dp.product_name,
            dp.category,
            dd.month,
            dd.year
        ORDER BY
            dd.year,
            dd.month,
            dp.product_name;
    """

    # Verify and execute the generated SQL query
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    print(
        "\nProduct | Category | Month | Year | "
        "Quantity | Total Sales"
    )

    for row in rows:
        print(row)

    print(f"\nTotal report rows: {len(rows)}")

    connection.close()


# ==========================================
# 3. MAIN WORKFLOW
# ==========================================

def main():

    print("\n========================================")
    print("   AI-ASSISTED MONTHLY SALES REPORT")
    print("========================================")

    create_database()
    generate_monthly_report()

    print("\n========================================")
    print(" MONTHLY REPORT GENERATED SUCCESSFULLY!")
    print("========================================")


if __name__ == "__main__":
    main()
