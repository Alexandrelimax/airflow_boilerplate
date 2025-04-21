module "bigquery" {
  source           = "./modules/bigquery"
  project_id       = var.project_id
  region           = var.region
  bq_dataset_id    = var.bq_dataset_id
  bq_table_id      = var.bq_table_id
  bq_schema_file   = var.bq_schema_file
}

module "dataflow" {
  source             = "./modules/dataflow"
  project_id         = var.project_id
  region             = var.region
  dataflow_job_name  = var.dataflow_job_name
  template_bucket    = var.template_bucket
  template_path      = var.template_path
  gcs_input_path     = var.gcs_input_path
  gcs_bucket_name    = var.gcs_bucket_name
  bq_output_table    = module.bigquery.table_id
  bq_output_dataset  = module.bigquery.dataset_id

  depends_on = [module.bigquery]
}
