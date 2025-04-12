from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataform import (
    DataformCreateCompilationResultOperator,
    DataformCreateWorkflowInvocationOperator,
)
from airflow.operators.python import PythonOperator
from datetime import timedelta

PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
REPOSITORY_ID = "meu-repositorio-dataform"
WORKSPACE_ID = "meu-workspace-id"
BRANCH_NAME = "main"

with DAG(
    dag_id="dataform_compile_and_run_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dataform", "bigquery"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
) as dag:

    # 1️⃣ Cria um resultado de compilação (congela o estado do repo na branch)
    compile_code = DataformCreateCompilationResultOperator(
        task_id="compile_dataform_code",
        project_id=PROJECT_ID,
        region=REGION,
        repository_id=REPOSITORY_ID,
        compilation_result={"git_commitish": BRANCH_NAME},
    )

    # 2️⃣ Executa o projeto compilado como um workflow
    run_compiled_code = DataformCreateWorkflowInvocationOperator(
        task_id="run_dataform_workflow",
        project_id=PROJECT_ID,
        region=REGION,
        repository_id=REPOSITORY_ID,
        workflow_invocation={"compilation_result": "{{ task_instance.xcom_pull(task_ids='compile_dataform_code') }}"},
    )

    compile_code >> run_compiled_code
