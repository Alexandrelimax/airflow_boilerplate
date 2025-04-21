from airflow.decorators import dag
from airflow.utils.dates import days_ago
from dataproc_hook_taskgroup import DataprocHookTaskGroup



cluster_config={
    "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
    "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
}

job_config={
    "pyspark_job": {
        "main_python_file_uri": "gs://meu-bucket/scripts/etl.py",
        "args": ["--input", "gs://...", "--output", "gs://..."],
    }
}


@dag(
    dag_id="dataproc_hook_dag",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["dataproc", "hook", "modern"],
)
def run_dataproc():

    DataprocHookTaskGroup(
        group_id="hook_pipeline",
        project_id="meu-projeto-id",
        region="us-central1",
        cluster_name="cluster-temp",
        cluster_config=cluster_config,
        job_config=job_config,
    )

dag = run_dataproc()
