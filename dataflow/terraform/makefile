# Ambiente padrão se não passar ENV
ENV ?= dev
# Auto-approve padrão ativado
AUTO_APPROVE ?= true

PROJECT_ID=my-project-id
BUCKET_NAME=my-bucket-name
REGION=us-central1

TFVARS_FILE=envs/$(ENV).tfvars

.PHONY: help create-backend init plan apply destroy deploy-dev deploy-prod

help:
	@echo "Comandos disponíveis:"
	@echo "  make create-backend             - Cria o bucket de backend se não existir"
	@echo "  make init                       - Inicializa o Terraform"
	@echo "  make plan ENV=dev                - Mostra o plano para o ambiente (default: dev)"
	@echo "  make apply ENV=dev               - Aplica o ambiente (default: auto-approve)"
	@echo "  make destroy ENV=dev             - Destrói o ambiente (default: auto-approve)"
	@echo "  make deploy-dev                  - Faz plan e apply para DEV automaticamente"
	@echo "  make deploy-prod                 - Faz plan e apply para PROD automaticamente"
	@echo "  make apply ENV=prod AUTO_APPROVE=false - Aplica pedindo confirmação manual"

create-backend:
	@echo "🔎 Verificando se o bucket gs://${BUCKET_NAME} existe..."
	@if ! gsutil ls -b gs://${BUCKET_NAME} > /dev/null 2>&1; then \
		echo "📦 Bucket não encontrado. Criando..."; \
		gsutil mb -p ${PROJECT_ID} -l ${REGION} gs://${BUCKET_NAME}; \
	else \
		echo "✅ Bucket já existe."; \
	fi

init:
	@echo "🚀 Inicializando Terraform..."
	terraform init

plan:
	@echo "🧠 Gerando plano Terraform para o ambiente: ${ENV}"
	terraform plan -var-file="$(TFVARS_FILE)"

apply:
	@echo "🔋 Aplicando infraestrutura Terraform para o ambiente: ${ENV}"
ifeq ($(AUTO_APPROVE), true)
	terraform apply -var-file="$(TFVARS_FILE)" -auto-approve
else
	terraform apply -var-file="$(TFVARS_FILE)"
endif

destroy:
	@echo "🔥 Destruindo infraestrutura Terraform para o ambiente: ${ENV}"
ifeq ($(AUTO_APPROVE), true)
	terraform destroy -var-file="$(TFVARS_FILE)" -auto-approve
else
	terraform destroy -var-file="$(TFVARS_FILE)"
endif

deploy-dev:
	@echo "🚀 Deploy completo para DEV"
	make plan ENV=dev
	make apply ENV=dev

deploy-prod:
	@echo "🚀 Deploy completo para PROD"
	make plan ENV=prod
	make apply ENV=prod
