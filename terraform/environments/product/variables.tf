# PRODUCT 環境用変数定義
# app_settings は GitHub Actions で管理するため、Terraform で使う変数はリソース識別用のみ。

variable "location" {
  description = "Azure リージョン（例: japanwest）"
  type        = string
}

variable "resource_group_name" {
  description = "リソースグループ名"
  type        = string
}

variable "function_app_name" {
  description = "West3 Function App 名（例: BrownieAtelierControllerWest3）"
  type        = string
}
