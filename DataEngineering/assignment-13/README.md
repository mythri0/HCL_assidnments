# Assignment 13 – Daily Sales Reporting Pipeline Using Apache Airflow and PySpark

## 1. Project Overview

This project implements an automated daily sales reporting pipeline using **Apache Airflow and Apache Spark (PySpark)**.

The pipeline simulates overnight batch ingestion of sales data, processes the data using Spark transformations, calculates important business metrics, and stores the final report in a presentation layer.

Apache Airflow is responsible for orchestrating and scheduling the workflow, while Apache Spark performs distributed data processing.

## 2. Objectives

- Simulate batch ingestion using static overnight sales CSV data.
- Separate storage layers from compute processing.
- Orchestrate the workflow using Apache Airflow.
- Use PySpark to transform and aggregate sales data.
- Calculate total sales and average order value.
- Demonstrate Spark lazy evaluation using execution-plan analysis.
- Store the processed output in the presentation layer.
- Configure a daily scheduled workflow.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing script |
| Apache Airflow 2.10.5 | Workflow orchestration |
| Apache Spark 3.5.3 | Data transformation |
| PySpark | Distributed data processing |
| Docker | Containerization |
| CSV | Input and output data format |
| PowerShell | Command-line operations |

## 4. Project Architecture

```text
             Overnight Sales CSV
                      |
                      v
               STAGING LAYER
              (overnight_sales.csv)
                      |
                      v
               APACHE AIRFLOW
              (Daily DAG Scheduler)
                      |
                      v
                DRIVER PROGRAM
              (DockerOperator)
                      |
                      v
                APACHE SPARK
                 (PySpark ETL)
                      |
                      v
              DATA TRANSFORMATION
              -------------------
              Calculate Order Sales
              Calculate Total Sales
              Calculate Average
              Order Value
                      |
                      v
              PRESENTATION LAYER
                      |
                      v
               Daily Sales Report
                    (CSV)
```

## 5. Project Structure

```text
assignment-13/
│
├── dags/
│   └── daily_sales_dag.py
│
├── scripts/
│   └── sales_transformation.py
│
├── staging/
│   └── overnight_sales.csv
│
├── presentation/
│   └── daily_sales_report/
│       ├── part-00000-*.csv
│       └── _SUCCESS
│
├── screen_shots/
│
├── docker-compose.yaml
│
└── README.md
```

## 6. Pipeline Workflow

### Step 1 – Batch Ingestion

The pipeline uses a static CSV file named `overnight_sales.csv` to simulate overnight sales data ingestion.

The file is stored in the staging layer.

### Step 2 – Workflow Orchestration

Apache Airflow manages the workflow through a DAG named:

`daily_sales_reporting`

The workflow is configured with a daily schedule using:

```python
schedule="@daily"
```

The `DockerOperator` launches a Spark container to execute the processing script.

### Step 3 – Data Transformation

The PySpark script reads the staging CSV file and calculates order-level sales.

**Order Sales Formula:**

```text
Order Sales = Quantity × Unit Price
```

### Step 4 – Business Metrics Calculation

The pipeline calculates:

**Total Sales**

```text
Total Sales = SUM(Order Sales)
```

**Average Order Value**

```text
Average Order Value = Total Sales / Total Orders
```

**Total Orders**

```text
Total Orders = COUNT(Order ID)
```

### Step 5 – Presentation Layer

The calculated metrics are written to the presentation layer in CSV format.

Spark generates a CSV output directory containing a data part file and a `_SUCCESS` marker.

## 7. Demonstrating Lazy Evaluation in Spark

Apache Spark uses lazy evaluation. Transformations are not immediately executed when they are defined.

In this project, the following transformations are created:

```python
orders_df = sales_df.withColumn(
    "order_sales",
    col("quantity") * col("unit_price")
)
```

The execution plan is examined using:

```python
orders_df.explain(mode="formatted")
```

This allows us to inspect the planned execution before triggering an action.

Execution is triggered using actions such as:

```python
metrics_df.show(truncate=False)
```

and:

```python
metrics_df.write.csv(output_path)
```

**Key concept:** Transformations build the execution plan, while actions trigger Spark computation.

## 8. Running the Project

### Prerequisites

- Docker Desktop installed and running.
- Apache Airflow configured through Docker Compose.
- Apache Spark Docker image available.
- Python and PySpark processing script.
- Windows PowerShell.

### Start Airflow

From the project directory:

```powershell
docker compose up -d
```

Open the Airflow dashboard:

```text
http://localhost:8080
```

### Monitor the DAG

1. Open the Airflow dashboard.
2. Locate `daily_sales_reporting`.
3. Enable the DAG if it is paused.
4. Trigger a manual run if required.
5. Monitor the `process_sales_data` task.
6. Verify that the task completes successfully.

### Verify the Output

```powershell
Get-ChildItem .\presentation\daily_sales_report
```

Read the generated CSV:

```powershell
Get-Content .\presentation\daily_sales_report\part-*.csv
```

## 9. Expected Deliverables

- Airflow DAG configuration.
- PySpark transformation script.
- Overnight sales staging CSV.
- Daily sales report in the presentation layer.
- Spark execution-plan evidence.
- Airflow orchestration dashboard screenshot.
- Python script execution output screenshot.
- Final presentation CSV screenshot.

## 10. Key Learning Outcomes

Through this assignment, the following data engineering concepts were implemented:

- Batch data ingestion.
- Data pipeline architecture.
- Separation of storage and compute.
- Apache Airflow DAG orchestration.
- Scheduled workflow execution.
- Docker-based Spark execution.
- PySpark transformations and aggregations.
- Spark lazy evaluation.
- Execution-plan inspection.
- Presentation-layer data generation.

## 11. Conclusion

This project demonstrates an automated daily sales reporting pipeline using Apache Airflow and PySpark.

It integrates batch ingestion, workflow orchestration, data transformation, business metric calculation, and output generation into a single workflow.

The implementation provides practical experience with essential data engineering concepts, particularly pipeline orchestration, Spark execution planning, and automated batch processing.

---

**Assignment:** 13 – Daily Sales Reporting Pipeline  
**Domain:** Data Engineering  
**Orchestration:** Apache Airflow  
**Processing Engine:** Apache Spark (PySpark)