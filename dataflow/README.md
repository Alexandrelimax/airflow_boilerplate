# 🚀 Dataflow Boilerplate (Apache Airflow + Apache Beam com Flex Template + BigQuery + Terraform)

Este exemplo mostra como criar um pipeline com Apache Beam, empacotar como Docker, gerar um Flex Template e executá-lo no Dataflow.  

O pipeline:
- Lê um arquivo CSV do Cloud Storage (GCS)
- Converte os nomes para letras maiúsculas
- Salva os dados em uma tabela no BigQuery

Inclui:

- Pipeline Apache Beam (`pipeline.py`)
- `Dockerfile` com base no SDK oficial do Beam
- `metadata.json` com parâmetros do template
- Script `build_dataflow.sh` para build e upload do template
- Infraestrutura com Terraform para criar dataset, tabela e executar o job
- Duas DAGs Airflow de exemplo:
  - Usando operador clássico
  - Usando sintaxe moderna com `@task` e `DataflowHook`

---

## 📁 Estrutura

```bash
dataflow/
├── dag/
│   ├── classic_operator_dag.py     # DAG com operador clássico
│   └── modern_taskflow_dag.py      # DAG com @task e Hook
├── terraform/                      # Infraestrutura com Terraform
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfvars
│   └── outputs.tf
├── build.sh                        # Script que builda e envia imagem/template
├── Dockerfile                      # Imagem base Beam SDK
├── metadata.json                   # Parâmetros do Flex Template
├── pipeline.py                     # Código do pipeline Apache Beam
├── requirements.txt                # Dependências do pipeline
└── README.md
```

---

## 📦 Pré-requisitos

- Projeto GCP com as seguintes APIs ativadas:
  - Cloud Storage
  - BigQuery
  - Dataflow
  - Artifact Registry

- Buckets criados manualmente:
  - Um bucket para armazenar o CSV  
    Ex: `gs://bucket/csv/data.csv`
  - Um bucket para armazenar o Flex Template  
    Ex: `gs://<project-id>-dataflow-templates`

---

## 🛠️ Build e Deploy do Template

1. Edite o script `build_dataflow.sh` com:
   - `PROJECT_ID`
   - `REGION`
   - `ARTIFACT_ID`
   - `IMAGE_NAME`

2. Execute:

```bash
chmod +x build.sh
./build.sh

```
O script irá:

 - Construir a imagem Docker do pipeline

 - Fazer push para o Artifact Registry

 - Gerar o Flex Template no GCS com base no metadata.json

## ☁️ Executar via Terraform

1. Configure o arquivo `terraform.tfvars` com seus valores:

```hcl
project_id         = "meu-projeto-id"
region             = "us-central1"
bq_dataset_id      = "dataset_teste"
bq_table_id        = "pessoas"
bq_schema_file     = "./schemas/pessoas_schema.json"
template_bucket    = "meu-bucket-templates"
template_path      = "templates/uppercase-dataflow-template.json"
gcs_bucket_name    = "bucket-teste-saida"
gcs_input_path     = "csv/data.csv"
dataflow_job_name  = "job-pessoas-uppercase"
```
Execute:

```bash
cd terraform
terraform init
terraform apply -var-file="terraform.tfvars"
```

## ☁️ Executar via Console (sem Terraform)

Você também pode executar o Flex Template manualmente através do Console do GCP:

1. Acesse **Dataflow > Criar job**
2. Selecione **Modelo personalizado**
3. Informe o caminho do template:  
   `gs://meu-bucket-templates/templates/uppercase-dataflow-template.json`
4. Preencha os parâmetros:

   ```text
   input: gs://bucket-teste-saida/csv/data.csv
   output_table: dataset_teste.pessoas
   ```

## ☁️ Executar via Airflow

### ✅ Clássico

**Arquivo:** `dag/classic_operator_dag.py`

- Utiliza o operador `DataflowFlexTemplateOperator`
- Boa opção para quem prefere a abordagem declarativa tradicional

---

### ✅ Moderno

**Arquivo:** `dag/modern_taskflow_dag.py`

- Utiliza `@task` com `DataflowHook` e `start_flex_template`
- Recomendado para quem busca mais flexibilidade, reutilização de código e controle de fluxo dinâmico

---

## ✨ Personalizações

- Edite o arquivo `pipeline.py` para modificar a transformação de dados
- Altere o `pessoas_schema.json` para incluir ou remover colunas
- Atualize o `metadata.json` para adicionar novos parâmetros ao Flex Template
- Ajuste a forma de escrita no BigQuery:

  ```python
  write_disposition = beam.io.BigQueryDisposition.WRITE_APPEND
  ```
