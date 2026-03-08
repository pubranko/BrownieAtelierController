# Terraform で管理する Azure インフラ（Brownie Atelier Controller）

- **product**: 本番（BrownieAtelierGroupWest）。datawest ストレージに加え、West3 用（ストレージ brownieatelierwest3・プラン・Application Insights・Function App）を定義。
- **test**: テスト環境（RankoKoushin）。ストレージ、App Service プラン、関数アプリ、Application Insights を定義。
- **`terraform apply` は実行していません。** 変更内容を確認してから手元で `terraform plan` → `apply` してください。

## 定義しているリソース（product の例）

| リソース | 説明 |
|----------|------|
| azurerm_resource_group | リソースグループ |
| azurerm_storage_account | ストレージ（datawest / west3＝brownieatelierwest3） |
| azurerm_service_plan | West3 用 Flex Consumption プラン（ASP-BrownieAtelierWest3） |
| azurerm_application_insights | West3 用 Application Insights |
| azurerm_function_app_flex_consumption | West3 用 Function App |

## 使い方

```bash
# 例: test 環境
cd terraform/environments/test
terraform init    # 初回またはプロバイダー変更後
terraform plan    # 変更内容の確認（apply する前に必ず実行）
terraform apply   # 問題なければ実行（確認プロンプトあり）
```

- **apply 前には必ず `plan` で差分を確認してください。**
- リモート state を使う場合は、各環境の `main.tf` 内の `backend "azurerm"` のコメントを外し、ストレージを用意したうえで `terraform init -reconfigure` してください。

## ディレクトリ構成

```
terraform/
├── README.md
├── .terraform-version     # tfenv 用
├── scripts/               # 一括 import 用（terraform import を並べたシェル）
│   ├── README.md
│   ├── import_brownie_atelier_group_west.sh
│   └── import_ranko_koushin.sh
└── environments/
    ├── test/              # TEST 環境（RankoKoushin）
    │   ├── main.tf
    │   ├── variables.tf
    │   └── terraform.tfvars
    └── product/           # PRODUCT 環境（BrownieAtelierGroupWest = 本番）
        ├── main.tf
        ├── variables.tf
        └── terraform.tfvars
```

既存リソースを state に取り込む場合は、ポータルからエクスポートした CSV 用の一括 import スクリプト（`scripts/README.md`）を利用できます。

## リモート state（任意・後から）

本番運用では state を Azure Storage に置くことを推奨します。  
その場合は各環境の `main.tf` の `terraform { backend "azurerm" { ... } }` のコメントを外し、  
ストレージアカウント・コンテナを用意したうえで `terraform init -reconfigure` してください。

### state 用ストレージの作成（Azure CLI）

最初の 1 回だけ、state を格納するストレージを手動で用意します。ポータルではなく以下のコマンドで作成できます（`<リソースグループ名>` と `<ロケーション>` は任意の値に置き換えてください）。

```bash
# 変数（必要に応じて変更）
RESOURCE_GROUP="BrownieAtelierTerraformStateRG"   # 例: BrownieAtelierTerraformStateRG
LOCATION="japaneast"                             # 例: japaneast / japanwest
STORAGE_ACCOUNT="brownieateliertfstate"          # 3〜24文字・英小文字と数字（グローバル一意のため既存なら別名に）
CONTAINER="tfstate"

# リソースグループ作成
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# ストレージアカウント作成
az storage account create \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --sku Standard_LRS

# state 用コンテナ作成
az storage container create \
  --name "$CONTAINER" \
  --account-name "$STORAGE_ACCOUNT" \
  --auth-mode login
```

作成後、各環境の `main.tf` の backend ブロックで `resource_group_name` / `storage_account_name` / `container_name` に上記の値を指定し、`key` には環境ごとの state ファイル名（例: `test.tfstate`, `product.tfstate`）を指定してください。

## state の保存先（二重化していないことの確認）

- product / test とも `backend "azurerm"` が有効です。**state は Azure のストレージ 1 か所だけ**（`BrownieAtelierTerraformStateRG` / `brownieateliertfstate` / コンテナ `tfstate` / キー `product.tfstate` または `test.tfstate`）に保存されます。
- 作業ディレクトリには `terraform.tfstate` は作られません（`.terraform/terraform.tfstate` は backend の種類・設定のメタデータのみで、実データは Azure 上）。
- **現在どの state を見ているか**は、各環境で `terraform state list` を実行すると確認できます。表示されるリソース一覧が、その環境で参照している state の内容です。
- ローカルに `terraform.tfstate` が残っている場合は、古い運用の名残の可能性があります。その場合は `terraform init -reconfigure` で backend を Azure に合わせたうえで、必要なら state の移行を検討してください。

## 注意

- **apply は内容を確認したうえで手元で実行してください。** CI では実行していません。
- 既に同じ名前のリソースが Azure にある場合は、`terraform import` で state に取り込むか、tfvars の名前を変更してください。
