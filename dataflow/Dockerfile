FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG DIR=/dataflow/template
RUN mkdir -p ${DIR}
WORKDIR ${DIR}

COPY requirements.txt .
COPY pipeline.py .

# Atualiza o pip e instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define para o Dataflow onde estão os arquivos
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${DIR}/pipeline.py"
