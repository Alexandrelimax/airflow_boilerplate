# Projeto GCP
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Location (ex: us-central1)"
  type        = string
}

# BigQuery
variable "datasets" {
  description = "Lista de datasets para criar"
  type = list(object({
    name        = string
    description = string
  }))
}

variable "tables" {
  description = "Lista de tabelas para criar"
  type = list(object({
    dataset_id  = string
    table_id    = string
    schema_path = string
  }))
}

# Secret Manager
variable "secret_id" {
  description = "Nome da Secret no Secret Manager"
  type        = string
}

variable "secret_label" {
  description = "Label do Secret"
  type        = string
}

variable "secret_data" {
  description = "Token secreto do GitHub"
  type        = string
  sensitive   = true
}

# Dataform
variable "display_name" {
  description = "Nome amigável do repositório Dataform"
  type        = string
}

variable "workspace_id" {
  description = "ID do workspace do Dataform"
  type        = string
}

variable "git_uri" {
  description = "URL do repositório Git conectado ao Dataform"
  type        = string
}

variable "branch_name" {
  description = "Nome da branch padrão do Git"
  type        = string
}

variable "authentication_token_secret_version" {
  description = "ID da versão da Secret Manager com o token do GitHub"
  type        = string
}
