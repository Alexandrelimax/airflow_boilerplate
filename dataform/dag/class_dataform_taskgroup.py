from airflow.decorators import dag
from airflow.utils.dates import days_ago
from taskgroups.dataform_taskgroup import DataformWorkflowTaskGroup
from taskgroups.gcs_load_taskgroup import GCSLoadTaskGroup
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'config/settings.json')) as f:
    config = json.load(f)

@dag(
    dag_id="full_pipeline_with_classes",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["gcs", "bigquery", "dataform", "modular"],
)
def pipeline():

    GCSLoadTaskGroup(
        group_id="load_to_bronze",
        project_id=config["project_id"],
        dataset_id=config["bigquery"]["dataset"],
        bucket_name=config["bucket"],
        files=config["files"]
    )

    DataformWorkflowTaskGroup(
        group_id="run_dataform",
        project_id=config["project_id"],
        region=config["region"],
        repository_id=config["repository_id"],
        branch=config["branch"]
    )

dag = pipeline()