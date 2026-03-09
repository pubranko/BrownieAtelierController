#!/usr/bin/env bash
# west2の環境変数.json から env_file/.env.gh.vars.PRODUCT / env_file/.env.gh.secrets.PRODUCT を生成し、
# 同内容で env_file/.env.gh.vars.TEST / env_file/.env.gh.secrets.TEST も生成する。
# 用法: ./scripts/generate-github-env-files.sh [JSON_PATH]
# 生成後、TEST 用は必要に応じて編集してから set-github-env-vars.sh を実行する。

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_DIR="${ROOT}/env_file"
mkdir -p "$ENV_DIR"

JSON_PATH="${1:-$ROOT/west2の環境変数.json}"

if [ ! -f "$JSON_PATH" ]; then
  echo "Error: $JSON_PATH がありません" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq が必要です。インストール例: sudo apt install jq" >&2
  exit 1
fi

get_val() {
  jq -r --arg k "$1" '.[] | select(.name==$k) | .value' "$JSON_PATH" 2>/dev/null || echo "$2"
}

# vars に含めるキー（function_app_settings.yml の vars.* と一致）
VARS_KEYS=(
  AZURE_RESOURCE_GROUP
  AZURE_FUNCTIONAPP_NAME
  AZURE_LOCATION
  AZURE_RESOURCE_GROUP_NAME
  AZURE_STORAGE__ACCOUNT_NAME
  TIMER_TRIGGER_SCHEDULE
  CONTAINER__MONGO_USE_DB
  CONTAINER__MONGO_USER
  CONTAINER_MONGO__RESOURCE_CPU
  CONTAINER_MONGO__RESOURCE_MEMORY_IN_GB
  CONTAINER_MONGO__DNS_NAME_LABEL
  CONTAINER_MONGO__MONGO_CONF
  CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME
  CONTAINER_MONGO__MONGO_TAG
  CONTAINER_MONGO__PORT
  CONTAINER_NEWS_CRAWLER__RESOURCE_CPU
  CONTAINER_NEWS_CRAWLER__RESOURCE_MEMORY_IN_GB
  CONTAINER_NEWS_CRAWLER__TAG
  CONTAINER_CRAWLER__MONGO_PORT
  CONTAINER_CRAWLER__MONGO_TLS
  CONTAINER_CRAWLER__MONGO_TLS_CA_FILE
  CONTAINER_CRAWLER__MONGO_TLS_CERTTIFICATE_KEY_FILE
  CONTAINER_CRAWLER__NOTICE__SLACK_CHANNEL_ID__ERROR
  CONTAINER_CRAWLER__NOTICE__SLACK_CHANNEL_ID__NOMAL
  CONTAINER_CRAWLER__PREFECT__API_URL
  CONTAINER_CRAWLER__SLEEP_TIME_AFTER_PREFECT_SERVER_STARTUP
)

# secrets に含めるキー（デプロイ用 / 関数実行用で CLIENT_ID と CLIENT_SECRET を分けている）
SECRETS_KEYS=(
  AZURE_CLIENT_ID__GITHUB_DEPLOY
  AZURE_CLIENT_ID__FUNCTION_EXEC
  AZURE_TENANT_ID
  AZURE_CLIENT_SECRET__FUNCTION_EXEC
  AZURE_SUBSCRIPTION_ID
  AZURE_STORAGE__ACCOUNT_KEY
  AZURE_STORAGE__CONNECTION_STRING
  ACI_DOCKER_IMAGE__REGISTRY_USERNAME
  ACI_DOCKER_IMAGE__REGISTRY_PASSWORD
  CONTAINER__MONGO_PASS
  CONTAINER_CRAWLER__NOTICE__SLACK_TOKEN
  CONTAINER_MONGO__MONGO_INITDB_ROOT_PASSWORD
)

VARS_FILE="$ENV_DIR/.env.gh.vars.PRODUCT"
SECRETS_FILE="$ENV_DIR/.env.gh.secrets.PRODUCT"

echo "Generating $VARS_FILE ..."
: > "$VARS_FILE"
for k in "${VARS_KEYS[@]}"; do
  case "$k" in
    AZURE_FUNCTIONAPP_NAME) val=$(get_val "$k" "BrownieAtelierControllerWest3") ;;
    AZURE_RESOURCE_GROUP)   val=$(get_val "AZURE_RESOURCE_GROUP_NAME" "BrownieAtelierGroupWest") ;;
    *)                      val=$(get_val "$k" "") ;;
  esac
  printf '%s=%s\n' "$k" "$val" >> "$VARS_FILE"
done

echo "Generating $SECRETS_FILE ..."
: > "$SECRETS_FILE"
for k in "${SECRETS_KEYS[@]}"; do
  val=$(get_val "$k" "")
  printf '%s=%s\n' "$k" "$val" >> "$SECRETS_FILE"
done

# TEST 用は PRODUCT をコピー（値をテスト用に編集する想定）
echo "Copying to env_file/.env.gh.vars.TEST and env_file/.env.gh.secrets.TEST ..."
cp "$VARS_FILE" "$ENV_DIR/.env.gh.vars.TEST"
cp "$SECRETS_FILE" "$ENV_DIR/.env.gh.secrets.TEST"

echo "---"
echo "生成しました:"
echo "  $VARS_FILE, $SECRETS_FILE"
echo "  $ENV_DIR/.env.gh.vars.TEST, $ENV_DIR/.env.gh.secrets.TEST"
echo "AZURE_CLIENT_ID__GITHUB_DEPLOY / AZURE_CLIENT_ID__FUNCTION_EXEC / AZURE_TENANT_ID / AZURE_CLIENT_SECRET__FUNCTION_EXEC は JSON にないため空です。手動で埋めてから ./scripts/set-github-env-vars.sh PRODUCT または TEST を実行してください。"
