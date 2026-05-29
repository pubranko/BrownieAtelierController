# West3 をリモート state から削除する手順

Azure 上で West3 の Function App とそのストレージを手動削除したあと、リモート state に West3 関連が残っていれば削除します。

## 1. state の確認（product で実行）

```bash
cd terraform/environments/product
terraform state list
```

次のアドレスが **あれば** 削除対象です。

- `azurerm_function_app_flex_consumption.west3`
- `azurerm_storage_container.deployment_west3`
- `azurerm_service_plan.west3`

※ `azurerm_storage_account.func` は West2 が利用しているため **削除しない**。

**apply で plan_8241 が 409 Conflict になった場合:** 「プランに West2 が割り当てられている」と Azure が返すことがあります。West2 の削除直後は Azure の反映が遅れるため、**数分待ってから `terraform apply` を再実行**すると plan_8241 の削除が通ることが多いです。

## 2. 削除コマンド（存在するものだけ実行）

上記のうち、`terraform state list` に表示されたものだけ実行してください。

```bash
cd terraform/environments/product

# West3 用 Function App（あれば）
terraform state rm 'azurerm_function_app_flex_consumption.west3'

# West3 用デプロイコンテナ（あれば）
terraform state rm 'azurerm_storage_container.deployment_west3'

# West3 用 Flex Consumption プラン（あれば）
terraform state rm 'azurerm_service_plan.west3'
```

## 3. 削除後の確認

```bash
terraform state list
terraform plan
```

`plan` で West3 関連の「destroy」や「add」が出ていなければ state の整理は完了です。
