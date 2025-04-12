from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.cloud_run import CloudRunServiceHook
from datetime import timedelta
import requests

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
SERVICE_NAME = "cloud-run-fastapi-demo"

@dag(
    dag_id="cloud_run_service_hook_dag",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
    tags=["cloud-run", "service"],
)
def cloud_run_service_dag():

    @task()
    def call_service():
        hook = CloudRunServiceHook(gcp_conn_id="google_cloud_default")
        service = hook.get_service(service_name=SERVICE_NAME, region=REGION, project_id=PROJECT_ID)

        url = service["status"]["url"]
        print(f"URL do serviço: {url}")

        response = requests.get(url)
        print("Status:", response.status_code)
        print("Body:", response.text)

    call_service()

dag = cloud_run_service_dag()
