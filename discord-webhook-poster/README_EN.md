<h1 align="center">cc-discord-skill</h1>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Discord-Webhook-5865F2?logo=discord&logoColor=white" alt="Discord Webhook">
</p>

An Agent Skill for one-way posting to Discord Webhook with text and attachments (images, audio, video, and documents).

- Skill directory: `discord-webhook-poster/`
- Script: `discord-webhook-poster/scripts/discord_webhook_post.py`

## ✨ Features
- Text posting
- Attachment posting (multiple files, up to 10 files)
- Read Claude hooks JSON from `stdin`
- Skip by default when `stop_hook_active=true` (loop prevention)
- Retry for 429/5xx/network errors
- Attachment size validation (default: 8MB per file)
- Config priority: `CLI arguments > .env`

## 🚀 Setup
1. Copy `discord-webhook-poster/.env.example`

```bash
cp discord-webhook-poster/.env.example discord-webhook-poster/.env
```

2. Edit `discord-webhook-poster/.env`

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_id/your_webhook_token
DISCORD_USERNAME=Claude Notifier
DISCORD_AVATAR_URL=https://example.com/avatar.png
DISCORD_MAX_FILE_SIZE_MB=8
```

### `.env` Variables

- Required
  - `DISCORD_WEBHOOK_URL`
    - Discord Incoming Webhook URL.
    - Posting will fail if this is not set.

- Optional
  - `DISCORD_USERNAME`
    - Display name for messages (overrides webhook default username).
  - `DISCORD_AVATAR_URL`
    - Avatar image URL for messages (HTTP/HTTPS URL).
    - Local file paths are not supported.
  - `DISCORD_MAX_FILE_SIZE_MB`
    - Per-file attachment size limit in MB.
    - Default is `8` when omitted.

## 🛠️ Usage
Run commands from `discord-webhook-poster/`:

```bash
cd discord-webhook-poster
```

### Text only
```bash
python scripts/discord_webhook_post.py --content "Build finished"
```

### With attachments
```bash
python scripts/discord_webhook_post.py \
  --content "Artifacts" \
  --file ./out/report.png \
  --file ./out/voice.mp3
```

### Use custom `.env`
```bash
python scripts/discord_webhook_post.py \
  --env-file /path/to/.env \
  --content "Build finished"
```

### Pipe Claude hook JSON via stdin
```bash
cat /tmp/hook.json | python scripts/discord_webhook_post.py --stdin-json
```

## 🔌 Claude Hooks Integration
Use this template:

- `discord-webhook-poster/assets/claude-hooks-example.json`

Replace `command` with the absolute path in your environment and merge it into `~/.claude/settings.json`.

## ✅ Validation (dry-run)
```bash
cd discord-webhook-poster
python scripts/discord_webhook_post.py --content "test" --dry-run
python scripts/discord_webhook_post.py --content "file test" --file /tmp/sample.mp3 --dry-run
printf '{"stop_hook_active":true}' | python scripts/discord_webhook_post.py --stdin-json
python scripts/discord_webhook_post.py --content "too large" --file /tmp/large.bin --max-file-size-mb 1 --dry-run
```

## ⚠️ Notes
- This skill is send-only (no inbound message handling from Discord).
- Do not post secrets, private keys, or personal data.
- Adjust file size limit based on your Discord/server constraints.
