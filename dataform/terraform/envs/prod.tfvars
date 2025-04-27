# Dados do Projeto
project_id = "meu-projeto-prod"
region     = "us-central1"

# Secret Manager
secret_id    = "github-token-dataform"
secret_label = "github-access"
secret_data  = "SEU_TOKEN_DO_GITHUB_AQUI"

# Dados do Dataform
display_name = "meu-repositorio-prod" # cuidado aqui, só o nome, não o caminho inteiro!
workspace_id = "prod-workspace"
git_uri      = "https://github.com/seu-usuario/seu-repo.git"
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
  },

  # Silver
  {
    dataset_id  = "silver"
    table_id    = "order_items_cleaned"
    schema_path = "./schemas/silver/order_items_cleaned_schema.json"
  },
  {
    dataset_id  = "silver"
    table_id    = "orders_cleaned"
    schema_path = "./schemas/silver/orders_cleaned_schema.json"
  },
  {
    dataset_id  = "silver"
    table_id    = "products_cleaned"
    schema_path = "./schemas/silver/products_cleaned_schema.json"
  },
  {
    dataset_id  = "silver"
    table_id    = "users_cleaned"
    schema_path = "./schemas/silver/users_cleaned_schema.json"
  },

  # Gold
  {
    dataset_id  = "gold"
    table_id    = "sales_summary"
    schema_path = "./schemas/gold/sales_summary_schema.json"
  },
  {
    dataset_id  = "gold"
    table_id    = "monthly_revenue_summary"
    schema_path = "./schemas/gold/monthly_revenue_summary_schema.json"
  },
  {
    dataset_id  = "gold"
    table_id    = "product_sales_summary"
    schema_path = "./schemas/gold/product_sales_summary_schema.json"
  },
  {
    dataset_id  = "gold"
    table_id    = "new_customers_summary"
    schema_path = "./schemas/gold/new_customers_summary_schema.json"
  }
]

