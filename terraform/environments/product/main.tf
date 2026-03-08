# PRODUCT 環境用 Terraform 設定
# リソース: リソースグループ、datawest ストレージ、West3 用（関数・プラン・Insights・ストレージ）

terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  # リモート state（README のコマンドで作成したストレージを利用）
  backend "azurerm" {
    resource_group_name  = "BrownieAtelierTerraformStateRG"
    storage_account_name = "brownieateliertfstate"
    container_name       = "tfstate"
    key                  = "product.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# ------------------------------------------------------------------------------
# リソースグループ
# ------------------------------------------------------------------------------
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# ------------------------------------------------------------------------------
# ストレージアカウント（brownieatelierdatawest）
# ------------------------------------------------------------------------------
resource "azurerm_storage_account" "datawest" {
  name                     = "brownieatelierdatawest"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  lifecycle {
    ignore_changes = [allow_nested_items_to_be_public]
  }
}

# ------------------------------------------------------------------------------
# West3 用: ストレージ・プラン・Application Insights・Function App（共通キーワード west3）
# ------------------------------------------------------------------------------

# West3 用ストレージアカウント（連番廃止、west3 を共通キーワードに）
resource "azurerm_storage_account" "west3" {
  name                     = "brownieatelierwest3"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  lifecycle {
    ignore_changes = [allow_nested_items_to_be_public, min_tls_version]
  }
}

# West3 用デプロイパッケージコンテナ
# Flex Consumption が Function App の zip をここに配置し、実行時に参照する。
resource "azurerm_storage_container" "west3_deployment" {
  name                  = "deploymentpackage"
  storage_account_id    = azurerm_storage_account.west3.id
  container_access_type = "private"
}

# West3 用 Flex Consumption プラン
resource "azurerm_service_plan" "west3" {
  name                = "ASP-BrownieAtelierWest3"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "FC1"
}

# West3 用 Application Insights
resource "azurerm_application_insights" "west3" {
  name                = "BrownieAtelierControllerWest3"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  application_type    = "web"
}

# West3 用 Function App（Flex Consumption）
resource "azurerm_function_app_flex_consumption" "west3" {
  name                        = var.function_app_name
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  service_plan_id             = azurerm_service_plan.west3.id
  storage_container_endpoint  = "${azurerm_storage_account.west3.primary_blob_endpoint}${azurerm_storage_container.west3_deployment.name}"
  storage_container_type      = "blobContainer"
  storage_authentication_type = "StorageAccountConnectionString"
  storage_access_key          = azurerm_storage_account.west3.primary_access_key

  runtime_name    = "python"
  runtime_version = "3.10"

  # app_settings は GitHub Actions で管理。Terraform では空のままにし、ignore_changes で触らない。
  app_settings = {}

  site_config {}

  # Azure が自動で付与するタグ・site_config と、app_settings（GitHub Actions 管理）の差分を無視
  lifecycle {
    ignore_changes = [tags, site_config, app_settings]
  }
}

