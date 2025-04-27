terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0" # ou a versão desejada
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}
