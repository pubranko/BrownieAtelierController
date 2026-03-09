# env_file

GitHub Actions の Environment（PRODUCT / TEST）に登録する variables / secrets の .env 形式ファイルを置くフォルダ。

## ファイル構成

| ファイル | 説明 |
|----------|------|
| `.env.gh.vars.PRODUCT` | PRODUCT 用 Variables（実体。.gitignore 対象） |
| `.env.gh.secrets.PRODUCT` | PRODUCT 用 Secrets（実体。.gitignore 対象） |
| `.env.gh.vars.TEST` | TEST 用 Variables（実体。.gitignore 対象） |
| `.env.gh.secrets.TEST` | TEST 用 Secrets（実体。.gitignore 対象） |
| `*.example` | 上記のテンプレート。コピーして値を埋めて使用 |

## 使い方

1. **初回**: `.env.gh.vars.PRODUCT.example` を `.env.gh.vars.PRODUCT` にコピーし値を埋める（または `./scripts/generate-github-env-files.sh` で west2の環境変数.json から生成）。
2. **一括登録**: タスク「GitHub: Set Environment Variables」で PRODUCT / TEST を選んで実行。または `./scripts/set-github-env-vars.sh PRODUCT`。
3. スクリプトはこのフォルダ内の `.env.gh.vars.${ENV}` と `.env.gh.secrets.${ENV}` を参照する。
