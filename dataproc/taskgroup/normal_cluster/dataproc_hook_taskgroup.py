from airflow.utils.task_group import TaskGroup
from airflow.decorators import task
from airflow.providers.google.cloud.hooks.dataproc import DataprocHook


class DataprocHookTaskGroup(TaskGroup):
    def __init__(self, group_id: str, project_id: str, region: str, cluster_name: str, cluster_config: dict, job_config: dict, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        @task(task_group=self)
        def create_cluster_task():
            hook = DataprocHook()
            hook.create_cluster(
                project_id=project_id,
                region=region,
                cluster_name=cluster_name,
                cluster_config=cluster_config
            )
            return f"{cluster_name}"

        @task(task_group=self)
        def submit_job_task(cluster_name: str) -> str:
            hook = DataprocHook()
            job_config["placement"] = {"cluster_name": cluster_name}
            job_response = hook.submit_job(
                project_id=project_id,
                region=region,
                job=job_config,
            )
            return job_response.reference.job_id

        @task(task_group=self)
        def wait_for_job_task(job_id: str):
            hook = DataprocHook()
            hook.wait_for_job(
                job_id=job_id,
                project_id=project_id,
                region=region,
                wait_time=10,
                timeout=600,
            )
            return f"Job {job_id} finished."

        @task(task_group=self, trigger_rule="all_done")
        def delete_cluster_task(cluster_name: str):
            hook = DataprocHook()
            hook.delete_cluster(
                project_id=project_id,
                region=region,
                cluster_name=cluster_name
            )
            return f"Cluster {cluster_name} deleted."

        # Encadeando as tarefas
        cluster = create_cluster_task()
        job_id = submit_job_task(cluster)
        wait = wait_for_job_task(job_id)
        delete_cluster_task(cluster)  # Executa mesmo em falha no job
