<h1 align="center">cc-discord-skill</h1>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Discord-Webhook-5865F2?logo=discord&logoColor=white" alt="Discord Webhook">
</p>

Discord Webhook に対して、テキストと添付ファイル（画像・音声・動画・ドキュメント）を一方向送信する Agent Skill です。

- Skill本体: `discord-webhook-poster/`
- スクリプト: `discord-webhook-poster/scripts/discord_webhook_post.py`

## ✨ 特徴
- テキスト投稿
- 添付ファイル投稿（複数可、最大10件）
- Claude hooks の JSON を `stdin` から受け取り投稿
- `stop_hook_active=true` の場合はデフォルトで送信スキップ（ループ防止）
- 429/5xx/ネットワークエラー時のリトライ
- 添付サイズ上限チェック（デフォルト 8MB/件）
- 設定の優先順位は `CLI引数 > .env`

## 🚀 セットアップ
1. `discord-webhook-poster/.env.example` をコピー

```bash
cp discord-webhook-poster/.env.example discord-webhook-poster/.env
```

2. `discord-webhook-poster/.env` を編集

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_id/your_webhook_token
DISCORD_USERNAME=Claude Notifier
DISCORD_AVATAR_URL=https://example.com/avatar.png
DISCORD_MAX_FILE_SIZE_MB=8
```

### `.env`項目の説明

- 必須
  - `DISCORD_WEBHOOK_URL`
    - Discord Incoming Webhook URL。
    - これが未設定だと送信できません。

- 任意
  - `DISCORD_USERNAME`
    - 投稿時の表示名（Webhookのデフォルト名を上書き）。
  - `DISCORD_AVATAR_URL`
    - 投稿時のアイコン画像URL（HTTP/HTTPSのURLを指定）。
    - ローカルファイルパスは指定できません。
  - `DISCORD_MAX_FILE_SIZE_MB`
    - 添付ファイル1件あたりのサイズ上限（MB）。
    - 未指定時のデフォルトは `8`。

## 🛠️ 使い方
`discord-webhook-poster/` ディレクトリで実行する例:

```bash
cd discord-webhook-poster
```

### テキストのみ
```bash
python scripts/discord_webhook_post.py --content "Build finished"
```

### 添付ファイル付き
```bash
python scripts/discord_webhook_post.py \
  --content "Artifacts" \
  --file ./out/report.png \
  --file ./out/voice.mp3
```

### `.env` を明示指定
```bash
python scripts/discord_webhook_post.py \
  --env-file /path/to/.env \
  --content "Build finished"
```

### Claude hook JSON を標準入力から渡す
```bash
cat /tmp/hook.json | python scripts/discord_webhook_post.py --stdin-json
```

## 🔌 Claude Hooks 連携
テンプレートを利用:

- `discord-webhook-poster/assets/claude-hooks-example.json`

テンプレ内の `command` を実環境の絶対パスに置き換えて、`~/.claude/settings.json` に反映してください。

## ✅ 検証コマンド（dry-run）
```bash
cd discord-webhook-poster
python scripts/discord_webhook_post.py --content "test" --dry-run
python scripts/discord_webhook_post.py --content "file test" --file /tmp/sample.mp3 --dry-run
printf '{"stop_hook_active":true}' | python scripts/discord_webhook_post.py --stdin-json
python scripts/discord_webhook_post.py --content "too large" --file /tmp/large.bin --max-file-size-mb 1 --dry-run
```

## ⚠️ 注意事項
- このSkillは送信専用です（Discordからの受信はしません）。
- 機密情報・秘密鍵・個人情報を投稿しないでください。
- Discord側のプラン/サーバー設定に応じて添付上限を調整してください。
