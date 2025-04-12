from airflow import DAG
from airflow.providers.google.cloud.operators.pubsub import PubSubPublishMessageOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="pubsub_classic_operator",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["pubsub", "classic"],
) as dag:

    publish_message = PubSubPublishMessageOperator(
        task_id="publish_hello_world",
        project_id="meu-projeto-id",
        topic="meu-topico",
        messages=[{"data": "Hello from Airflow!"}],
    )
