#!/bin/bash
# List saved HTML files in the configured local directory, optionally filtered by
# name prefix. Useful for finding existing docs to revisit locally.
#
# Usage:
#   list.sh                   # all HTML files
#   list.sh setup-guide       # files matching prefix "setup-guide"
#   list.sh setup-guide --keys-only   # just filenames, no path prefix

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$SCRIPT_DIR/../config.json"

if [[ ! -f "$CONFIG" ]]; then
  echo "error: config.json not found at $CONFIG. see references/setup.md." >&2
  exit 1
fi

read_cfg() {
  python3 -c "import json; v=json.load(open('$CONFIG')).get('$1'); print('' if v is None else v)"
}

expand_path() {
  python3 -c 'import os, sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$1"
}

OUTPUT_DIR_RAW=$(read_cfg output_dir)

if [[ -z "$OUTPUT_DIR_RAW" || "$OUTPUT_DIR_RAW" == "<"* ]]; then
  echo "error: config.json has unfilled placeholders. see references/setup.md." >&2
  exit 1
fi

OUTPUT_DIR=$(expand_path "$OUTPUT_DIR_RAW")

PREFIX="${1:-}"
KEYS_ONLY=0
if [[ "${2:-}" == "--keys-only" || "${1:-}" == "--keys-only" ]]; then
  KEYS_ONLY=1
  PREFIX="${1:-}"
  [[ "$PREFIX" == "--keys-only" ]] && PREFIX=""
fi

if [[ ! -d "$OUTPUT_DIR" ]]; then
  exit 0
fi

LIST=$(find "$OUTPUT_DIR" -maxdepth 1 -type f -name '*.html' -printf '%f\n' \
  | sort \
  | awk -v prefix="$PREFIX" 'prefix == "" || index($0, prefix) == 1')

if [[ -z "$LIST" ]]; then
  exit 0
fi

if [[ "$KEYS_ONLY" == "1" ]]; then
  echo "$LIST"
else
  while IFS= read -r key; do
    printf '%s/%s\n' "$OUTPUT_DIR" "$key"
  done <<< "$LIST"
fi
