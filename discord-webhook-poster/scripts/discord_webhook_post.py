#!/usr/bin/env python3
"""Post text and attachments to Discord webhook."""

from __future__ import annotations

import argparse
import json
import mimetypes
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_RETRY_COUNT = 2
DEFAULT_BACKOFF_SECONDS = 1.5
MAX_DISCORD_FILES = 10
DEFAULT_MAX_FILE_SIZE_MB = 8.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post message/files to Discord webhook")
    parser.add_argument("--env-file", default=".env", help="Path to .env file (default: .env)")
    parser.add_argument("--webhook-url", help="Discord webhook URL")
    parser.add_argument("--content", default="", help="Message content")
    parser.add_argument("--content-file", help="Read message content from a file")
    parser.add_argument("--file", action="append", default=[], help="Attachment path (repeatable)")
    parser.add_argument("--username", help="Override bot username")
    parser.add_argument("--avatar-url", help="Override avatar URL")
    parser.add_argument("--stdin-json", action="store_true", help="Read JSON event payload from stdin")
    parser.add_argument(
        "--allow-stop-hook-active",
        action="store_true",
        help="Send even when stdin JSON contains stop_hook_active=true",
    )
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="HTTP timeout seconds")
    parser.add_argument("--retry", type=int, default=DEFAULT_RETRY_COUNT, help="Retry count for transient failures")
    parser.add_argument(
        "--retry-backoff",
        type=float,
        default=DEFAULT_BACKOFF_SECONDS,
        help="Base seconds for exponential backoff",
    )
    parser.add_argument(
        "--max-file-size-mb",
        type=float,
        default=None,
        help="Maximum size per attachment in MB (default: 8, overridable by .env DISCORD_MAX_FILE_SIZE_MB)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print payload summary only")
    return parser.parse_args()


def read_text_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"content-file read failed: {path}: {exc}") from exc


def read_stdin_json() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"stdin JSON parse failed: {exc}") from exc
    if not isinstance(obj, dict):
        raise ValueError("stdin JSON root must be an object")
    return obj


def load_dotenv(path: str) -> dict[str, str]:
    env_path = Path(path).expanduser().resolve()
    if not env_path.exists():
        return {}
    if not env_path.is_file():
        raise ValueError(f".env path is not a file: {path}")

    loaded: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        if raw.startswith("export "):
            raw = raw[len("export ") :].strip()
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        loaded[key] = value
    return loaded


def redact_webhook(url: str) -> str:
    if not url:
        return ""
    if "/api/webhooks/" not in url:
        return "<invalid-webhook-format>"
    head, tail = url.rsplit("/", 1)
    return f"{head}/***{tail[-4:]}"


def ensure_files(paths: Iterable[str], max_file_size_mb: float) -> list[Path]:
    normalized: list[Path] = []
    max_bytes = int(max_file_size_mb * 1024 * 1024)
    for p in paths:
        fp = Path(p).expanduser().resolve()
        if not fp.exists() or not fp.is_file():
            raise ValueError(f"attachment not found or not a file: {p}")
        size = fp.stat().st_size
        if size > max_bytes:
            raise ValueError(
                f"attachment too large: {p} ({size} bytes) exceeds {max_file_size_mb:.2f} MB"
            )
        normalized.append(fp)
    if len(normalized) > MAX_DISCORD_FILES:
        raise ValueError(f"too many attachments: {len(normalized)} > {MAX_DISCORD_FILES}")
    return normalized


def build_content(base: str, event_payload: dict) -> str:
    if not event_payload:
        return base

    lines: list[str] = []
    event = event_payload.get("hook_event_name")
    session_id = event_payload.get("session_id")
    cwd = event_payload.get("cwd")

    if event:
        lines.append(f"event: {event}")
    if session_id:
        lines.append(f"session: {session_id}")
    if cwd:
        lines.append(f"cwd: {cwd}")

    assistant = event_payload.get("assistant_message")
    if isinstance(assistant, str) and assistant.strip():
        lines.append(assistant.strip()[:1200])

    composed = "\n".join(lines).strip()
    if base.strip() and composed:
        return f"{base.strip()}\n\n{composed}"
    return base.strip() or composed


def json_payload(content: str, username: str | None, avatar_url: str | None) -> dict:
    payload: dict[str, object] = {}
    if content:
        payload["content"] = content
    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar_url"] = avatar_url
    return payload


