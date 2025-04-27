output "repository_name" {
  description = "Nome do repositório criado no Dataform"
  value       = google_dataform_repository.repository.name
}

output "workspace_name" {
  description = "Nome do workspace criado no Dataform"
  value       = google_dataform_workspace.workspace.name
}
