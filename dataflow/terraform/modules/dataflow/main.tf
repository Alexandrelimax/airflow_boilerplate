# Para usar o Dataflow Flex Template é necessário usar o provider google-beta
resource "google_dataflow_flex_template_job" "dataflow_job" {
  provider                = google-beta 
  name                    = var.dataflow_job_name
  container_spec_gcs_path = "gs://${var.template_bucket}/${var.template_path}"
  parameters = {
    input  = "gs://${var.gcs_bucket_name}/${var.gcs_input_path}"
    output_table = "${var.bq_output_dataset}.${var.bq_output_table}"
  }
  on_delete = "cancel"
  region    = var.region
}