def encode_multipart(payload: dict, files: list[Path]) -> tuple[bytes, str]:
    boundary = f"----discordboundary{random.randint(100000, 999999)}"
    parts: list[bytes] = []

    payload_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    parts.append(f"--{boundary}\r\n".encode("utf-8"))
    parts.append(b'Content-Disposition: form-data; name="payload_json"\r\n')
    parts.append(b"Content-Type: application/json\r\n\r\n")
    parts.append(payload_bytes)
    parts.append(b"\r\n")

    for i, file_path in enumerate(files):
        mime, _ = mimetypes.guess_type(str(file_path))
        if not mime:
            mime = "application/octet-stream"
        content = file_path.read_bytes()

        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(
            (
                f'Content-Disposition: form-data; name="files[{i}]"; '
                f'filename="{file_path.name}"\r\n'
            ).encode("utf-8")
        )
        parts.append(f"Content-Type: {mime}\r\n\r\n".encode("utf-8"))
        parts.append(content)
        parts.append(b"\r\n")

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def should_retry(status: int) -> bool:
    return status == 429 or 500 <= status <= 599


def parse_retry_after(response_bytes: bytes) -> float | None:
    try:
        data = json.loads(response_bytes.decode("utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    value = data.get("retry_after")
    if isinstance(value, (int, float)):
        return float(value)
    return None


def post_discord(
    webhook_url: str,
    payload: dict,
    attachments: list[Path],
    timeout: float,
    retry: int,
    retry_backoff: float,
) -> None:
    if attachments:
        body, content_type = encode_multipart(payload, attachments)
    else:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        content_type = "application/json"

    attempt = 0
    while True:
        req = urllib.request.Request(
            webhook_url,
            data=body,
            method="POST",
            headers={
                "Content-Type": content_type,
                "User-Agent": "discord-webhook-poster/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                if 200 <= status < 300:
                    return
                if should_retry(status) and attempt < retry:
                    wait = retry_backoff * (2**attempt)
                    time.sleep(wait)
                    attempt += 1
                    continue
                raise RuntimeError(f"discord webhook failed: status={status}")
        except urllib.error.HTTPError as exc:
            body_bytes = exc.read()
            if should_retry(exc.code) and attempt < retry:
                retry_after = parse_retry_after(body_bytes)
                wait = retry_after if retry_after is not None else retry_backoff * (2**attempt)
                time.sleep(max(wait, 0.1))
                attempt += 1
                continue
            detail = body_bytes.decode("utf-8", errors="replace")[:500]
            raise RuntimeError(f"discord webhook failed: status={exc.code}, body={detail}") from exc
        except urllib.error.URLError as exc:
            if attempt < retry:
                wait = retry_backoff * (2**attempt)
                time.sleep(wait)
                attempt += 1
                continue
            raise RuntimeError(f"network error: {exc}") from exc


def main() -> int:
    args = parse_args()
    try:
        dotenv = load_dotenv(args.env_file)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    webhook_url = (
        args.webhook_url
        or dotenv.get("DISCORD_WEBHOOK_URL")
        or dotenv.get("CLAUDE_DISCORD_WEBHOOK_URL")
    )
    if not webhook_url:
        print("error: webhook URL is required (--webhook-url or .env DISCORD_WEBHOOK_URL)", file=sys.stderr)
        return 2

    username = args.username or dotenv.get("DISCORD_USERNAME")
    avatar_url = args.avatar_url or dotenv.get("DISCORD_AVATAR_URL")
    max_file_size_mb = args.max_file_size_mb
    if max_file_size_mb is None:
        raw_max_file_size_mb = dotenv.get("DISCORD_MAX_FILE_SIZE_MB", str(DEFAULT_MAX_FILE_SIZE_MB))
        try:
            max_file_size_mb = float(raw_max_file_size_mb)
        except ValueError:
            print(f"error: invalid DISCORD_MAX_FILE_SIZE_MB: {raw_max_file_size_mb}", file=sys.stderr)
            return 2
    if max_file_size_mb <= 0:
        print("error: max file size must be > 0 MB", file=sys.stderr)
        return 2

    try:
        content = args.content
        if args.content_file:
            file_content = read_text_file(args.content_file)
            content = f"{content}\n{file_content}".strip() if content else file_content

        event_payload = read_stdin_json() if args.stdin_json else {}
        if event_payload.get("stop_hook_active") and not args.allow_stop_hook_active:
            print("skipped: stop_hook_active=true")
            return 0
        content = build_content(content, event_payload)

        attachments = ensure_files(args.file, max_file_size_mb)

        if not content and not attachments:
            raise ValueError("either content or at least one --file is required")

        payload = json_payload(content, username, avatar_url)

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "webhook": redact_webhook(webhook_url),
                        "content_preview": content[:120],
                        "attachment_count": len(attachments),
                        "attachments": [p.name for p in attachments],
                    },
                    ensure_ascii=False,
                )
            )
            return 0

        post_discord(
            webhook_url=webhook_url,
            payload=payload,
            attachments=attachments,
            timeout=args.timeout,
            retry=max(0, args.retry),
            retry_backoff=max(0.1, args.retry_backoff),
        )
        print(
            f"posted: webhook={redact_webhook(webhook_url)} content={len(content)}chars attachments={len(attachments)}"
        )
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
