from airflow.utils.task_group import TaskGroup
from airflow.decorators import task
from airflow.providers.google.cloud.hooks.dataform import DataformHook


class DataformWorkflowTaskGroup(TaskGroup):
    def __init__(self, group_id, project_id, region, repository_id, branch="main", **kwargs):
        super().__init__(group_id=group_id, **kwargs)

        @task(task_group=self)
        def create_compilation_result():
            hook = DataformHook()
            compilation_result = {
                "git_commitish": branch
            }
            result = hook.create_compilation_result(
                project_id=project_id,
                region=region,
                repository_id=repository_id,
                compilation_result=compilation_result
            )
            name = result.name
            print(f"✅ Compilation created: {name}")
            return name

        @task(task_group=self)
        def start_workflow_invocation(compilation_result_name: str):
            hook = DataformHook()
            workflow_invocation = {
                "compilation_result": compilation_result_name
            }
            result = hook.create_workflow_invocation(
                project_id=project_id,
                region=region,
                repository_id=repository_id,
                workflow_invocation=workflow_invocation
            )
            name = result.name
            print(f"🚀 Workflow started: {name}")
            return name

        @task(task_group=self)
        def monitor_workflow_invocation(workflow_invocation_name: str):
            hook = DataformHook()
            print(f"⏳ Waiting for workflow to complete: {workflow_invocation_name}")
            
            workflow_invocation_id = workflow_invocation_name.split("/")[-1]
            
            hook.wait_for_workflow_invocation(
                workflow_invocation_id=workflow_invocation_id,
                repository_id=repository_id,
                project_id=project_id,
                region=region,
                wait_time=10,
                timeout=600,
            )
            print(f"✅ Workflow {workflow_invocation_id} completed!")

        # Encadeamento interno
        compilation_result_name = create_compilation_result()
        workflow_invocation_name = start_workflow_invocation(compilation_result_name)
        self.monitor_task = monitor_workflow_invocation(workflow_invocation_name)
