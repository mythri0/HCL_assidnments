# Databricks / Synapse Spark Notebook Task Script
# Author: Poornima - Data Engineer at NorthStar Retail

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, desc

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("NorthStar_Sales_Aggregation") \
    .getOrCreate()

# 1. Define Data Lake paths (Storage Layer)
storage_account_name = "adlspoornimasales"
container_name = "salesdata"
raw_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/raw-data/*.parquet"
processed_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/processed-data/sales_summary/"

# 2. Read Raw Sales Data (Parquet format)
df_raw = spark.read.parquet(raw_path)

# 3. Perform Compute & Transformation (Compute Layer)
# Filter out transactions under $100 and aggregate sales & counts by region
df_processed = df_raw.filter(col("total_sales") > 100) \
    .groupBy("region") \
    .agg(
        sum("total_sales").alias("total_sales"),
        count("transaction_id").alias("transaction_count")
    ) \
    .orderBy(desc("total_sales"))

# Display transformation output in notebook
display(df_processed)

# 4. Write back processed results to Data Lake Storage Gen2
df_processed.write \
    .mode("overwrite") \
    .parquet(processed_path)
