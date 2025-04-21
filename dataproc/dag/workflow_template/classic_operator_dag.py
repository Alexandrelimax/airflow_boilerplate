from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta
import uuid

from dataproc_template_taskgroup import DataprocWorkflowTemplateTaskGroup

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
BUCKET = "seu-bucket"
SCRIPT = "scripts/etl.py"

TEMPLATE_ID = f"etl-template-{uuid.uuid4().hex[:6]}"

WORKFLOW_TEMPLATE = {
    "id": TEMPLATE_ID,
    "placement": {
        "managed_cluster": {
            "cluster_name": f"cluster-temp-{uuid.uuid4().hex[:4]}",
            "config": {
                "master_config": {
                    "num_instances": 1,
                    "machine_type_uri": "n1-standard-2",
                },
                "worker_config": {
                    "num_instances": 2,
                    "machine_type_uri": "n1-standard-2",
                },
            },
        }
    },
    "jobs": [
        {
            "step_id": "run-etl",
            "pyspark_job": {
                "main_python_file_uri": f"gs://{BUCKET}/{SCRIPT}",
                "args": [
                    "--input", f"gs://{BUCKET}/input/",
                    "--output", f"gs://{BUCKET}/output/"
                ]
            },
        }
    ],
}

default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dataproc_workflow_template_classic",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["dataproc", "workflow", "classic"],
) as dag:

    workflow_group = DataprocWorkflowTemplateTaskGroup(
        group_id="workflow_template",
        project_id=PROJECT_ID,
        region=REGION,
        template_id=TEMPLATE_ID,
        workflow_template=WORKFLOW_TEMPLATE,
    )
