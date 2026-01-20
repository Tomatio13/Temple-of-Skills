#!/usr/bin/env python3
"""
Codexの会話履歴から指定日のエントリを収集し、中間データとして保存するスクリプト
"""

import json
import sys
import subprocess
from datetime import datetime, timedelta, time
from pathlib import Path

from config import get_output_dir

# 履歴ディレクトリのパス
SESSION_DIR_PRIMARY = Path.home() / ".codex" / "session"
SESSION_DIR_FALLBACK = Path.home() / ".codex" / "sessions"
OUTPUT_DIR = get_output_dir()


def resolve_session_roots():
    roots = []
    if SESSION_DIR_PRIMARY.exists():
        roots.append(SESSION_DIR_PRIMARY)
    if SESSION_DIR_FALLBACK.exists() and SESSION_DIR_FALLBACK not in roots:
        roots.append(SESSION_DIR_FALLBACK)
    return roots


def parse_timestamp(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def to_local_date_window(target_date):
    local_tz = datetime.now().astimezone().tzinfo
    start = datetime(target_date.year, target_date.month, target_date.day, tzinfo=local_tz)
    end = start + timedelta(days=1)
    return start, end

def get_git_stats(project_path, target_date):
    """指定日のGit統計情報を取得"""
    project_path = Path(project_path)
    if not (project_path / '.git').exists():
        return None

    try:
        # 当日の開始と終了（JST）
        today_start = datetime.combine(target_date, time.min)
        today_end = datetime.combine(target_date, time.max)

        # Git形式の日時範囲
        since = today_start.strftime('%Y-%m-%dT00:00:00')
        until = today_end.strftime('%Y-%m-%dT23:59:59')

        # コミット数を取得
        result = subprocess.run(
            ['git', 'rev-list', '--count', '--after', since, '--before', until, 'HEAD'],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        commit_count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0

        if commit_count == 0:
            return {'commits': 0, 'additions': 0, 'deletions': 0, 'files': 0}

        # 変更統計を取得
        result = subprocess.run(
            ['git', 'log', '--numstat', '--pretty=format:', '--after', since, '--before', until, 'HEAD'],
            cwd=project_path,
            capture_output=True,
            text=True
        )

        additions = 0
        deletions = 0
        files = set()

        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                additions += int(parts[0])
                deletions += int(parts[1])
                if len(parts) >= 3:
                    files.add(parts[2])

        return {
            'commits': commit_count,
            'additions': additions,
            'deletions': deletions,
            'files': len(files),
            'net_lines': additions - deletions
        }
    except Exception as e:
        return None

def load_history(target_date=None):
    """指定日の履歴を読み込む"""
    if target_date is None:
        target_date = datetime.now()

    start_dt, end_dt = to_local_date_window(target_date)
    roots = resolve_session_roots()
    if not roots:
        print(
            f"エラー: {SESSION_DIR_PRIMARY} または {SESSION_DIR_FALLBACK} が見つかりません",
            file=sys.stderr,
        )
        sys.exit(1)

    entries = []
    for root in roots:
        date_dir = root / target_date.strftime("%Y") / target_date.strftime("%m") / target_date.strftime("%d")
        if date_dir.exists():
            session_files = sorted(date_dir.glob("*.jsonl"))
        else:
            session_files = sorted(root.rglob("*.jsonl"))

        for session_file in session_files:
            session_cwd = "unknown"
            session_id = ""
            try:
                with open(session_file, "r") as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                        except json.JSONDecodeError:
                            continue

                        if data.get("type") == "session_meta":
                            payload = data.get("payload", {})
                            session_cwd = payload.get("cwd", session_cwd) or session_cwd
                            session_id = payload.get("id", session_id)[:8]
                            continue

                        ts = parse_timestamp(data.get("timestamp"))
                        if ts is None:
                            continue
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=datetime.now().astimezone().tzinfo)
                        ts_local = ts.astimezone(start_dt.tzinfo)
                        if not (start_dt <= ts_local < end_dt):
                            continue

                        display = None
                        data_type = data.get("type")
                        payload = data.get("payload", {})
                        if data_type == "event_msg" and payload.get("type") == "user_message":
                            message = payload.get("message", "")
                            if message:
                                display = f"User: {message}"
                        elif data_type == "response_item":
                            if payload.get("type") == "message" and payload.get("role") == "assistant":
                                parts = []
                                for item in payload.get("content", []):
                                    if item.get("type") == "output_text":
                                        text = item.get("text", "")
                                        if text:
                                            parts.append(text)
                                if parts:
                                    display = "Assistant: " + "\n".join(parts)

                        if display:
                            entries.append({
                                "timestamp": int(ts_local.timestamp() * 1000),
                                "time": ts_local.strftime("%H:%M"),
                                "project": session_cwd,
                                "project_name": Path(session_cwd).name if session_cwd != "unknown" else "unknown",
                                "session_id": session_id,
                                "display": display,
                            })
            except FileNotFoundError:
                continue

    # 時間順にソート
    entries.sort(key=lambda x: x.get('timestamp', 0))
    return entries

def normalize_entries(entries):
    normalized = []
    for e in entries:
        normalized.append({
            'timestamp': e.get('timestamp', 0),
            'time': e.get('time', ''),
            'project': e.get('project', 'unknown'),
            'project_name': e.get('project_name', 'unknown'),
            'session_id': e.get('session_id', ''),
            'display': e.get('display', ''),
        })
    return normalized


def build_project_index(entries, target_date):
    by_project = {}
    for idx, e in enumerate(entries):
        proj = e.get('project', 'unknown')
        if proj not in by_project:
            by_project[proj] = {
                'path': proj,
                'name': proj.split('/')[-1],
                'entry_ids': [],
                'entries_count': 0,
                'git_stats': None,
            }
        by_project[proj]['entry_ids'].append(idx)
        by_project[proj]['entries_count'] += 1

    total_commits = 0
    total_additions = 0
    total_deletions = 0
    total_files = 0

    for proj, data in by_project.items():
        git_stats = get_git_stats(proj, target_date)
        data['git_stats'] = git_stats
        if git_stats:
            total_commits += git_stats['commits']
            total_additions += git_stats['additions']
            total_deletions += git_stats['deletions']
            total_files += git_stats['files']

    totals = {
        'commits': total_commits,
        'additions': total_additions,
        'deletions': total_deletions,
        'files': total_files,
        'net_lines': total_additions - total_deletions,
    }

    return by_project, totals


def write_json(data, target_date):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    year_dir = OUTPUT_DIR / target_date.strftime("%Y")
    month_dir = year_dir / target_date.strftime("%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    data_path = month_dir / f"{data['date']}_data.json"
    with open(data_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data_path

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Codex履歴から指定日のデータを収集")
    parser.add_argument('-y', '--yesterday', action='store_true', help='昨日のデータを収集')
    parser.add_argument('-d', '--date', help='対象日付 (YYYY-MM-DD), デフォルト: 今日')

    args = parser.parse_args()

    target_date = None
    if args.yesterday:
        target_date = datetime.now() - timedelta(days=1)
    elif args.date:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print(f"エラー: 日付フォーマットが正しくありません。YYYY-MM-DD形式で指定してください", file=sys.stderr)
            sys.exit(1)

    if target_date is None:
        target_date = datetime.now()

    raw_entries = load_history(target_date)
    normalized_entries = normalize_entries(raw_entries)
    by_project, git_totals = build_project_index(normalized_entries, target_date)

    data = {
        'date': target_date.strftime('%Y-%m-%d'),
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'entries_count': len(normalized_entries),
        'projects_count': len(by_project),
        'entries': normalized_entries,
        'projects': by_project,
        'git_totals': git_totals,
    }

    data_path = write_json(data, target_date)
    print(f"保存しました: {data_path}")
    print(f"総エントリ数: {len(normalized_entries)}件 / プロジェクト数: {len(by_project)}個")

if __name__ == '__main__':
    main()
