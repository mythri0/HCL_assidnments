
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

PROJECT_PATH = (
    "C:/Users/Administrator/Desktop/"
    "aws-sales-etl-pyspark/assignment-13"
)

default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="daily_sales_reporting",
    default_args=default_args,
    description="Daily sales reporting using Airflow and PySpark",
    start_date=datetime(2026, 11, 1),
    schedule="@daily",
    catchup=False,
    tags=["sales", "pyspark", "assignment-13"],
) as dag:

    process_sales = DockerOperator(
        task_id="process_sales_data",
        image="apache/spark:3.5.3",
        api_version="auto",
        auto_remove="never",
        command=(
            "/opt/spark/bin/spark-submit "
            "/opt/spark/scripts/sales_transformation.py"
        ),
        docker_url="unix://var/run/docker.sock",
        network_mode="assignment-13_default",
        mounts=[
            Mount(
                source=f"{PROJECT_PATH}/staging",
                target="/opt/spark/staging",
                type="bind",
                read_only=True,
            ),
            Mount(
                source=f"{PROJECT_PATH}/scripts",
                target="/opt/spark/scripts",
                type="bind",
                read_only=True,
            ),
            Mount(
                source=f"{PROJECT_PATH}/presentation",
                target="/opt/spark/presentation",
                type="bind",
            ),
        ],
        mount_tmp_dir=False,
    )
