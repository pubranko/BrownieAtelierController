# Terraform 一括 import 用スクリプト

`terraform import` コマンドを並べただけのシェルです。リポジトリ直下の CSV（ポータルからエクスポートしたリソース一覧）を元に ID を記載してあります。必要に応じて行の追加・削除・編集をしてください。

## BrownieAtelierGroupWest（product 環境）

- **対象:** `terraform/environments/product`
- **参照 CSV:** `Azureresources_BrownieAtelierGroupWest.csv`

```bash
# リポジトリルートから実行（事前に product で terraform init 済みであること）
./terraform/scripts/import_brownie_atelier_group_west.sh
```

CSV の全リソース＋リソースグループを import 対象にしています（廃止予定の West2 や旧プラン 8241 も Terraform 管理下に置き、廃止時は main.tf から該当 resource を削除して apply で削除）。必要な行のコメントを外して実行してください。

**Azure 上で West3 を手動削除した場合:** リモート state に West3 関連が残っていれば削除する必要があります。手順は [remove_west3_from_state.md](./remove_west3_from_state.md) を参照してください。

**import がエラーになる場合:**

1. **実行場所**  
   `terraform import` は **必ず** `terraform/environments/product` で実行してください。スクリプトは自動でそのディレクトリに cd します。手動で実行する場合は `cd terraform/environments/product` してから import を実行してください。

2. **エラー内容の確認**  
   - **「Resource not found」 / 「404」**  
     サブスクリプション ID・リソースグループ名・リソース名が Azure と一致しているか確認してください。`az account show` でサブスクリプション、ポータルでリソース名を確認し、スクリプト先頭の `SUB` や ID を修正してください。
   - **「Permission denied」 / Azure CLI のエラー**  
     `az login` が済んでいるか、該当サブスクリプションへの権限があるか確認してください。
   - **「Resource already managed by Terraform」**  
     そのリソースはすでに state に存在しています。**エラーではなく正常です。** 該当 import 行はコメントアウトしたままにしてください。

## RankoKoushin（TEST 環境）

- **対象:** `terraform/environments/test`（リソースグループ RankoKoushin = テスト環境）
- **参照 CSV:** `Azureresources_RankoKoushin.csv`

```bash
# 事前に test で terraform init 済みであること
./terraform/scripts/import_ranko_koushin.sh
```

別ディレクトリを対象にする場合:

```bash
TF_DIR="$PWD/terraform/environments/test" ./terraform/scripts/import_ranko_koushin.sh
```

スクリプト内のリソースアドレス（例: `azurerm_storage_account.data`）は main.tf のリソース名に合わせてあります。不要な import は行ごとコメントアウト、定義と違う場合はアドレスを編集してください。

---

## CSV 行と import の対応

### BrownieAtelierGroupWest（CSV ＋ RG 等）

CSV の全行に対応する import を実行します。リソースグループは CSV に含まれないため、スクリプト内で ID を記載しています。廃止予定の West2・旧プラン 8241 も import し、廃止時は main.tf から該当 resource を削除して `terraform apply` で削除します。

### RankoKoushin（CSV 14 行 → import 10 本）

**CSV にあるが import から除外したもの（5 行）**

| 名前 | 種類 | 除外理由 |
|------|------|----------|
| Application Insights Smart Detection | アクション グループ | スクリプトでは「必要に応じて追加」としてコメントのみ。名前のスペースやリソース種別の扱いを分けるため一旦省略。 |
| Failure Anomalies - BrownieAtelierControllerAppInsights | スマート検出機能アラート ルール | main.tf にアラートルールを定義していない想定でコメントのみ。 |
| Failure Anomalies - BrownieAtelierControllerDevelop | スマート検出機能アラート ルール | 同上。 |
| Failure Anomalies - BrownieAtelierTest | スマート検出機能アラート ルール | 同上。 |
| vault-lxogxlpw | Recovery Services コンテナー | 同上。「必要に応じて追加」とコメントのみで、import 行は未記載。 |

※ RankoKoushin はリソースグループも CSV に含まれないため、スクリプトで RG の ID を手で 1 本追加。CSV 14 行のうち 9 行分を import に使用（ストレージ2・プラン2・関数2・App Insights3）。上記 5 行は除外。
