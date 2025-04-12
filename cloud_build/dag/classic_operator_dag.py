from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.cloud_build import CloudBuildCreateBuildOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from datetime import datetime

# Função para substituir o modelo no bucket da aplicação
def substituir_modelo_no_gcs():
    gcs_hook = GCSHook()
    bucket = 'meu-bucket'

    # Caminho do novo modelo salvo pelo MLflow
    origem = 'modelos/modelo_novo.pkl'
    
    # Caminho onde a API espera o modelo
    destino = 'app/model.pkl'

    # Baixa o novo modelo e substitui o antigo
    conteudo = gcs_hook.download(bucket_name=bucket, object_name=origem)
    gcs_hook.upload(bucket_name=bucket, object_name=destino, data=conteudo)

# DAG
with DAG('mlops_deploy_novo_modelo',
         start_date=datetime(2024, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:

    substituir_modelo = PythonOperator(
        task_id='substituir_modelo',
        python_callable=substituir_modelo_no_gcs
    )

    build_deploy = CloudBuildCreateBuildOperator(
        task_id='build_e_deploy_cloud_run',
        project_id='seu-projeto-id',
        source={
            'storageSource': {
                'bucket': 'meu-bucket',
                'object': 'app/'  # onde estão o Dockerfile, model.pkl, main.py, cloudbuild.yaml
            }
        }
    )

    substituir_modelo >> build_deploy
