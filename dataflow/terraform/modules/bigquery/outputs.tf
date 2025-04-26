output "dataset_id" {
  description = "ID do dataset criado"
  value       = google_bigquery_dataset.dataflow_dataset.dataset_id
}

output "table_id" {
  description = "ID da tabela criada"
  value       = google_bigquery_table.pessoas_table.table_id
}
