project_id      = "{PROJECT_ID}"
region          = "us-central1"

# BigQuery
bq_dataset_id   = "dataset_dev"
bq_table_id     = "pessoas_dev"
bq_schema_file  = "pessoas_schema.json"

# Dataflow
dataflow_job_name = "uppercase-job-dev"
template_bucket   = "{PROJECT_ID}-dataflow-templates"
template_path     = "templates/uppercase-dataflow-template.json"

# Datasource CSV
gcs_bucket_name   = "{BUCKET_NAME}"
gcs_input_path    = "csv/data.csv"
