from airflow import models
from airflow.providers.google.cloud.operators.run import CloudRunJobOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
SERVICE_NAME = "cloud-run-fastapi-demo"

default_args = {
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with models.DAG(
    dag_id="cloud_run_call_operator",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["cloud-run"],
) as dag:

    call_cloud_run = CloudRunJobOperator(
        task_id="call_cloud_run_service",
        project_id=PROJECT_ID,
        region=REGION,
        job_name=SERVICE_NAME,
        launch_stage="BETA",
        gcp_conn_id="google_cloud_default",
    )
