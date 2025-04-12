from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.functions import CloudFunctionsHook
from datetime import timedelta

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
FUNCTION_NAME = "hello-world-function"

@dag(
    dag_id="cloud_function_modern_hook_dag",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
    tags=["cloud-function", "modern"],
)
def cloud_function_dag():

    @task()
    def call_cloud_function():
        hook = CloudFunctionsHook(gcp_conn_id="google_cloud_default")
        result = hook.call_function(
            project_id=PROJECT_ID,
            location=REGION,
            function_id=FUNCTION_NAME,
            input_data={"caller": "Airflow modern"},
        )
        print("Function result:", result)

    call_cloud_function()

dag = cloud_function_dag()
