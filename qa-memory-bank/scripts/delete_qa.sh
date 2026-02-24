#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <db_path> <id>" >&2
  exit 1
fi

db_path="$1"
id="$2"

if ! [[ "$id" =~ ^[0-9]+$ ]]; then
  echo "Error: <id> must be an integer" >&2
  exit 1
fi

affected_rows="$(sqlite3 "$db_path" <<SQL
DELETE FROM qa_entries
WHERE id = $id;
SELECT changes();
SQL
)"

if [[ "$affected_rows" -eq 0 ]]; then
  echo "Deleted 0 rows (id=$id not found)" >&2
  exit 1
fi

echo "Deleted 1 row from qa_entries (id=$id)"
