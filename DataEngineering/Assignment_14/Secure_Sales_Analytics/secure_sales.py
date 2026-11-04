import sqlite3

# Step 1: Create database connection
conn = sqlite3.connect("sales.db")

cursor = conn.cursor()

# Step 2: Create sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    sales_amount REAL
)
""")

# Step 3: Insert sample customer data
customers = [
    (1, "Arun", "arun@gmail.com", "9876543210", 1500),
    (2, "Priya", "priya@gmail.com", "9876543211", 2500),
    (3, "Karthik", "karthik@gmail.com", "9876543212", 1800),
    (4, "Divya", "divya@gmail.com", "9876543213", 3000),
    (5, "Rahul", "rahul@gmail.com", "9876543214", 2200)
]

cursor.executemany("""
INSERT OR IGNORE INTO sales
VALUES (?, ?, ?, ?, ?)
""", customers)

conn.commit()

# Step 4: Display original data
print("ORIGINAL CUSTOMER DATA")

cursor.execute("SELECT * FROM sales")

for row in cursor.fetchall():
    print(row)


# Step 5: Secure parameterized query function

def secure_query(customer_id):

    query = """
    SELECT customer_id, customer_name, email, phone, sales_amount
    FROM sales
    WHERE customer_id = ?
    """

    cursor.execute(query, (customer_id,))

    return cursor.fetchall()


# Step 6: Test secure query

print("\nSECURE CUSTOMER SEARCH")

search_id = 1

result = secure_query(search_id)

for row in result:
    print(row)


# Step 7: Email masking function

def mask_email(email):
    username, domain = email.split("@")
    return username[0] + "***@" + domain


# Step 8: Phone masking function

def mask_phone(phone):
    return "******" + phone[-4:]


# Step 9: Display masked customer data

print("\nMASKED CUSTOMER DATA")

cursor.execute("SELECT * FROM sales")

for row in cursor.fetchall():

    customer_id, name, email, phone, amount = row

    masked_email = mask_email(email)
    masked_phone = mask_phone(phone)

    print(
        customer_id,
        name,
        masked_email,
        masked_phone,
        amount
    )


conn.close()