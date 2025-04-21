from airflow.decorators import dag
from airflow.utils.dates import days_ago
from dataproc_batch_taskgroup import DataprocBatchTaskGroup  # supondo que esteja salvo em um arquivo separado

batch_config = {
    "pyspark_batch": {
        "main_python_file_uri": "gs://meu-bucket/scripts/etl.py",
        "args": ["--input", "gs://input.csv", "--output", "gs://output/"]
    },
    "environment_config": {
        "execution_config": {
            "service_account": "meu-sa@meu-projeto-id.iam.gserviceaccount.com"
        }
    }
}

@dag(
    dag_id="dataproc_batch_pipeline",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["dataproc", "batch", "modern"],
)
def run_batch_job():
    DataprocBatchTaskGroup(
        group_id="batch_group",
        project_id="meu-projeto-id",
        region="us-central1",
        batch_id="batch-job-id",
        batch_config=batch_config
    )

dag = run_batch_job()