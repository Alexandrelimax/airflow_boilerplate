# 🚀 Cloud Run Boilerplate

Este exemplo mostra 4 maneiras diferentes de orquestrar serviços ou jobs do Cloud Run via Apache Airflow.

Inclui:
- Serviço FastAPI simples (`app/main.py`)
- `Dockerfile` pronto para deploy
- Script `run.sh` para build e deploy
- 4 DAGs distintas para uso em Airflow

---

## 📁 Estrutura
```bash
cloud_run/
├── app/ # Código FastAPI
│ └── main.py
├── dag/ # DAGs do Airflow
│ ├── classic_operator_dag.py
│ ├── cloud_run_http_operator_dag.py
│ ├── cloud_run_job_dag.py
│ └── cloud_run_service_dag.py
├── Dockerfile # Para subir no Cloud Run
├── requirements.txt
├── run.sh # Build + deploy
└── README.md
```

## 🧪 Testar localmente
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

bash run.sh
```
## 📡 As 4 DAGs explicadas

### 1️⃣ `classic_operator_dag.py`

| Campo        | Valor |
|--------------|-------|
| **Tipo**     | `CloudRunJobOperator` (clássico) |
| **Uso**      | Executa um Cloud Run Job existente |
| **Vantagem** | Rápido para jobs em lote |
| **Limitação**| Só funciona com Jobs |

### 2️⃣ `cloud_run_job_dag.py`

| Campo        | Valor |
|--------------|-------|
| **Tipo**     | `@task` + `CloudRunHook` |
| **Uso**      | Executa Jobs programaticamente |
| **Vantagem** | Lógica customizável |
| **Limitação**| Requer job pré-existente |

### 3️⃣ `cloud_run_service_dag.py`

| Campo        | Valor |
|--------------|-------|
| **Tipo**     | `@task` + `CloudRunServiceHook` + `requests` |
| **Uso**      | Chama serviços HTTP |
| **Vantagem** | Acessa URL oficial via hook |
| **Limitação**| Requer código extra para chamadas HTTP |

### 4️⃣ `cloud_run_http_operator_dag.py`

| Campo        | Valor |
|--------------|-------|
| **Tipo**     | `SimpleHttpOperator` |
| **Uso**      | Requisições diretas (GET/POST) |
| **Config**   | Criar Connection `cloud_run_service_http` |
| **Vantagem** | Simplicidade |
| **Limitação**| Não usa metadados do Cloud Run |



## 🌐 Criando conexão HTTP no Airflow

1. Acesse **Admin** > **Connections** na interface do Airflow
2. Crie uma nova conexão com os seguintes parâmetros:

```yaml
Conn Id: cloud_run_service_http
Conn Type: HTTP
Host: https://cloud-run-fastapi-demo-xxxxx.a.run.app
```

## ✅ Conclusão

Este boilerplate cobre os dois principais usos do Cloud Run:

**1. Jobs (em batch):**
```python
CloudRunJobOperator | CloudRunHook
```
**2. Serviços HTTP:**
```python
CloudRunServiceHook | requests | SimpleHttpOperator
```