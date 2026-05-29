# TEST 環境用変数定義（RankoKoushin = テスト環境）

variable "location" {
  description = "Azure リージョン（例: japaneast）"
  type        = string
}

variable "resource_group_name" {
  description = "リソースグループ名"
  type        = string
}

variable "subscription_id" {
  description = "Azure サブスクリプション ID（未指定時は az login の既定）"
  type        = string
  default     = null
}
