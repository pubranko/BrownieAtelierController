#!/usr/bin/env bash
# 環境別に terraform plan/apply を実行する。
# 用法: ./scripts/terraform-run.sh <product|test> <plan|apply>
# 呼び出し元はワークスペースルート（terraform/environments/ があるディレクトリ）であること。
# 変数は terraform.tfvars および CI では GitHub Actions の TF_VAR_* 等で指定。

set -e

ENV="${1:?Usage: $0 <product|test> <plan|apply>}"
ACTION="${2:?Usage: $0 <product|test> <plan|apply>}"

case "$ENV" in
  product|test) ;;
  *) echo "Error: 第1引数は product または test にしてください" >&2; exit 1 ;;
esac
case "$ACTION" in
  plan|apply) ;;
  *) echo "Error: 第2引数は plan または apply にしてください" >&2; exit 1 ;;
esac

cd "terraform/environments/$ENV"
exec terraform "$ACTION"
