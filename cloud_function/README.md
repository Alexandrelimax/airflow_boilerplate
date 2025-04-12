# ☁️ Cloud Function Boilerplate

Este boilerplate mostra como criar, testar e orquestrar uma função HTTP no Cloud Functions usando Apache Airflow.

Inclui:
- Função HTTP simples (`main.py`)
- Script de deploy (`run.sh`)
- Teste local com `functions-framework`
- Duas DAGs:
  - Clássica com `CloudFunctionInvokeFunctionOperator`
  - Moderna com `@task` + `CloudFunctionsHook`

---

## 📁 Estrutura
```bash
cloud_function/ 
├── main.py
├── requirements.txt 
├── run.sh
├── dag/ 
│ ├── classic_operator_dag.py
│ └── modern_taskflow_dag.py 
└── README.md
```

---

## ▶️ Rodar localmente com functions-framework

1. Instale o pacote:

```bash
pip install -r requirements.txt
```

2. Rode a função localmente:
```bash
functions-framework --target=hello_world
```

3. Acesse em `http://localhost:8080`


## ☁️ Deploy no Cloud Functions
Edite o `run.sh` e rode:
```bash
bash run.sh
```
Parâmetros a ajustar:

1. `PROJECT_ID`
2. `REGION`
3. `FUNCTION_NAME`



## 📡 DAGs disponíveis

### 1️⃣ `classic_operator_dag.py`

| Campo        | Valor |
|--------------|-------|
| **Tipo**     | `CloudFunctionInvokeFunctionOperator` (clássico) |
| **Uso**      | Dispara a função passando `input_data` (payload JSON) |
| **Vantagem** | Simples e direto |
| **Requisitos**| Função já publicada |

### 2️⃣ `modern_taskflow_dag.py`

| Campo        | Valor |
|--------------|-------|
| **Tipo**     | `@task` + `CloudFunctionsHook` |
| **Uso**      | Chamada programática da função com retorno tratado |
| **Vantagem** | Mais controle sobre a resposta |
| **Limitação**| Requer mais código, mas mais flexível |

## ✅ Resultado esperado

```json
{
  "message": "Cloud Function is working 🚀"
}
