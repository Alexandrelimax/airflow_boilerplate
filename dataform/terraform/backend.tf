terraform {
  backend "gcs" {
    bucket = "{bucket_name}"
    prefix = "dataform/terraform.tfstate"
  }
}
