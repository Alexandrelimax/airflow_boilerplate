from airflow.decorators import dag
from airflow.utils.dates import days_ago
from dataproc_workflow_taskgroup import DataprocWorkflowTemplateTaskGroup  # salva esse TG nesse arquivo

template_config = {
    "placement": {
        "managed_cluster": {
            "cluster_name": "cluster-temporario",
            "config": {
                "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
                "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"}
            }
        }
    },
    "jobs": [
        {
            "pyspark_job": {
                "main_python_file_uri": "gs://meu-bucket/scripts/etl.py",
                "args": ["--input", "gs://...", "--output", "gs://..."]
            },
            "step_id": "pyspark-step"
        }
    ]
}

@dag(
    dag_id="dataproc_workflow_template_pipeline",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["dataproc", "workflow", "modern"],
)
def run_workflow():
    
    DataprocWorkflowTemplateTaskGroup(
        group_id="workflow_group",
        project_id="meu-projeto-id",
        region="us-central1",
        template_id="template-etl-pipeline",
        template_config=template_config
    )

dag = run_workflow()
