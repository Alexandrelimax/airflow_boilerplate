output "github_token_secret_id" {
  description = "ID do Secret Manager Secret do GitHub usado no Dataform."
  value       = google_secret_manager_secret.github_token.id
}

output "github_token_secret_version_name" {
  description = "Nome completo da versão do Secret Manager usada como token do GitHub."
  value       = google_secret_manager_secret_version.github_token_version.name
}
