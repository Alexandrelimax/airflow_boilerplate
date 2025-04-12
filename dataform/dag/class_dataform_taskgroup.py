from airflow.decorators import dag
from airflow.utils.dates import days_ago
from dataform.taskgroup.dataform_taskgroup import DataformWorkflowTaskGroup


@dag(
    dag_id="dataform_class_taskgroup_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dataform", "taskgroup", "class"],
)
def dataform_dag():

    DataformWorkflowTaskGroup(
        group_id="dataform_pipeline",
        project_id="seu-projeto-id",
        region="us-central1",
        repository_id="meu-repo-id",
        branch="main",
    )

dag = dataform_dag()
