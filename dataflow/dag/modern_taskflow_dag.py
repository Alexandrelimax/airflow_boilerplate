from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.dataflow import DataflowHook
from datetime import timedelta
import uuid

PROJECT_ID = 'seu-projeto-id'
REGION = 'us-central1'
BUCKET_NAME = 'seu-bucket'
DATASET_ID = 'dataset_teste'
TABLE_ID = 'pessoas'

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


@dag(
    dag_id='dataflow_csv_to_bigquery_modern',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['dataflow', 'modern', 'hook'],
)
def dataflow_modern_pipeline():

    @task()
    def trigger_dataflow_job():
        job_name = f'dataflow-modern-{uuid.uuid4()}'
        dataflow = DataflowHook(gcp_conn_id='google_cloud_default', location=REGION)

        dataflow.start_python_dataflow(
            job_name=job_name,
            variables={
                'input': f'gs://{BUCKET_NAME}/input/data.csv',
                'output_table': f'{PROJECT_ID}:{DATASET_ID}.{TABLE_ID}',
                'temp_location': f'gs://{BUCKET_NAME}/temp',
            },
            py_file=f'gs://{BUCKET_NAME}/dataflow/main.py',
            project_id=PROJECT_ID,
            py_options=[],
        )

    trigger_dataflow_job()


dag = dataflow_modern_pipeline()
