module "secret_manager" {
  source = "./modules/secret_manager"

  project_id  = var.project_id
  region      = var.region
  secret_id   = var.secret_id
  label       = var.secret_label
  secret_data = var.secret_data
}

module "bigquery" {
  source = "./modules/bigquery"

  project_id = var.project_id
  region     = var.region
  datasets   = var.datasets
  tables     = var.tables

  depends_on = [
    module.secret_manager
  ]
}

module "dataform" {
  source = "./modules/dataform"

  project_id                          = var.project_id
  region                              = var.region
  display_name                        = var.display_name
  workspace_id                        = var.workspace_id
  git_uri                             = var.git_uri
  branch_name                         = var.branch_name
  authentication_token_secret_version = module.secret_manager.secret_version_id

  depends_on = [
    module.secret_manager,
    module.bigquery
  ]
}
