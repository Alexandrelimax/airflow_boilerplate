# Dados do Projeto
project_id     = "{project_id}"
project_number = "{project_number}"
region         = "us-central1"

# Secret Manager
secret_id    = "github-token-dataform"
secret_label = "github-access"
secret_data  = "{github_token}"

# Dados do Dataform
display_name = "meu-repositorio-dev"
workspace_id = "dev-workspace"
git_uri      = "{git_uri}"
branch_name  = "main"

# BigQuery Datasets
datasets = [
  { name = "bronze", description = "Landing zone para dados crus" },
  { name = "silver", description = "Zona limpa e deduplicada" },
  { name = "gold", description = "Zona de agregações e analytics" }
]

# BigQuery Tables
tables = [
  # Bronze
  {
    dataset_id  = "bronze"
    table_id    = "order_items_raw"
    schema_path = "./schemas/bronze/order_items_raw_schema.json"
  },
  {
    dataset_id  = "bronze"
    table_id    = "orders_raw"
    schema_path = "./schemas/bronze/orders_raw_schema.json"
  },
  {
    dataset_id  = "bronze"
    table_id    = "products_raw"
    schema_path = "./schemas/bronze/products_raw_schema.json"
  },
  {
    dataset_id  = "bronze"
    table_id    = "users_raw"
    schema_path = "./schemas/bronze/users_raw_schema.json"
  }
]

