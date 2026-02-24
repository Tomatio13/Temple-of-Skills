#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 6 ]]; then
  echo "Usage: $0 <db_path> <id> <question> <answer> <summary> <keywords_csv>" >&2
  exit 1
fi

db_path="$1"
id="$2"
question="$3"
answer="$4"
summary="$5"
keywords="$6"

if ! [[ "$id" =~ ^[0-9]+$ ]]; then
  echo "Error: <id> must be an integer" >&2
  exit 1
fi

escape_sql() {
  printf "%s" "$1" | sed "s/'/''/g"
}

q_escaped="$(escape_sql "$question")"
a_escaped="$(escape_sql "$answer")"
s_escaped="$(escape_sql "$summary")"
k_escaped="$(escape_sql "$keywords")"

affected_rows="$(sqlite3 "$db_path" <<SQL
UPDATE qa_entries
SET question = '$q_escaped',
    answer = '$a_escaped',
    summary = '$s_escaped',
    keywords = '$k_escaped',
    updated_at = datetime('now')
WHERE id = $id;
SELECT changes();
SQL
)"

if [[ "$affected_rows" -eq 0 ]]; then
  echo "Updated 0 rows (id=$id not found)" >&2
  exit 1
fi

echo "Updated 1 row in qa_entries (id=$id)"
