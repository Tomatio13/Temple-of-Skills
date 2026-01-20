#!/usr/bin/env python3
"""
LLMが生成した日報MarkdownをCodex用のファイル名で保存するスクリプト
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

from config import get_output_dir


def parse_date_arg(args):
    if args.yesterday:
        return datetime.now() - timedelta(days=1)
    if args.date:
        return datetime.strptime(args.date, "%Y-%m-%d")
    return datetime.now()


def output_path(target_date):
    output_dir = get_output_dir()
    year_dir = output_dir / target_date.strftime("%Y")
    month_dir = year_dir / target_date.strftime("%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    return month_dir / f"{target_date.strftime('%Y-%m-%d')}_codex_daily.md"


def main():
    parser = argparse.ArgumentParser(description="日報Markdownを保存")
    parser.add_argument("-y", "--yesterday", action="store_true", help="昨日のデータ")
    parser.add_argument("-d", "--date", help="対象日付 (YYYY-MM-DD), デフォルト: 今日")
    args = parser.parse_args()

    target_date = parse_date_arg(args)
    content = sys.stdin.read()
    if not content.strip():
        print("エラー: 標準入力から日報内容を受け取れませんでした", file=sys.stderr)
        sys.exit(1)

    path = output_path(target_date)
    path.write_text(content, encoding="utf-8")
    print(f"保存しました: {path}")



if __name__ == "__main__":
    main()
