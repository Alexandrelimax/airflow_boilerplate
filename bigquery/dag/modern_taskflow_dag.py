from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.dates import days_ago

@dag(
    dag_id="bq_hook_taskflow",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["bigquery", "hook", "modern"],
)
def bq_hook_example():

    @task
    def run_query():
        hook = BigQueryHook()
        sql = """
        SELECT state, COUNT(*) AS total
        FROM `meu-projeto.minha_dataset.clientes`
        GROUP BY state
        """
        hook.run_query(sql=sql, location="US")

    run_query()

dag = bq_hook_example()
