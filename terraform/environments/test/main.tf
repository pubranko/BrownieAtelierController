# TEST 環境用 Terraform 設定（リソースグループ RankoKoushin = テスト環境）

terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "BrownieAtelierTerraformStateRG"
    storage_account_name = "brownieateliertfstate"
    container_name       = "tfstate"
    key                  = "test.tfstate"
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
# ストレージアカウント
# ------------------------------------------------------------------------------
resource "azurerm_storage_account" "data" {
  name                     = "brownieatelierdata"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_account" "functest" {
  name                     = "brownieatelierfunctest"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# ------------------------------------------------------------------------------
# App Service プラン
# ------------------------------------------------------------------------------
resource "azurerm_service_plan" "plan_bdff" {
  name                = "ASP-RankoKoushin-bdff"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1"

  lifecycle { ignore_changes = [sku_name] }
}

resource "azurerm_service_plan" "plan_fd5b" {
  name                = "ASP-rankokoushin-fd5b"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1"

  lifecycle { ignore_changes = [sku_name] }
}

# ------------------------------------------------------------------------------
# 関数アプリ
# ------------------------------------------------------------------------------
resource "azurerm_linux_function_app" "main" {
  name                       = "BrownieAtelierController"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  service_plan_id            = azurerm_service_plan.plan_bdff.id
  storage_account_name       = azurerm_storage_account.functest.name
  storage_account_access_key = azurerm_storage_account.functest.primary_access_key

  site_config {}

  lifecycle {
    ignore_changes = [app_settings, site_config, storage_account_name, storage_account_access_key]
  }
}

resource "azurerm_linux_function_app" "develop" {
  name                       = "BrownieAtelierControllerDevelop"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  service_plan_id            = azurerm_service_plan.plan_fd5b.id
  storage_account_name       = azurerm_storage_account.functest.name
  storage_account_access_key = azurerm_storage_account.functest.primary_access_key

  site_config {}

  lifecycle {
    ignore_changes = [app_settings, site_config, storage_account_name, storage_account_access_key]
  }
}

# ------------------------------------------------------------------------------
# Application Insights
# ------------------------------------------------------------------------------
resource "azurerm_application_insights" "app" {
  name                = "BrownieAtelierControllerAppInsights"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  application_type   = "other"
}

resource "azurerm_application_insights" "develop" {
  name                = "BrownieAtelierControllerDevelop"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  application_type   = "other"
}

resource "azurerm_application_insights" "test" {
  name                = "BrownieAtelierTest"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  application_type   = "other"
}
