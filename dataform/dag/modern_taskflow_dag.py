import json
from pathlib import Path
from datetime import timedelta
from airflow.decorators import dag, task, task_group
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.hooks.dataform import DataformHook


CONFIG_PATH = Path('include/config/settings.json')

with open(CONFIG_PATH, 'r') as file:
    CONFIG = json.load(file)

@dag(
    dag_id="gcs_to_bq_dataform_taskflow",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=["dataform", "bronze", "taskflow"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
)
def pipeline():

    @task_group(group_id="load_to_bronze")
    def load_to_bronze():
        for item in CONFIG["gcs"]["files"]:

            @task(task_id=f"load_{item['table']}")
            def load_csv_to_bq(table: str, file_path: str):
                client = BigQueryHook().get_client()
                uri = f"gs://{CONFIG['gcs']['bucket']}/{file_path}"
                job_config = {
                    "configuration": {
                        "load": {
                            "sourceUris": [uri],
                            "destinationTable": {
                                "projectId": CONFIG["dataform"]["project_id"],
                                "datasetId": CONFIG["bigquery"]["dataset"],
                                "tableId": table
                            },
                            "sourceFormat": "CSV",
                            "skipLeadingRows": 1,
                            "autodetect": True,
                            "writeDisposition": "WRITE_TRUNCATE"
                        }
                    }
                }

                client.insert_job(
                    projectId=CONFIG["dataform"]["project_id"],
                    body=job_config
                )

            load_csv_to_bq(table=item["table"], file_path=item["file"])

    @task_group(group_id="run_dataform")
    def run_dataform():

        @task()
        def compile_code() -> str:
            hook = DataformHook()
            result = hook.create_compilation_result(
                project_id=CONFIG["dataform"]["project_id"],
                region=CONFIG["dataform"]["region"],
                repository_id=CONFIG["dataform"]["repository_id"],
                compilation_result={"git_commitish": CONFIG["dataform"]["branch"]},
            )
            return result.name

        @task()
        def invoke_workflow(compilation_result_name: str) -> str:
            hook = DataformHook()

            result = hook.create_workflow_invocation(
                project_id=CONFIG["dataform"]["project_id"],
                region=CONFIG["dataform"]["region"],
                repository_id=CONFIG["dataform"]["repository_id"],
                workflow_invocation={"compilation_result": compilation_result_name},
            )
            return result.name

        @task()
        def wait_for_completion(invocation_id: str):
            hook = DataformHook()
            workflow_invocation_id = invocation_id.split("/")[-1]
            
            hook.wait_for_workflow_invocation(
                workflow_invocation_id=workflow_invocation_id,
                repository_id=CONFIG["dataform"]["repository_id"],
                project_id=CONFIG["dataform"]["project_id"],
                region=CONFIG["dataform"]["region"],
                wait_time=10,
                timeout=600,
            )

        compilation_name = compile_code()
        invocation_name = invoke_workflow(compilation_name)
        wait_for_completion(invocation_name)

    load_to_bronze() >> run_dataform()

dag = pipeline()
