#!/bin/bash
# Save HTML into a configured local directory and print the absolute file path.
# Reads HTML from stdin (preferred) or a file path.
#
# Naming:
#   - Name provided  -> <name>-<8hex>.html  (persistent doc; for later reference)
#   - No name        -> <YYYY-MM-DDTHHMM>-<8hex>.html  (timestamp; ephemeral output)
#
# Usage:
#   echo "$HTML" | publish.sh                    # -> /.../2026-...-xxxxxx.html
#   echo "$HTML" | publish.sh setup-guide        # -> /.../setup-guide-xxxxxx.html
#   publish.sh path/to/file.html                 # file mode, timestamp name
#   publish.sh path/to/file.html setup-guide     # file mode, named

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
mkdir -p "$OUTPUT_DIR"

SRC=""
NAME=""
CLEANUP_SRC=""
CLEANUP_DEST=""

cleanup() {
  [[ -n "$CLEANUP_SRC" ]] && rm -f "$CLEANUP_SRC"
  [[ -n "$CLEANUP_DEST" ]] && rm -f "$CLEANUP_DEST"
}

trap cleanup EXIT

if [[ -t 0 ]]; then
  if [[ $# -eq 0 ]]; then
    echo "usage: publish.sh < file.html [name]   OR   publish.sh path/to/file.html [name]" >&2
    exit 1
  fi
  if [[ -f "$1" ]]; then
    SRC="$1"
    NAME="${2:-}"
  else
    echo "error: file not found: $1" >&2
    exit 1
  fi
else
  SRC=$(mktemp -t html-output.XXXXXX)
  CLEANUP_SRC="$SRC"
  cat > "$SRC"
  NAME="${1:-}"
fi

if [[ "$NAME" == *.html ]]; then
  KEY="$NAME"
elif [[ -n "$NAME" ]]; then
  SLUG=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9-]+/-/g; s/^-+|-+$//g; s/-+/-/g')
  if [[ -z "$SLUG" ]]; then
    echo "error: name must contain alphanumeric chars" >&2
    exit 1
  fi
  RAND=$(python3 -c "import secrets; print(secrets.token_hex(4))")
  KEY="${SLUG}-${RAND}.html"
else
  TS=$(date -u +%Y-%m-%dT%H%M)
  RAND=$(python3 -c "import secrets; print(secrets.token_hex(4))")
  KEY="${TS}-${RAND}.html"
fi

DEST="$OUTPUT_DIR/$KEY"
TMP_DEST=$(mktemp "$OUTPUT_DIR/.html-output.XXXXXX")
CLEANUP_DEST="$TMP_DEST"

cp "$SRC" "$TMP_DEST"
mv "$TMP_DEST" "$DEST"
CLEANUP_DEST=""

echo "$DEST"
