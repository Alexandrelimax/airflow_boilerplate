from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

PROJECT_ID = 'seu-projeto-id'
REGION = 'us-central1'
BUCKET_NAME = 'seu-bucket'
DATASET_ID = 'dataset_teste'
TABLE_ID = 'pessoas'

default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with models.DAG(
    dag_id='dataflow_csv_to_bigquery',
    default_args=default_args,
    schedule_interval=None,  # pode mudar para '@daily' etc
    catchup=False,
    tags=['dataflow', 'beam'],
) as dag:

    dataflow_task = DataflowCreatePythonJobOperator(
        task_id='run_beam_pipeline',
        py_file='gs://{}/dataflow/main.py'.format(BUCKET_NAME),  # precisa estar no GCS
        project_id=PROJECT_ID,
        location=REGION,
        job_name='dataflow-csv-to-bq-{{ ds_nodash }}',
        options={
            'input': f'gs://{BUCKET_NAME}/input/data.csv',
            'output_table': f'{PROJECT_ID}:{DATASET_ID}.{TABLE_ID}',
            'temp_location': f'gs://{BUCKET_NAME}/temp',
        },
    )
