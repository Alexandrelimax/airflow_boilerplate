from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

with DAG(
    dag_id='cloud_run_http_operator_dag',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["cloud-run", "http"],
) as dag:

    call_root = SimpleHttpOperator(
        task_id='call_cloud_run_root',
        http_conn_id='cloud_run_service_http',  # definida nas Connections do Airflow
        endpoint='/',
        method='GET',
        response_check=lambda response: response.status_code == 200,
        log_response=True,
    )
