#!/bin/bash

PROJECT_ID="seu-projeto-id"
REGION="us-central1"
ARTIFACT_ID="dataflow-pipelines"
IMAGE_NAME="uppercase-dataflow"
VERSION="v1"

IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_ID/$IMAGE_NAME:$VERSION"
TEMPLATE_BUCKET="gs://$PROJECT_ID-dataflow-templates"
TEMPLATE_PATH="templates/$IMAGE_NAME-template.json"
METADATA_FILE="metadata.json"

echo "🔐 Autenticando no projeto GCP..."
gcloud config set project $PROJECT_ID 
gcloud auth configure-docker $REGION-docker.pkg.dev


echo "🔨 Build da imagem Docker..."
docker build -t $IMAGE .


echo "📤 Enviando a imagem para o Artifact Registry..."
docker push $IMAGE


echo "📁 Garantindo que o bucket para templates existe..."
gsutil ls $TEMPLATE_BUCKET || gsutil mb -l $REGION $TEMPLATE_BUCKET


echo "🧠 Gerando template no GCS..."
gcloud dataflow flex-template build $TEMPLATE_BUCKET/$TEMPLATE_PATH \
  --image $IMAGE \
  --sdk-language "PYTHON" \
  --metadata-file $METADATA_FILE

echo "✅ Template criado com sucesso!"
echo "📄 Caminho do template: $TEMPLATE_BUCKET/$TEMPLATE_PATH"
