#!/usr/bin/env python3
"""
中間データからLLM用プロンプトを生成するスクリプト
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from config import get_output_dir

OUTPUT_DIR = get_output_dir()


def parse_date_arg(args):
    if args.yesterday:
        return datetime.now() - timedelta(days=1)
    if args.date:
        return datetime.strptime(args.date, "%Y-%m-%d")
    return datetime.now()


def load_data(target_date):
    path = OUTPUT_DIR / target_date.strftime("%Y") / target_date.strftime("%m") / f"{target_date.strftime('%Y-%m-%d')}_data.json"
    if not path.exists():
        raise FileNotFoundError(str(path))
    with open(path, "r") as f:
        return json.load(f), path


def build_context(data):
    entries = []
    for e in data.get("entries", []):
        entries.append({
            "time": e.get("time"),
            "project": e.get("project_name"),
            "display": e.get("display"),
        })
    ctx = {
        "date": data.get("date"),
        "entries_count": data.get("entries_count"),
        "projects_count": data.get("projects_count"),
        "git_totals": data.get("git_totals", {}),
        "projects": data.get("projects", {}),
        "entries": entries,
    }
    return ctx


def render_prompt(template_path, context):
    with open(template_path, "r") as f:
        template = f.read()
    payload = json.dumps(context, ensure_ascii=False, indent=2)
    return template.replace("{{CONTEXT_JSON}}", payload)


def main():
    parser = argparse.ArgumentParser(description="LLMプロンプトを生成")
    parser.add_argument('-y', '--yesterday', action='store_true', help='昨日のデータ')
    parser.add_argument('-d', '--date', help='対象日付 (YYYY-MM-DD), デフォルト: 今日')
    parser.add_argument('--keep-temp', action='store_true', help='中間データを保持する')
    args = parser.parse_args()

    target_date = parse_date_arg(args)
    data, data_path = load_data(target_date)
    context = build_context(data)

    base = Path(__file__).resolve().parent.parent / "references"
    daily_prompt = render_prompt(base / "prompt_daily.md", context)
    print(daily_prompt)

    if not args.keep_temp:
        try:
            os.remove(data_path)
            print(f"削除しました: {data_path}")
        except OSError:
            pass


if __name__ == '__main__':
    main()
