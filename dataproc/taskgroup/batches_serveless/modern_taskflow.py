from airflow.utils.task_group import TaskGroup
from airflow.decorators import task
from airflow.providers.google.cloud.hooks.dataproc import DataprocHook


class DataprocBatchTaskGroup(TaskGroup):
    def __init__(self, group_id: str, project_id: str, region: str, batch_id: str, batch_config: dict, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        @task(task_group=self)
        def create_batch_task() -> str:
            hook = DataprocHook()
            hook.create_batch(
                project_id=project_id,
                region=region,
                batch=batch_config,
                batch_id=batch_id
            )
            return batch_id

        @task(task_group=self)
        def wait_for_batch_task(batch_id: str):
            hook = DataprocHook()
            hook.wait_for_batch(
                batch_id=batch_id,
                region=region,
                project_id=project_id,
                wait_check_interval=10,
                timeout=900
            )
            return f"Batch {batch_id} completed."

        # Encadeia as tarefas
        batch = create_batch_task()
        wait_for_batch_task(batch)
