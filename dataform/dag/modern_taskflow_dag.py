from airflow.decorators import dag, task, task_group
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.hooks.dataform import DataformHook
from airflow.utils.task_group import TaskGroup
from datetime import timedelta
import json
import os

# Load settings from external config file
with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as f:
    config = json.load(f)

@dag(
    dag_id="gcs_to_bq_dataform_taskflow",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dataform", "bronze", "taskflow"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
)
def pipeline():

    @task_group(group_id="load_to_bronze")
    def load_to_bronze():
        for item in config["gcs"]["files"]:

            @task(task_id=f"load_{item['table']}")
            def load_csv_to_bq(table: str, file_path: str):
                client = BigQueryHook().get_client()
                uri = f"gs://{config['gcs']['bucket']}/{file_path}"
                job_config = {
                    "configuration": {
                        "load": {
                            "sourceUris": [uri],
                            "destinationTable": {
                                "projectId": config["dataform"]["project_id"],
                                "datasetId": config["bigquery"]["dataset"],
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
                    projectId=config["dataform"]["project_id"],
                    body=job_config
                )

            load_csv_to_bq(table=item["table"], file_path=item["file"])

    @task_group(group_id="run_dataform")
    def run_dataform():

        @task()
        def compile_code() -> str:
            hook = DataformHook()
            result = hook.create_compilation_result(
                project_id=config["dataform"]["project_id"],
                region=config["dataform"]["region"],
                repository_id=config["dataform"]["repository_id"],
                compilation_result={"git_commitish": config["dataform"]["branch"]},
            )
            return result["name"].split("/")[-1]

        @task()
        def invoke_workflow(compilation_result_id: str) -> str:
            hook = DataformHook()
            full_compilation_uri = config["dataform"]["compilation_uri_prefix"] + compilation_result_id
            result = hook.create_workflow_invocation(
                project_id=config["dataform"]["project_id"],
                region=config["dataform"]["region"],
                repository_id=config["dataform"]["repository_id"],
                workflow_invocation={"compilation_result": full_compilation_uri},
            )
            return result["name"].split("/")[-1]

        @task()
        def wait_for_completion(invocation_id: str):
            hook = DataformHook()
            hook.wait_for_workflow_invocation(
                workflow_invocation_id=invocation_id,
                repository_id=config["dataform"]["repository_id"],
                project_id=config["dataform"]["project_id"],
                region=config["dataform"]["region"],
                wait_time=10,
                timeout=600,
            )

        comp_id = compile_code()
        inv_id = invoke_workflow(comp_id)
        wait_for_completion(inv_id)

    load_to_bronze() >> run_dataform()

dag = pipeline()
