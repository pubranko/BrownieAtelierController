#!/usr/bin/env bash
# GitHub Actions の Environment に variables と secrets を一括登録する。
# 前提: gh CLI インストール済み・gh auth login 済み。
# 用法: ./scripts/set-github-env-vars.sh [ENV] [REPO]
#   ENV: PRODUCT または TEST（省略時は PRODUCT）
#   REPO: owner/repo（省略時は git remote origin から取得）
#
# 読み込むファイル: env_file/ 配下
#   env_file/.env.gh.vars.${ENV}   - Variables 用（例: env_file/.env.gh.vars.PRODUCT）
#   env_file/.env.gh.secrets.${ENV} - Secrets 用
# 例は env_file/.env.gh.vars.PRODUCT.example 等をコピーして値を埋める。

set -e

ENV_NAME="${1:-PRODUCT}"
REPO="${2:-}"

case "$ENV_NAME" in
  PRODUCT|TEST) ;;
  *) echo "Error: ENV は PRODUCT または TEST にしてください" >&2; exit 1 ;;
esac

if [ -z "$REPO" ]; then
  REPO=$(git remote get-url origin 2>/dev/null | sed -E 's|^https://github\.com/||; s|^git@github\.com:||; s|\.git$||') || true
  if [ -z "$REPO" ]; then
    echo "Error: REPO を指定するか、git remote origin を設定してください" >&2
    exit 1
  fi
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh CLI がインストールされていません。https://cli.github.com/ を参照してください" >&2
  exit 1
fi

if ! gh auth status 2>&1; then
  echo "" >&2
  echo "---" >&2
  echo "上記のメッセージを確認してください。未認証の場合はターミナルで: gh auth login" >&2
  exit 1
fi

# リポジトリルート（このスクリプトは scripts/ にある想定）
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_DIR="${ROOT}/env_file"
VARS_FILE="${ENV_DIR}/.env.gh.vars.${ENV_NAME}"
SECRETS_FILE="${ENV_DIR}/.env.gh.secrets.${ENV_NAME}"

if [ ! -f "$VARS_FILE" ]; then
  echo "Error: ${VARS_FILE} がありません。env_file/.env.gh.vars.${ENV_NAME}.example をコピーして作成してください" >&2
  exit 1
fi

if [ ! -f "$SECRETS_FILE" ]; then
  echo "Error: ${SECRETS_FILE} がありません。env_file/.env.gh.secrets.${ENV_NAME}.example をコピーして作成してください" >&2
  exit 1
fi

echo "Environment: $ENV_NAME"
echo "Repository:  $REPO"
echo "Variables:   $VARS_FILE"
echo "Secrets:     $SECRETS_FILE"
echo "---"

echo "Variables を登録しています..."
gh variable set -f "$VARS_FILE" --env "$ENV_NAME" -R "$REPO"

echo "Secrets を登録しています..."
gh secret set --env-file "$SECRETS_FILE" --env "$ENV_NAME" -R "$REPO"

echo "---"
echo "完了: $ENV_NAME に variables と secrets を登録しました。"
