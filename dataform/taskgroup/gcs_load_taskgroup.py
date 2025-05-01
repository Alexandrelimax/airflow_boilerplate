from airflow.utils.task_group import TaskGroup
from airflow.decorators import task
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

class GCSLoadTaskGroup(TaskGroup):
    def __init__(self, group_id, project_id, dataset_id, bucket_name, files: list, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        for item in files:
            self._create_load_task(
                table=item["table"],
                file_path=item["file"],
                project_id=project_id,
                dataset_id=dataset_id,
                bucket_name=bucket_name
            )

    def _create_load_task(self, table, file_path, project_id, dataset_id, bucket_name):
        @task(task_id=f"load_{table}", task_group=self)
        def load_csv_to_bq():
            client = BigQueryHook().get_client()
            uri = f"gs://{bucket_name}/{file_path}"
            job_config = {
                "configuration": {
                    "load": {
                        "sourceUris": [uri],
                        "destinationTable": {
                            "projectId": project_id,
                            "datasetId": dataset_id,
                            "tableId": table
                        },
                        "sourceFormat": "CSV",
                        "skipLeadingRows": 1,
                        "autodetect": True,
                        "writeDisposition": "WRITE_TRUNCATE"
                    }
                }
            }
            client.insert_job(projectId=project_id, body=job_config)

        load_csv_to_bq()
