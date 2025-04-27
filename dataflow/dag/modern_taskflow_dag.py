from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.dataflow import DataflowHook
from datetime import timedelta
import json
from pathlib import Path
from uuid import uuid4

# Atualizado para carregar JSON
CONFIG_PATH = Path('include/config/settings.json')

with open(CONFIG_PATH, 'r') as file:
    CONFIG = json.load(file)

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='dataflow_flex_csv_to_bigquery_modern',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=['dataflow', 'flex-template', 'modern', 'hook'],
)
def dataflow_flex_modern_pipeline():

    @task()
    def trigger_flex_template():
        job_name = f"dataflow-flex-modern-{uuid4()}"
        
        hook = DataflowHook(
            gcp_conn_id='google_cloud_default', 
            location=CONFIG['dataflow']['region']
        )

        hook.start_flex_template(
            project_id=CONFIG['dataflow']['project_id'],
            location=CONFIG['dataflow']['region'],
            body = {
                "launchParameter": {
                    "jobName": job_name,
                    "containerSpecGcsPath": f"gs://{CONFIG['dataflow']['bucket_name']}/{CONFIG['dataflow']['template_path']}",
                    "parameters": {
                        "input": CONFIG['dataflow']['input_path'],
                        "output_table": CONFIG['dataflow']['output_table']
                    },
                    "environment": {
                        "serviceAccountEmail": CONFIG['dataflow']['service_account_email'],
                        "tempLocation": CONFIG['dataflow']['temp_location'],
                        "autoscalingAlgorithm": CONFIG['dataflow']['autoscaling_algorithm'],
                        "numWorkers": CONFIG['dataflow']['num_workers'],
                        "maxWorkers": CONFIG['dataflow']['max_workers'],
                        "machineType": CONFIG['dataflow']['machine_type'],
                        "network": CONFIG['dataflow']['vpc'],
                        "subnetwork": CONFIG['dataflow']['subnetwork']
                    }
                }
            }
        )

    trigger_flex_template()

dataflow_flex_modern_pipeline()
