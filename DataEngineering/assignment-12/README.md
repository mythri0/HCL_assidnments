# AWS Serverless CSV-to-Parquet ETL Pipeline

## 1. Project Overview

This project implements a serverless data engineering pipeline using **Amazon S3, AWS Glue, AWS Glue Data Catalog, AWS Glue Workflows, Amazon EventBridge, and AWS CloudTrail**.

The pipeline automatically processes raw sales data stored in Amazon S3 in CSV format, removes records with missing customer names, and converts the cleaned data into Apache Parquet format.

The objective is to build an event-driven ETL pipeline that reduces manual intervention and provides an automated approach to processing incoming data.

## 2. Architecture

```text
             Raw Sales CSV
                   |
                   v
          Amazon S3 Raw Bucket
                   |
                   v
             AWS Glue Crawler
                   |
                   v
           AWS Glue Data Catalog
                   |
                   |
          New CSV Object Uploaded
                   |
                   v
             AWS CloudTrail
          (S3 Data Events - Write)
                   |
                   v
             Amazon EventBridge
              (Event Rule)
                   |
                   v
             AWS Glue Workflow
                   |
                   v
             AWS Glue Trigger
                   |
                   v
             AWS Glue ETL Job
                (PySpark)
                   |
          +--------+---------+
          |                  |
          v                  v
      Read CSV          Clean Records
          |                  |
          +--------+---------+
                   |
                   v
          Convert to Parquet
                   |
                   v
        Amazon S3 Processed Bucket
                   |
                   v
             Parquet Files
```

## 3. AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon S3 | Stores raw CSV and processed Parquet files |
| AWS Glue Crawler | Automatically discovers the CSV schema |
| AWS Glue Data Catalog | Stores table metadata and schema information |
| AWS Glue ETL | Executes PySpark data transformations |
| AWS Glue Workflow | Orchestrates the ETL job |
| AWS Glue Trigger | Starts the ETL job based on the configured event |
| Amazon EventBridge | Detects matching S3-related events and starts the workflow |
| AWS CloudTrail | Records S3 data events used by the EventBridge rule |
| AWS IAM | Manages permissions for AWS resources |

## 4. S3 Bucket Configuration

Two Amazon S3 buckets were created.

### Raw Data Bucket

**Bucket name:** `suriya-sales-raw-2026`

Purpose:
- Stores incoming sales CSV files.
- Acts as the source of the ETL pipeline.
- Provides input data for the AWS Glue job.

### Processed Data Bucket

**Bucket name:** `suriya-sales-processed-2026`

Purpose:
- Stores cleaned and transformed data.
- Holds the final output in Apache Parquet format.

Output location:

```text
s3://suriya-sales-processed-2026/sales/
```

## 5. Sample Input Data

The input CSV contains sales transaction records.

```csv
order_id,customer_name,product,quantity,amount
101,Arun,Laptop,1,55000
102,Kumar,Mouse,2,1000
103,Priya,Keyboard,1,2500
104,,Monitor,1,12000
105,David,Laptop,1,55000
106,Meena,Mouse,3,1500
```

The record with an empty `customer_name` is considered invalid and removed during transformation.

## 6. AWS Glue Crawler and Data Catalog

An AWS Glue Crawler was configured to scan the raw S3 bucket.

The crawler performs the following operations:

1. Scans the CSV files stored in the raw bucket.
2. Identifies the column names.
3. Infers the data types.
4. Creates or updates the corresponding table in AWS Glue Data Catalog.

The Data Catalog stores metadata about the dataset, including its schema and S3 location.

**Important:** The Data Catalog stores metadata, not the actual sales records.

## 7. PySpark ETL Implementation

The AWS Glue ETL job performs the following operations:

1. Initializes the AWS Glue and Spark contexts.
2. Reads CSV files from the raw S3 bucket.
3. Identifies records with null or empty customer names.
4. Removes invalid records.
5. Converts the cleaned DataFrame into Parquet format.
6. Writes the output to the processed S3 bucket.
7. Commits the Glue job.

### PySpark Script

```python
import sys

from pyspark.context import SparkContext
from pyspark.sql.functions import col, trim

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

# Initialize AWS Glue and Spark
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

print("Starting CSV to Parquet ETL job...")

# Define S3 locations
raw_path = "s3://suriya-sales-raw-2026/"
processed_path = "s3://suriya-sales-processed-2026/sales/"

# Read CSV data
sales_df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(raw_path)

print("Raw sales data loaded")
print("Input record count:", sales_df.count())

# Remove null and empty customer names
cleaned_df = sales_df.filter(
    col("customer_name").isNotNull() &
    (trim(col("customer_name")) != "")
)

print("Cleaned record count:", cleaned_df.count())

# Write output in Parquet format
cleaned_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .save(processed_path)

print("Parquet output successfully written!")
print("Destination:", processed_path)

job.commit()
```

