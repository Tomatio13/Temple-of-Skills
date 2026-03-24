#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime

WEEKDAY_JA = ["月", "火", "水", "木", "金", "土", "日"]
WEEKDAY_JA_FULL = [f"{day}曜日" for day in WEEKDAY_JA]
WEEKDAY_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAY_EN_FULL = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Format current or provided datetime with explicit tokens."
    )
    parser.add_argument(
        "--format",
        required=True,
        help="Output format using tokens like {YYYY}, {MM}, {DD}, {HH}, {mm}, {ss}, {W_JA_FULL}.",
    )
    parser.add_argument(
        "--datetime",
        dest="datetime_value",
        help="Datetime to format. Uses current local time when omitted. Accepts ISO 8601 or 'YYYY-MM-DD HH:MM:SS'.",
    )
    return parser.parse_args()


def parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now()

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise SystemExit(
            "Invalid --datetime value. Use ISO 8601 or 'YYYY-MM-DD HH:MM:SS', "
            "for example: '2026-03-13 09:15:30' or '2026-03-13T09:15:30+09:00'."
        ) from exc

    if parsed.tzinfo is None:
        return parsed
    return parsed.astimezone()


def build_tokens(dt: datetime) -> dict[str, str]:
    weekday = dt.weekday()
    return {
        "{YYYY}": f"{dt.year:04d}",
        "{YY}": f"{dt.year % 100:02d}",
        "{MM}": f"{dt.month:02d}",
        "{M}": str(dt.month),
        "{DD}": f"{dt.day:02d}",
        "{D}": str(dt.day),
        "{HH}": f"{dt.hour:02d}",
        "{H}": str(dt.hour),
        "{mm}": f"{dt.minute:02d}",
        "{m}": str(dt.minute),
        "{ss}": f"{dt.second:02d}",
        "{s}": str(dt.second),
        "{W_JA_FULL}": WEEKDAY_JA_FULL[weekday],
        "{W_JA}": WEEKDAY_JA[weekday],
        "{W_EN_FULL}": WEEKDAY_EN_FULL[weekday],
        "{W_EN}": WEEKDAY_EN[weekday],
    }


def format_datetime(template: str, dt: datetime) -> str:
    result = template
    tokens = build_tokens(dt)
    for token in sorted(tokens, key=len, reverse=True):
        result = result.replace(token, tokens[token])
    return result


def main() -> None:
    args = parse_args()
    dt = parse_datetime(args.datetime_value)
    print(format_datetime(args.format, dt))


if __name__ == "__main__":
    main()
