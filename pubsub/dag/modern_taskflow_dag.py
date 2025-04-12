from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.pubsub import PubSubHook
from airflow.utils.dates import days_ago

@dag(
    dag_id="pubsub_modern_taskflow",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["pubsub", "modern"],
)
def pubsub_taskflow():

    @task
    def publish():
        hook = PubSubHook()
        hook.publish(
            topic="projects/meu-projeto-id/topics/meu-topico",
            messages=[{"data": "Mensagem moderna com Hook"}]
        )

    publish()

dag = pubsub_taskflow()
