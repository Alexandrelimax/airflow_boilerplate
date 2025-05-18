import json
from pathlib import Path
from airflow.decorators import dag
from airflow.utils.dates import days_ago
from taskgroups.dataform_taskgroup import DataformWorkflowTaskGroup
from taskgroups.gcs_load_taskgroup import GCSLoadTaskGroup

CONFIG_PATH = Path('include/config/settings.json')

with open(CONFIG_PATH, 'r') as file:
    CONFIG = json.load(file)

@dag(
    dag_id="pipeline_dataform",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=["gcs", "bigquery", "dataform", "modular"],
)
def pipeline_dataform():
    
    GCSLoadTaskGroup(
        group_id="load_to_bronze",
        project_id=CONFIG["cloud_storage"]["project_id"],
        dataset_id=CONFIG["cloud_storage"]["dataset"],
        bucket_name=CONFIG["cloud_storage"]["bucket"],
        files=CONFIG["cloud_storage"]["files"]
    )

    DataformWorkflowTaskGroup(
        group_id="run_dataform",
        project_id=CONFIG["dataform"]["project_id"],
        region=CONFIG["dataform"]["region"],
        repository_id=CONFIG["dataform"]["repository_id"],
        branch=CONFIG["dataform"]["branch"]
    )

dag = pipeline_dataform()