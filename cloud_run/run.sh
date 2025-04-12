#!/bin/bash

PROJECT_ID="seu-projeto-id"
REGION="us-central1"
SERVICE_NAME="cloud-run-fastapi-demo"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

gcloud builds submit --tag $IMAGE

gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
