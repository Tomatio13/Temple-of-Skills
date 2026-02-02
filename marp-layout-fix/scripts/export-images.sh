#!/usr/bin/env bash
set -euo pipefail

md_path="${1:-}"
out_dir="${2:-}"

if [[ -z "$md_path" || -z "$out_dir" ]]; then
  echo "usage: export-images.sh /absolute/path/to/slides.md /absolute/path/to/out" >&2
  exit 2
fi

if ! command -v marp >/dev/null 2>&1; then
  echo "error: marp not found in PATH" >&2
  exit 1
fi

marp --images png --allow-local-files -o "$out_dir" "$md_path"
