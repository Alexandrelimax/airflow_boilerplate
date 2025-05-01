output "repository_name" {
  description = "Nome do repositório criado no Dataform"
  value       = google_dataform_repository.repository.name
}
