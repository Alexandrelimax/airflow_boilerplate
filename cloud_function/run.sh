#!/bin/bash

PROJECT_ID="seu-projeto-id"
REGION="us-central1"
FUNCTION_NAME="hello-world-function"

gcloud functions deploy $FUNCTION_NAME \
  --entry-point hello_world \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --region $REGION \
  --project $PROJECT_ID
