output "location" {
  value       = var.location
  description = "Azure リージョン"
}

output "resource_group_name" {
  value       = var.resource_group_name
  description = "リソースグループ名"
}

output "storage_account_west3_name" {
  value       = azurerm_storage_account.west3.name
  description = "West3 用ストレージアカウント名（brownieatelierwest3）"
}

output "function_app_west3_name" {
  value       = azurerm_function_app_flex_consumption.west3.name
  description = "West3 用 Function App 名"
}
