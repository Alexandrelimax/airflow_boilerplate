terraform {
  backend "gcs" {
    bucket  = "{BUCKET_NAME}"
    prefix  = "dataflow/terraform.tfstate"
  }
}
