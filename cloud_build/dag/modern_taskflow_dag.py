from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.cloud_build import CloudBuildHook
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from datetime import datetime
import yaml

bucket = "meu-bucket"
modelo_origem = "modelos/modelo_novo.pkl"
modelo_destino = "app/model.pkl"
cloudbuild_yaml_path = "app/cloudbuild.yaml"
projeto_id = "seu-projeto-id"

@dag(
    dag_id="mlops_cloudbuild_taskflow",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["mlops", "cloudbuild"]
)
def deploy_model_taskflow():

    @task()
    def substituir_modelo(bucket_name: str, origem: str, destino: str):
        gcs = GCSHook()
        conteudo = gcs.download(bucket_name=bucket_name, object_name=origem)
        gcs.upload(bucket_name=bucket_name, object_name=destino, data=conteudo)

    @task()
    def executar_build_do_yaml(bucket_name: str, yaml_path: str, project_id: str):
        gcs = GCSHook()
        yaml_content = gcs.download(bucket_name=bucket_name, object_name=yaml_path).decode("utf-8")
        build_config = yaml.safe_load(yaml_content)

        cloudbuild = CloudBuildHook()
        build = cloudbuild.create_build(project_id=project_id, build=build_config)

        build_id = build.metadata.build.id
        return build_id


    substituir_modelo(bucket, modelo_origem, modelo_destino) >> executar_build_do_yaml(bucket, cloudbuild_yaml_path, projeto_id)

deploy_model_taskflow()
