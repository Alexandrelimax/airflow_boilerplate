from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta
from dataproc_batch_taskgroup import DataprocBatchTaskGroup  # caminho para o seu TaskGroup

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
BATCH_ID = "job-batch-etl"

default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": "gs://seu-bucket/scripts/etl.py",
        "args": [
            "--input", "gs://seu-bucket/input/",
            "--output", "gs://seu-bucket/output/"
        ],
    },
    "runtime_config": {
        "version": "2.2",
    },
    "environment_config": {
        "execution_config": {
            "subnetwork_uri": "default",
            "service_account": "sua-service-account@gcp.iam.gserviceaccount.com"
        }
    }
}

with DAG(
    dag_id="dataproc_batch_etl_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["dataproc", "batch", "serverless"],
) as dag:

    DataprocBatchTaskGroup(
        group_id="batch_taskgroup",
        project_id=PROJECT_ID,
        region=REGION,
        batch_id=BATCH_ID,
        batch_config=BATCH_CONFIG,
    )
