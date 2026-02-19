---
name: discord-webhook-poster
description: Discord通知や成果物共有のために、Webhookへテキストとマルチメディアファイルを一方向送信する。Claude hooksや手動実行で添付投稿が必要なときに使う。
---

# Discord Webhook Poster

## When to use
- Send one-way notifications to Discord.
- Upload files such as PNG/JPG/GIF, MP3/WAV/M4A, MP4, PDF, ZIP.
- Use from Claude hooks (`Stop` / `Notification`) or manual command execution.

## Required configuration
- Create `.env` from `.env.example`.
- Required key in `.env`:
  - `DISCORD_WEBHOOK_URL`
- Optional keys in `.env`:
  - `DISCORD_USERNAME`
  - `DISCORD_AVATAR_URL`
  - `DISCORD_MAX_FILE_SIZE_MB` (default: `8`, adjust to your Discord/server limits)

## Prerequisites
- Python 3.9+
- Outbound HTTPS access to `discord.com`
- A valid Discord Incoming Webhook URL

## Commands
- Run examples from `discord-webhook-poster/` directory, or replace with absolute script path.
- Text only:
  - `python scripts/discord_webhook_post.py --content "Build finished"`
- Text + files:
  - `python scripts/discord_webhook_post.py --content "Artifacts" --file ./out/report.png --file ./out/voice.mp3`
- Text + files with custom size limit:
  - `python scripts/discord_webhook_post.py --content "Artifacts" --file ./out/voice.mp3 --max-file-size-mb 10`
- Read hook event JSON from stdin:
  - `cat /tmp/hook.json | python scripts/discord_webhook_post.py --stdin-json`
- Use custom `.env` path:
  - `python scripts/discord_webhook_post.py --env-file /path/to/.env --content "Build finished"`

## Hook example
Use `assets/claude-hooks-example.json` as a template and set the absolute path to `discord_webhook_post.py`.

## Notes
- Priority is `CLI arguments > .env`.
- This skill is send-only. It does not receive or process Discord user messages.
- The script uses retry with backoff for transient failures (429/5xx/network errors).
- Webhook URL is never printed in full; logs include a redacted form.
- When `--stdin-json` is used and `stop_hook_active=true`, posting is skipped by default to avoid hook loops (`--allow-stop-hook-active` overrides this).
- Attachment size is validated before upload (8MB per file by default; configurable via `.env`/flag).
- MUST: Do not post secrets or private credentials in message text or attachments.
- MUST: Validate file selection before posting to avoid accidental data leakage.

## Validation
- Prepare env file: `cp .env.example .env` and set your webhook URL.
- Dry run (text): `python scripts/discord_webhook_post.py --content "test" --dry-run`
- Dry run (attachment): `python scripts/discord_webhook_post.py --content "file test" --file /tmp/sample.mp3 --dry-run`
- Loop guard: `printf '{"stop_hook_active":true}' | python scripts/discord_webhook_post.py --stdin-json`
- Size reject: `python scripts/discord_webhook_post.py --content "too large" --file /tmp/large.bin --max-file-size-mb 1 --dry-run`
