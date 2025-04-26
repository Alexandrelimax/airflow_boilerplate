resource "google_bigquery_dataset" "dataflow_dataset" {
  dataset_id = var.bq_dataset_id
  location   = var.region
}

resource "google_bigquery_table" "pessoas_table" {
  dataset_id = google_bigquery_dataset.dataflow_dataset.dataset_id
  table_id   = var.bq_table_id
  schema     = file("${path.module}/../../schemas/${var.bq_schema_file}")
}
