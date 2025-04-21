output "dataset_id" {
  value = google_bigquery_dataset.dataflow_dataset.dataset_id
}

output "table_id" {
  value = google_bigquery_table.pessoas_table.table_id
}
