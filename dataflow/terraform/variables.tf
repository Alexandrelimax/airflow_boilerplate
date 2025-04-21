variable "project_id" {
  type        = string
  description = "ID do projeto GCP"
}

variable "region" {
  type        = string
  description = "Região do GCP"
}

variable "bq_dataset_id" {
  type        = string
  description = "ID do dataset no BigQuery"
}

variable "bq_table_id" {
  type        = string
  description = "ID da tabela no BigQuery"
}

variable "bq_schema_file" {
  type        = string
  description = "Nome do arquivo de schema JSON do BigQuery"
}

variable "gcs_bucket_name" {
  type        = string
  description = "Nome do bucket onde o CSV já está"
}

variable "gcs_input_path" {
  type        = string
  description = "Caminho dentro do bucket (ex: csv/data.csv)"
}

variable "template_bucket" {
  type        = string
  description = "Bucket onde o template JSON está salvo"
}

variable "template_path" {
  type        = string
  description = "Caminho para o arquivo JSON do Flex Template dentro do bucket"
}

variable "dataflow_job_name" {
  type        = string
  description = "Nome do job Dataflow"
}
