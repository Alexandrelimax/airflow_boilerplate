from datetime import timedelta
import json
import os
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.dataform import (
    DataformCreateCompilationResultOperator,
    DataformCreateWorkflowInvocationOperator,
)

# Carrega configurações do JSON externo
with open(os.path.join(os.path.dirname(__file__), "settings_gcs_to_dataform.json")) as f:
    config = json.load(f)

with DAG(
    dag_id="gcs_to_bq_then_run_dataform",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dataform", "bigquery", "bronze"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
) as dag:

    # TaskGroup: carregar arquivos CSV para o BigQuery
    with TaskGroup(group_id="load_csvs_to_bronze") as load_group:
        for item in config["files"]:
            GCSToBigQueryOperator(
                task_id=f"load_{item['table']}",
                bucket=config["bucket"],
                source_objects=[item["file"]],
                destination_project_dataset_table=f"{config['project_id']}.{config['dataset']}.{item['table']}",
                source_format="CSV",
                skip_leading_rows=1,
                autodetect=True,
                write_disposition="WRITE_TRUNCATE",
                gcp_conn_id="google_cloud_default",
            )

    # TaskGroup: compilar e rodar workflow no Dataform
    with TaskGroup(group_id="run_dataform") as dataform_group:

        compile_code = DataformCreateCompilationResultOperator(
            task_id="compile_code",
            project_id=config["project_id"],
            region=config["region"],
            repository_id=config["repository_id"],
            compilation_result={"git_commitish": config["branch"]},
        )

        run_workflow = DataformCreateWorkflowInvocationOperator(
            task_id="run_workflow",
            project_id=config["project_id"],
            region=config["region"],
            repository_id=config["repository_id"],
            workflow_invocation={
                "compilation_result": "{{ task_instance.xcom_pull(task_ids='run_dataform.compile_code') }}"
            },
        )

        compile_code >> run_workflow

    load_group >> dataform_group
