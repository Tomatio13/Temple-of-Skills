#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 5 ]]; then
  echo "Usage: $0 <db_path> <question> <answer> <summary> <keywords_csv>" >&2
  exit 1
fi

db_path="$1"
question="$2"
answer="$3"
summary="$4"
keywords="$5"

escape_sql() {
  printf "%s" "$1" | sed "s/'/''/g"
}

q_escaped="$(escape_sql "$question")"
a_escaped="$(escape_sql "$answer")"
s_escaped="$(escape_sql "$summary")"
k_escaped="$(escape_sql "$keywords")"

sqlite3 "$db_path" <<SQL
INSERT INTO qa_entries (question, answer, summary, keywords, updated_at)
VALUES ('$q_escaped', '$a_escaped', '$s_escaped', '$k_escaped', datetime('now'));
SQL

echo "Inserted 1 row into qa_entries"
