from airflow.utils.task_group import TaskGroup
from airflow.decorators import task
from airflow.providers.google.cloud.hooks.dataproc import DataprocHook


class DataprocWorkflowTemplateTaskGroup(TaskGroup):
    def __init__(self, group_id: str, project_id: str, region: str, template_id: str, template_config: dict, **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        @task(task_group=self)
        def create_template_task():
            hook = DataprocHook()
            # O nome precisa ser adicionado ao dicionário do template
            template_config["id"] = template_id
            hook.create_workflow_template(
                project_id=project_id,
                region=region,
                template=template_config
            )
            return template_id

        @task(task_group=self)
        def instantiate_template_task(template_id: str):
            hook = DataprocHook()
            hook.instantiate_workflow_template(
                template_name=template_id,
                project_id=project_id,
                region=region
            )
            return f"Workflow {template_id} started."

        # Encadeamento
        created_template = create_template_task()
        instantiate_template_task(created_template)
