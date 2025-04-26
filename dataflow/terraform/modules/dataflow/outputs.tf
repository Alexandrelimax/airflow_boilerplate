output "job_id" {
  description = "ID do job Dataflow"
  value       = google_dataflow_flex_template_job.dataflow_job.id
}

output "state" {
  description = "Estado atual do job"
  value       = google_dataflow_flex_template_job.dataflow_job.state
}
