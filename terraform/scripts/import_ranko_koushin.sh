#!/usr/bin/env bash
# RankoKoushin（TEST 環境）用: terraform import を一括実行
# 対象: terraform/environments/test（リソースグループ RankoKoushin = テスト環境）
# 既に import 済みの行はコメントアウトして再実行すること。

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "${TF_DIR:-$REPO_ROOT/terraform/environments/test}"

SUB="/subscriptions/f1a4dbd6-2833-4f2b-addb-1c07e6f0f220"
RG="$SUB/resourceGroups/RankoKoushin"

# リソースグループ。既に import 済みの場合はコメントアウト
terraform import -input=false azurerm_resource_group.main "$RG"

# ストレージアカウント。既に import 済みの場合はコメントアウト
terraform import -input=false azurerm_storage_account.data "$RG/providers/Microsoft.Storage/storageAccounts/brownieatelierdata"
terraform import -input=false azurerm_storage_account.functest "$RG/providers/Microsoft.Storage/storageAccounts/brownieatelierfunctest"

# App Service プラン（RG は RankoKoushin / rankokoushin の2種あり）。既に import 済みの場合はコメントアウト
terraform import -input=false azurerm_service_plan.plan_bdff "$RG/providers/Microsoft.Web/serverFarms/ASP-RankoKoushin-bdff"
terraform import -input=false azurerm_service_plan.plan_fd5b "$SUB/resourceGroups/rankokoushin/providers/Microsoft.Web/serverFarms/ASP-rankokoushin-fd5b"

# 関数アプリ。既に import 済みの場合はコメントアウト
terraform import -input=false azurerm_linux_function_app.main "$RG/providers/Microsoft.Web/sites/BrownieAtelierController"
terraform import -input=false azurerm_linux_function_app.develop "$SUB/resourceGroups/rankokoushin/providers/Microsoft.Web/sites/BrownieAtelierControllerDevelop"

# Application Insights（プロバイダーは Microsoft.Insights 表記を要求）。既に import 済みの場合はコメントアウト
terraform import -input=false azurerm_application_insights.app "$RG/providers/Microsoft.Insights/components/BrownieAtelierControllerAppInsights"
terraform import -input=false azurerm_application_insights.develop "$RG/providers/Microsoft.Insights/components/BrownieAtelierControllerDevelop"
terraform import -input=false azurerm_application_insights.test "$RG/providers/Microsoft.Insights/components/BrownieAtelierTest"

# アクショングループ・アラート・Recovery Services などは必要に応じて追加
# terraform import ... "$RG/providers/microsoft.insights/actiongroups/Application Insights Smart Detection"
# terraform import ... "$RG/providers/microsoft.alertsmanagement/smartDetectorAlertRules/..."
# terraform import ... "$RG/providers/Microsoft.RecoveryServices/vaults/vault-lxogxlpw"
