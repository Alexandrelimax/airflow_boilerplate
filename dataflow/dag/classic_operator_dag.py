from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import yaml
from pathlib import Path
from uuid import uuid4

# Load config.yaml
CONFIG_PATH = Path('include/config/config.yaml')

with open(CONFIG_PATH, 'r') as f:
    CONFIG = yaml.safe_load(f)

default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with models.DAG(
    dag_id='dataflow_flex_csv_to_bigquery',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=['dataflow', 'beam', 'flex-template'],
) as dag:

    run_flex_template = DataflowStartFlexTemplateOperator(
        task_id='run_flex_template_pipeline',
        project_id=CONFIG['dataflow']['project_id'],
        location=CONFIG['dataflow']['region'],
        body={
            'launchParameter': {
                'jobName': f'dataflow-classic-{uuid4().hex}',
                'containerSpecGcsPath': f"gs://{CONFIG['dataflow']['bucket_name']}/{CONFIG['dataflow']['template_path']}",
                "parameters": {
                    "input": CONFIG['dataflow']['input_path'],
                    "output_table": CONFIG['dataflow']['output_table']
                },
                "environment": {
                    "serviceAccountEmail": CONFIG['dataflow']['service_account_email'],
                    "tempLocation": CONFIG['dataflow']['temp_location'],
                    "autoscalingAlgorithm": CONFIG['dataflow']['autoscaling_algorithm'],  
                    "machineType": CONFIG['dataflow']['machine_type'], 
                    "numWorkers": CONFIG['dataflow']['num_workers'],
                    "maxWorkers": CONFIG['dataflow']['max_workers'],
                    "network": CONFIG['dataflow']['vpc'],              
                    "subnetwork": CONFIG['dataflow']['subnetwork']     
                    }
            }
        }
    )
