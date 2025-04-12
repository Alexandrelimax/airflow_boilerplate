# 🚀 Dataflow Boilerplate (Apache Beam + BigQuery)

Este exemplo mostra como criar um pipeline com Apache Beam, rodando no Dataflow, que:
- Lê um arquivo CSV do Cloud Storage (GCS)
- Realiza uma transformação simples (ex: deixa o nome em maiúsculas)
- Salva os dados no BigQuery

Inclui:
- Pipeline Apache Beam (`pipeline/main.py`)
- Empacotamento com `setup.py`
- Script de execução (`run.sh`)
- Duas versões de DAG do Airflow:
  - Usando operador clássico (`classic_operator_dag.py`)
  - Usando sintaxe moderna com `@task` e `DataflowHook` (`modern_taskflow_dag.py`)

---

## 📁 Estrutura

```bash
dataflow/
 ├── dags/ │ 
 ├── classic_operator_dag.py # DAG usando operador Dataflow clássico 
 │ └── modern_taskflow_dag.py # DAG usando @task e DataflowHook 
 ├── pipeline/ 
 │ └── main.py # Código do pipeline Beam 
 ├── requirements.txt 
 ├── setup.py # Empacotamento pro Dataflow 
 ├── run.sh # Executa local ou envia pro Dataflow 
 └── README.md
```


---

## 📦 Pré-requisitos

- Projeto no GCP com APIs habilitadas:
  - Cloud Storage
  - BigQuery
  - Dataflow
- Bucket no GCS criado com:
  - `input/data.csv` (com cabeçalho: `id,name,age`)
  - Pasta `temp/` para staging
  - Pasta `dataflow/` para salvar o `main.py` se for usar no Airflow
- Dataset e tabela no BigQuery com schema:
  - `id:INTEGER`, `name:STRING`, `age:INTEGER`

---

## ▶️ Executar via terminal (sem Airflow)

1. Ajuste o `run.sh` com seu:
   - `PROJECT_ID`
   - `REGION`
   - `BUCKET_NAME`
   - `DATASET` e `TABLE`

2. Rode o script:
```bash
bash run.sh

```

☁️ **Executar via Airflow**

✅ **Opção 1: Usando operador clássico**  
`Arquivo: dags/classic_operator_dag.py`  

- Usa `DataflowCreatePythonJobOperator`  
- Requer que o `main.py` esteja no GCS: `gs://<bucket>/dataflow/main.py`  

✅ **Opção 2: Usando sintaxe moderna (@task + hook)**  
`Arquivo: dags/modern_taskflow_dag.py`  

- Usa `@task` com `DataflowHook`  
- Mais flexível e reutilizável  

✨ **Personalizações**  
- Mude o nome das colunas e lógica de transformação no `pipeline/main.py`  
- Alterne entre `WriteToBigQueryDisposition.WRITE_APPEND` ou `WRITE_TRUNCATE`  
- Adicione validações, filtros, joins, etc.  

✅ **Dica final**  
Este boilerplate é a base. Copie e cole como template para novos pipelines!