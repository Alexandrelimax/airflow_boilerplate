import subprocess

# Configurações locais
PIPELINE_SCRIPT = "pipeline.py"
INPUT_PATH = "gs://seu-bucket-teste/data.csv"
OUTPUT_TABLE = "seu-projeto:seu_dataset.sua_tabela"
TEMP_LOCATION = "gs://seu-bucket-teste/temp"
PROJECT = "seu-projeto"
RUNNER = "DirectRunner"
REGION = "us-central1"

# Montar o comando
command = [
    "python", PIPELINE_SCRIPT,
    "--input", INPUT_PATH,
    "--output_table", OUTPUT_TABLE,
    "--runner", RUNNER,
    "--project", PROJECT,
    "--temp_location", TEMP_LOCATION,
    "--region", REGION
]

# Executar
subprocess.run(command)
