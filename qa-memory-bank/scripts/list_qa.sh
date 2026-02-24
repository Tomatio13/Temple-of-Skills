#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <db_path>" >&2
  exit 1
fi

db_path="$1"

sqlite3 -header -column "$db_path" <<'SQL'
SELECT
  id,
  created_at,
  updated_at,
  question,
  keywords,
  summary
FROM qa_entries
ORDER BY updated_at DESC;
SQL
