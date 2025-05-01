resource "google_bigquery_dataset" "datasets" {
  for_each = { for ds in var.datasets : ds.name => ds }

  project     = var.project_id
  location    = var.region
  dataset_id  = each.value.name
  description = each.value.description
}

resource "google_bigquery_table" "tables" {
  for_each = { for tbl in var.tables : "${tbl.dataset_id}.${tbl.table_id}" => tbl }

  project    = var.project_id
  dataset_id = each.value.dataset_id
  table_id   = each.value.table_id

  schema = file(each.value.schema_path)

  deletion_protection = false

  depends_on = [
    google_bigquery_dataset.datasets
  ]
}
