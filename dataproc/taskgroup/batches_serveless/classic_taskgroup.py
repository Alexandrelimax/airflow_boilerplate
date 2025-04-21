from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.providers.google.cloud.sensors.dataproc import DataprocBatchSensor


class DataprocBatchTaskGroup(TaskGroup):
    def __init__(self, group_id: str, project_id: str, region: str, batch_id: str, batch_config: dict, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        create_batch = DataprocCreateBatchOperator(
            task_id="create_batch",
            project_id=project_id,
            region=region,
            batch_id=batch_id,
            batch=batch_config,
            task_group=self
        )

        wait_batch = DataprocBatchSensor(
            task_id="wait_batch",
            project_id=project_id,
            region=region,
            batch_id=batch_id,
            poke_interval=30,
            task_group=self
        )

        create_batch >> wait_batch