## 8. Data Transformation

The main transformation removes rows where `customer_name` is either NULL or an empty string.

The following PySpark condition is used:

```python
cleaned_df = sales_df.filter(
    col("customer_name").isNotNull() &
    (trim(col("customer_name")) != "")
)
```

### Expected Transformation Result

| Metric | Value |
|---|---:|
| Input records | 6 |
| Invalid records removed | 1 |
| Output records | 5 |

The resulting dataset is written in Apache Parquet format using Snappy compression.

## 9. Event-Driven Automation

Amazon EventBridge and AWS Glue Workflows are used to automate the pipeline.

The automation process consists of:

1. A new CSV file is uploaded to the raw S3 bucket.
2. CloudTrail records the S3 `PutObject` data event.
3. EventBridge evaluates the event against the configured rule.
4. The rule targets the AWS Glue Workflow.
5. The workflow activates its configured event trigger.
6. The Glue ETL job executes.
7. The transformed Parquet data is stored in the processed bucket.

The EventBridge rule uses the default event bus.

**Event matching:** S3 object creation through the CloudTrail `PutObject` event.

For reliable operation, the event pattern should additionally filter the intended raw-data prefix and `.csv` object suffix.

## 10. IAM Permissions

An IAM role named:

`sales-role-glue-suriya`

was configured for AWS Glue.

The role requires appropriate permissions to:

- Read objects from the raw S3 bucket.
- List and access the raw bucket.
- Write transformed objects to the processed S3 bucket.
- Access required AWS Glue resources.
- Publish execution logs to Amazon CloudWatch.

An additional EventBridge execution role grants permission to invoke the AWS Glue Workflow.

## 11. Execution and Validation

The pipeline was executed and verified using the AWS Management Console.

### Validation 1: Glue Data Catalog

Verified that the crawler successfully identified the sales CSV schema and registered the table in the Data Catalog.

### Validation 2: AWS Glue Workflow

Verified the workflow execution through the AWS Glue Workflow History page.

### Validation 3: Amazon S3 Output

Verified the existence of a generated Parquet object in:

```text
s3://suriya-sales-processed-2026/sales/
```

Generated output example:

```text
part-00000-...-c000.snappy.parquet
```

The output object was confirmed in the Amazon S3 console.

### Validation 4: Glue Job Run

The individual Glue ETL job run should be verified with the `SUCCEEDED` status in AWS Glue Job Runs.

## 12. Project Folder Structure

```text
aws-serverless-csv-to-parquet/
│
├── scripts/
│   └── sales_csv_to_parquet.py
│
├── sample-data/
│   └── sales.csv
│
├── screenshots/
│   ├── glue-crawler.png
│   ├── data-catalog-schema.png
│   ├── glue-job-success.png
│   ├── workflow-history.png
│   ├── eventbridge-rule.png
│   └── processed-parquet-s3.png
│
└── README.md
```

## 13. Key Concepts Learned

Through this project, the following data engineering concepts were implemented and explored:

- Serverless ETL architecture
- Amazon S3 object storage
- CSV and Parquet file formats
- AWS Glue Crawlers
- AWS Glue Data Catalog
- PySpark DataFrame transformations
- Null value handling
- Event-driven architecture
- Amazon EventBridge rules and targets
- AWS CloudTrail S3 data events
- AWS Glue Workflows and triggers
- IAM roles and permission policies
- Snappy compression
- Data pipeline execution monitoring

## 14. Future Improvements

The pipeline can be extended with:

- Date-based partitioning of Parquet files.
- Data quality validation.
- Error handling and retry mechanisms.
- Amazon SNS notifications for job failures.
- CloudWatch dashboards and monitoring.
- Incremental processing of incoming CSV files.
- AWS Glue Data Catalog updates after processing.

For production use, input processing should be restricted to a dedicated raw-data prefix, and output paths should be designed to prevent overwriting previously processed data.

## 15. Conclusion

This project demonstrates the implementation of a serverless, event-driven ETL pipeline using AWS services.

Raw sales data is stored in Amazon S3, its schema is discovered through AWS Glue Crawlers, and PySpark performs data cleaning and format conversion. Amazon EventBridge, CloudTrail, and AWS Glue Workflows provide the automation mechanism.

The final transformed dataset is stored in Amazon S3 in compressed Apache Parquet format.

This project provides practical experience with cloud-based data ingestion, transformation, orchestration, and storage using AWS services.

---

**Technologies:** Amazon S3 | AWS Glue | PySpark | AWS Glue Data Catalog | AWS Glue Workflows | Amazon EventBridge | AWS CloudTrail | IAM | Apache Parquet