from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.cloud_run import CloudRunHook
from datetime import timedelta
import uuid

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
JOB_NAME = "cloud-run-job-demo"  # Job precisa estar criado no Cloud Run

@dag(
    dag_id="cloud_run_job_hook_dag",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
    tags=["cloud-run", "job"],
)
def cloud_run_job_dag():

    @task()
    def execute_job():
        hook = CloudRunHook(gcp_conn_id="google_cloud_default")
        run_id = f"{JOB_NAME}-{uuid.uuid4()}"
        hook.execute_job(
            job_name=JOB_NAME,
            region=REGION,
            project_id=PROJECT_ID,
            overrides={"env": {"EXECUTION_ID": run_id}},
        )
        print(f"Job {JOB_NAME} executado com sucesso.")

    execute_job()

dag = cloud_run_job_dag()
