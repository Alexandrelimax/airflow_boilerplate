from airflow.decorators import dag, task, task_group
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.hooks.dataform import DataformHook
from datetime import timedelta


PROJECT_ID = "seu-projeto-id"
REGION = "us-central1"
REPOSITORY_ID = "meu-repo-id"
BRANCH_NAME = "main"


@dag(
    dag_id="dataform_taskgroup_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dataform", "taskgroup"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
)
def dataform_dag():

    @task_group(group_id="dataform_pipeline")
    def run_dataform():

        @task()
        def compile_code() -> str:
            hook = DataformHook()
            result = hook.create_compilation_result(
                project_id=PROJECT_ID,
                region=REGION,
                repository_id=REPOSITORY_ID,
                compilation_result={"git_commitish": BRANCH_NAME},
            )
            comp_id = result["name"].split("/")[-1]
            print(f"✅ Compilation ID: {comp_id}")
            return comp_id

        @task()
        def invoke_workflow(compilation_result_id: str) -> str:
            hook = DataformHook()
            result = hook.create_workflow_invocation(
                project_id=PROJECT_ID,
                region=REGION,
                repository_id=REPOSITORY_ID,
                workflow_invocation={
                    "compilation_result": f"projects/{PROJECT_ID}/locations/{REGION}/repositories/{REPOSITORY_ID}/compilationResults/{compilation_result_id}"
                },
            )
            invocation_id = result["name"].split("/")[-1]
            print(f"🚀 Workflow Invocation ID: {invocation_id}")
            return invocation_id

        @task()
        def wait_for_finish(invocation_id: str):
            hook = DataformHook()
            print("⏳ Aguardando execução do workflow...")
            hook.wait_for_workflow_invocation(
                workflow_invocation_id=invocation_id,
                repository_id=REPOSITORY_ID,
                project_id=PROJECT_ID,
                region=REGION,
                wait_time=10,
                timeout=600,
            )
            print("✅ Workflow concluído com sucesso!")

        # Encadeamento dentro do grupo
        comp_id = compile_code()
        inv_id = invoke_workflow(comp_id)
        wait_for_finish(inv_id)

    # Executa o grupo
    run_dataform()


dag = dataform_dag()
