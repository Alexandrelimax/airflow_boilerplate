#!/bin/bash

PROJECT_ID="seu-projeto-id"
REGION="us-central1"
JOB_NAME="dataflow-job-$(date +%Y%m%d%H%M%S)"
INPUT_FILE="gs://seu-bucket/input/data.csv"
OUTPUT_TABLE="${PROJECT_ID}:dataset_teste.pessoas"

python3 -m pipeline.main \
  --runner=DataflowRunner \
  --project=$PROJECT_ID \
  --region=$REGION \
  --temp_location=gs://seu-bucket/temp/ \
  --input=$INPUT_FILE \
  --output_table=$OUTPUT_TABLE \
  --setup_file=./setup.py
