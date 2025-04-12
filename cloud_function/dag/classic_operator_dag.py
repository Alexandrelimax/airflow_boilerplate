from airflow import DAG
from airflow.providers.google.cloud.operators.functions import CloudFunctionInvokeFunctionOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

PROJECT_ID = "seu-projeto-id"
LOCATION = "us-central1"
FUNCTION_NAME = "hello-world-function"

with DAG(
    dag_id="cloud_function_classic_operator_dag",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["cloud-function", "classic"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
) as dag:

    invoke_function = CloudFunctionInvokeFunctionOperator(
        task_id="invoke_cloud_function",
        project_id=PROJECT_ID,
        location=LOCATION,
        input_data={"caller": "Airflow"},
        function_id=FUNCTION_NAME,
        gcp_conn_id="google_cloud_default",
    )
