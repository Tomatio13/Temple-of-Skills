#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <db_path>" >&2
  exit 1
fi

db_path="$1"
db_dir="$(dirname "$db_path")"
mkdir -p "$db_dir"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
schema_path="${script_dir}/../references/schema.sql"

table_exists="$(sqlite3 "$db_path" "SELECT 1 FROM sqlite_master WHERE type='table' AND name='qa_entries';")"
if [[ -n "$table_exists" ]] && ! sqlite3 "$db_path" "PRAGMA table_info(qa_entries);" | grep -q "|keywords|"; then
  sqlite3 "$db_path" "ALTER TABLE qa_entries ADD COLUMN keywords TEXT NOT NULL DEFAULT '';"
fi

sqlite3 "$db_path" < "$schema_path"

echo "Initialized: $db_path"
