resource "google_dataform_repository" "repository" {
  provider     = google-beta
  project      = var.project_id
  region       = var.region
  display_name = var.display_name
  name         = "projects/${var.project_id}/locations/${var.region}/repositories/${var.display_name}"
  git_remote_settings {
    url                                 = var.git_uri
    default_branch                      = var.branch_name
    authentication_token_secret_version = var.authentication_token_secret_version
  }
}

resource "google_dataform_workspace" "workspace" {
  provider = google-beta

  project       = var.project_id
  region        = var.region
  repository_id = google_dataform_repository.repository.repository_id
  workspace_id  = var.workspace_id
}
