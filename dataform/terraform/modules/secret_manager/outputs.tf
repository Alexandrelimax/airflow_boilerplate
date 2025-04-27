output "secret_id" {
  description = "ID do Secret Manager Secret."
  value       = google_secret_manager_secret.secret.id
}

output "secret_version_id" {
  description = "ID da versão criada no Secret Manager."
  value       = google_secret_manager_secret_version.version_id
}
