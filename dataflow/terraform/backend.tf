terraform {
  backend "gcs" {
    bucket  = "terraform-state-meu-projeto"
    prefix  = "dataflow"
  }
}
