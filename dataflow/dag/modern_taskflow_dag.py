from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.dataflow import DataflowHook
from datetime import timedelta
import uuid

PROJECT_ID = 'seu-projeto-id'
REGION = 'us-central1'
TEMPLATE_BUCKET = 'seu-bucket-templates'
TEMPLATE_PATH = 'templates/uppercase-dataflow-template.json'

GCS_INPUT_PATH = 'gs://bucket-teste-saida/csv/data.csv'
BQ_OUTPUT_TABLE = 'dataset_teste.pessoas'

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
    tags=['dataflow', 'flex-template', 'modern', 'hook'],
)
def dataflow_flex_modern_pipeline():

    @task()
    def trigger_flex_template():
        job_name = f'dataflow-flex-modern-{uuid.uuid4()}'
        hook = DataflowHook(gcp_conn_id='google_cloud_default', location=REGION)

        hook.start_flex_template(
            project_id=PROJECT_ID,
            location=REGION,
            body={
                'launchParameter': {
                    'jobName': job_name,
                    'containerSpecGcsPath': f'gs://{TEMPLATE_BUCKET}/{TEMPLATE_PATH}',
                    'parameters': {
                        'input': GCS_INPUT_PATH,
                        'output_table': BQ_OUTPUT_TABLE,
                    }
                }
            },
        )

    trigger_flex_template()


dag = dataflow_flex_modern_pipeline()
