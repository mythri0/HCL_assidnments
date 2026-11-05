
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, round, col

# 1. Create SparkSession
spark = SparkSession.builder \
    .appName("Daily Sales Reporting") \
    .master("local[*]") \
    .getOrCreate()

print("Spark application started successfully!")

# 2. Read overnight sales from staging layer
input_path = "/opt/spark/staging/overnight_sales.csv"

sales_df = spark.read.csv(
    input_path,
    header=True,
    inferSchema=True
)

print("Staging data loaded successfully!")

# 3. Calculate order-level sales
orders_df = sales_df.withColumn(
    "order_sales",
    col("quantity") * col("unit_price")
)

# 4. Build the Spark execution plan
print("\nSpark execution plan BEFORE execution:")
orders_df.explain(mode="formatted")

# 5. Calculate business metrics
metrics_df = orders_df.agg(
    round(sum("order_sales"), 2).alias("total_sales"),
    round(sum("order_sales") / count("order_id"), 2)
        .alias("average_order_value"),
    count("order_id").alias("total_orders")
)

# 6. Trigger execution using an action
print("\nExecuting Spark transformations...")
metrics_df.show(truncate=False)

# 7. Write results to presentation layer
output_path = "/opt/spark/presentation/daily_sales_report"

metrics_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(output_path)

print("\nDaily sales report generated successfully!")

spark.stop()
