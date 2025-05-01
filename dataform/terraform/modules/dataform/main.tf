resource "google_dataform_repository" "repository" {
  provider     = google-beta
  project      = var.project_id
  region       = var.region
  display_name = var.display_name
  name         = var.display_name
  git_remote_settings {
    url                                 = var.git_uri
    default_branch                      = var.branch_name
    authentication_token_secret_version = var.authentication_token_secret_version
  }

  workspace_compilation_overrides {
    default_database = var.project_id
  }
}
