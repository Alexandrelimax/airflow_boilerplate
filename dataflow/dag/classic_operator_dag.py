from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

PROJECT_ID = 'seu-projeto-id'
REGION = 'us-central1'
BUCKET_NAME = 'seu-bucket-templates'
TEMPLATE_PATH = 'templates/uppercase-dataflow-template.json'
GCS_INPUT_PATH = 'gs://bucket/csv/data.csv'
BQ_OUTPUT_TABLE = 'dataset_teste.pessoas'

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
    tags=['dataflow', 'beam', 'flex-template'],
) as dag:

    run_flex_template = DataflowStartFlexTemplateOperator(
        task_id='run_flex_template_pipeline',
        project_id=PROJECT_ID,
        location=REGION,
        body={
            'launchParameter': {
                'jobName': 'flex-csv-to-bq-{{ ds_nodash }}',
                'containerSpecGcsPath': f'gs://{BUCKET_NAME}/{TEMPLATE_PATH}',
                'parameters': {
                    'input': GCS_INPUT_PATH,
                    'output_table': BQ_OUTPUT_TABLE,
                }
            }
        }
    )
