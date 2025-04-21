from airflow.decorators import dag
from airflow.utils.dates import days_ago
from dataproc_taskgroup import DataprocJobTaskGroup


project_id = "seu-projeto-id"
region = "us-central1"
cluster_name = "meu-cluster-temp"

cluster_config = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-2",
    },
}

job_config = {
    "placement": {"cluster_name": cluster_name},
    "pyspark_job": {
        "main_python_file_uri": "gs://meu-bucket/pyspark/meu_script.py",
    },
}



@dag(
    dag_id="dataproc_taskgroup_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dataproc", "taskgroup"],
)
def dataproc_dag():

    DataprocJobTaskGroup(
        group_id="dataproc_pipeline",
        project_id=project_id,
        region=region,
        cluster_name=cluster_name,
        job_config=job_config,
        cluster_config=cluster_config,
    )

dag = dataproc_dag()
