---
name: current-time
description: Get the current time or today's date, or format the current or specified date/time into a requested string with year, month, day, hour, minute, second, and weekday tokens. Use when a user asks what time it is now, wants today's date, wants a date with weekday, or requests a custom datetime string such as a timestamp, filename label, or Japanese date text, for example "今何時?", "今日の日付を返して", "曜日付きで出して", or "この日時を整形して".
---

# Datetime Format String

## Overview

Return a datetime string in a user-specified format.
The formatter is token-based and does not depend on process locale for weekday names.
Use `scripts/format_datetime.py` for deterministic output instead of manually composing the string.

## Workflow

1. Identify the target datetime.
   If the user does not provide one, use the current local datetime in the execution environment timezone.
2. Choose the output format.
   - "今何時?" -> `{HH}:{mm}:{ss}`
   - "今日の日付" -> `{YYYY}-{MM}-{DD}`
   - "今日の日付と曜日" -> `{YYYY}-{MM}-{DD} ({W_JA})`
3. Convert any custom layout into the supported tokens below.
4. Run the formatter script and return only the formatted string unless the user asks for explanation.

## Supported Tokens

- `{YYYY}`: 4-digit year
- `{YY}`: 2-digit year
- `{MM}`: zero-padded month
- `{M}`: month
- `{DD}`: zero-padded day
- `{D}`: day
- `{HH}`: zero-padded hour (24h)
- `{H}`: hour (24h)
- `{mm}`: zero-padded minute
- `{m}`: minute
- `{ss}`: zero-padded second
- `{s}`: second
- `{W_JA}`: Japanese weekday short form (`月`)
- `{W_JA_FULL}`: Japanese weekday full form (`月曜日`)
- `{W_EN}`: English weekday short form (`Mon`)
- `{W_EN_FULL}`: English weekday full form (`Monday`)

## Command

```bash
python scripts/format_datetime.py --format '{YYYY}年{MM}月{DD}日（{W_JA_FULL}） {HH}:{mm}:{ss}'
```

Use `--datetime` when the user provides a target datetime:

```bash
python scripts/format_datetime.py \
  --datetime '2026-03-13 09:15:30' \
  --format '{YYYY}/{MM}/{DD} {W_EN} {HH}:{mm}:{ss}'
```

## Input Rules

- Accept these forms for `--datetime`:
  - `2026-03-13`
  - `2026-03-13 09:15:30`
  - `2026-03-13T09:15:30+09:00`
  - `2026-03-13T00:15:30Z`
- Normalize a trailing `Z` to UTC, then convert it to the execution environment local timezone.
- If the requested layout uses plain prose, map it to token form before running the script.
- If the user only wants a formatted result, do not include surrounding explanation.

## Examples

- `'{YYYY}-{MM}-{DD}'` -> `2026-03-13`
- `'{YYYY}年{M}月{D}日 {W_JA_FULL}'` -> `2026年3月13日 金曜日`
- `'{YY}{MM}{DD}_{HH}{mm}{ss}'` -> `260313_091530`

## Notes

- Prefer this skill over ad-hoc manual formatting when weekday text or zero-padding matters.
- If the user explicitly asks for a timezone-specific answer and it cannot be inferred from context, confirm the timezone before formatting.
