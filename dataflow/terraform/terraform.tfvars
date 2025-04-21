project_id        = ""
region             = "us-central1"

bq_dataset_id      = "dataset_teste"
bq_table_id        = "pessoas"
bq_schema_file     = "./schemas/pessoas_schema.json"

template_bucket    = "apresentacao"
template_path      = "template/workshop-dataflow.json"

gcs_bucket_name    = "apresentacao"
gcs_input_path     = "csv/data.csv"

dataflow_job_name  = "job-pessoas-uppercase"
