#!/bin/bash

# Configurações
PROJECT_ID=""
REGION="us-central1"
ARTIFACT_ID="my-repository"
IMAGE_NAME="uppercase-dataflow"
VERSION="v1"

# Derivados
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_ID/$IMAGE_NAME:$VERSION"
TEMPLATE_BUCKET="gs://$PROJECT_ID-dataflow-templates"
TEMPLATE_PATH="templates/$IMAGE_NAME-template.json"
METADATA_FILE="metadata.json"

# --- Início do Script ---

echo "🔐 Autenticando no projeto GCP..."
gcloud config set project "$PROJECT_ID"
gcloud auth configure-docker "$REGION-docker.pkg.dev"

echo "🔨 Build da imagem Docker..."
docker build -t "$IMAGE" .

echo "📤 Enviando a imagem para o Artifact Registry..."
docker push "$IMAGE"

echo "📁 Verificando se o bucket de templates existe..."
if ! gsutil ls "$TEMPLATE_BUCKET" > /dev/null 2>&1; then
  echo "📦 Bucket não encontrado. Criando..."
  gsutil mb -l "$REGION" "$TEMPLATE_BUCKET"
else
  echo "✅ Bucket já existe."
fi

echo "🧠 Gerando Flex Template no GCS..."
gcloud dataflow flex-template build "$TEMPLATE_BUCKET/$TEMPLATE_PATH" \
  --image "$IMAGE" \
  --sdk-language "PYTHON" \
  --metadata-file "$METADATA_FILE"

echo "✅ Template criado com sucesso!"
echo "📄 Caminho do template: $TEMPLATE_BUCKET/$TEMPLATE_PATH"
