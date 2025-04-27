output "dataset_ids" {
  description = "Lista dos datasets criados"
  value       = [for ds in google_bigquery_dataset.datasets : ds.dataset_id]
}

output "table_ids" {
  description = "Lista das tabelas criadas"
  value       = [for tbl in google_bigquery_table.tables : tbl.table_id]
}
