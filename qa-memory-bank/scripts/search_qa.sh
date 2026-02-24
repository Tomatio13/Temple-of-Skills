#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Usage: $0 <db_path> <keyword> [--full]" >&2
  exit 1
fi

db_path="$1"
keyword="$2"
full_mode="${3:-}"

if [[ -n "$full_mode" && "$full_mode" != "--full" ]]; then
  echo "Error: third argument must be --full" >&2
  exit 1
fi

escape_sql() {
  printf "%s" "$1" | sed "s/'/''/g"
}

k_escaped="$(escape_sql "$keyword")"

if [[ "$full_mode" == "--full" ]]; then
  sqlite3 -header -column "$db_path" <<SQL
SELECT
  id,
  created_at,
  updated_at,
  question,
  keywords,
  answer,
  summary
FROM qa_entries
WHERE question LIKE '%$k_escaped%'
   OR answer LIKE '%$k_escaped%'
   OR summary LIKE '%$k_escaped%'
   OR keywords LIKE '%$k_escaped%'
ORDER BY updated_at DESC;
SQL
else
  sqlite3 -header -column "$db_path" <<SQL
SELECT
  id,
  created_at,
  updated_at,
  question,
  keywords,
  summary
FROM qa_entries
WHERE question LIKE '%$k_escaped%'
   OR answer LIKE '%$k_escaped%'
   OR summary LIKE '%$k_escaped%'
   OR keywords LIKE '%$k_escaped%'
ORDER BY updated_at DESC;
SQL
fi
