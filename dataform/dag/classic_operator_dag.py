import json
from pathlib import Path
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.dataform import (
    DataformCreateCompilationResultOperator,
    DataformCreateWorkflowInvocationOperator,
)
from airflow.decorators import task
CONFIG_PATH = Path('include/config/settings.json')

with open(CONFIG_PATH, 'r') as file:
    CONFIG = json.load(file)

with DAG(
    dag_id="dataform_dag_operators",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=["dataform", "bigquery", "bronze"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
) as dag:

    

    @task
    def extract_compilation_result_name(compilation_result: dict) -> str:
        return compilation_result["name"]

    with TaskGroup(group_id="run_dataform", tooltip="Compilar e rodar projeto no Dataform") as dataform_group:

        create_compilation_result = DataformCreateCompilationResultOperator(
            task_id="create-compilation-result",
            project_id=CONFIG['dataform']["project_id"],
            region=CONFIG['dataform']["region"],
            repository_id=CONFIG['dataform']["repository_id"],
            compilation_result={
                "git_commitish": CONFIG['dataform']["branch"],
                # "workspace": CONFIG['dataform']["workspace"],
            }
        )
        extract_name = extract_compilation_result_name(create_compilation_result.output)

        create_workflow_invocation = DataformCreateWorkflowInvocationOperator(
            task_id="create-workflow-invocation",
            project_id=CONFIG['dataform']["project_id"],
            region=CONFIG['dataform']["region"],
            repository_id=CONFIG['dataform']["repository_id"],
            workflow_invocation={
                "compilation_result": extract_name
            },
        )

        create_compilation_result >>  extract_name >> create_workflow_invocation

    dataform_group

