#!/usr/bin/env bash
# BrownieAtelierGroupWest 用: CSV の全リソースを terraform import で一括取り込み
# 実行前に cd 先で terraform init 済みであること。
# 実行場所: リポジトリルートから ./terraform/scripts/import_brownie_atelier_group_west.sh で実行すること（スクリプトが product に cd する）。

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT/terraform/environments/product"

SUB="/subscriptions/f1a4dbd6-2833-4f2b-addb-1c07e6f0f220"
RG="$SUB/resourceGroups/BrownieAtelierGroupWest"

# リソースグループ（CSV に無い）。既に import 済みの場合はコメントアウト
# terraform import -input=false azurerm_resource_group.main "$RG"

# ストレージアカウント（brownieatelierdatawest）。既に import 済みの場合はコメントアウト
# terraform import -input=false azurerm_storage_account.datawest "$RG/providers/Microsoft.Storage/storageAccounts/brownieatelierdatawest"
