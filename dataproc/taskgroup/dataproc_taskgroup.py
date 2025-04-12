from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
)


class DataprocJobTaskGroup(TaskGroup):
    def __init__(self, group_id: str, project_id: str, region: str, cluster_name: str, job_config: dict, cluster_config: dict, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        create_cluster = DataprocCreateClusterOperator(
            task_id="create_cluster",
            project_id=project_id,
            region=region,
            cluster_name=cluster_name,
            cluster_config=cluster_config,
        )

        submit_job = DataprocSubmitJobOperator(
            task_id="submit_job",
            job=job_config,
            project_id=project_id,
            region=region,
        )

        delete_cluster = DataprocDeleteClusterOperator(
            task_id="delete_cluster",
            project_id=project_id,
            region=region,
            cluster_name=cluster_name,
            trigger_rule="all_done",
        )

        create_cluster >> submit_job >> delete_cluster
