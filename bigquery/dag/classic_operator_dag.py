from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="bq_classic_query",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=["bigquery", "classic"],
) as dag:

    bq_query = BigQueryInsertJobOperator(
        task_id="run_query",
        configuration={
            "query": {
                "query": "SELECT name, SUM(sales) as total_sales FROM `meu-projeto.minha_dataset.vendas` GROUP BY name",
                "useLegacySql": False,
            }
        },
        location="US",
    )
