from airflow.utils.task_group import TaskGroup
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateWorkflowTemplateOperator,
    DataprocInstantiateWorkflowTemplateOperator,
)
from airflow.operators.empty import EmptyOperator
import uuid


class DataprocWorkflowTemplateTaskGroup(TaskGroup):
    def __init__(self, group_id: str, project_id: str, region: str, template_id: str, workflow_template: dict, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        start = EmptyOperator(task_id="start", task_group=self)

        create_template = DataprocCreateWorkflowTemplateOperator(
            task_id="create_template",
            project_id=project_id,
            region=region,
            template=workflow_template,
            task_group=self,
        )

        run_template = DataprocInstantiateWorkflowTemplateOperator(
            task_id="run_template",
            project_id=project_id,
            region=region,
            template_id=template_id,
            task_group=self,
        )

        start >> create_template >> run_template
