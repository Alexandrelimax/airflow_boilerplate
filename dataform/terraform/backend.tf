terraform {
  backend "gcs" {
    bucket = "{BUCKET_NAME}"
    prefix = "dataform/terraform.tfstate"
  }
}
