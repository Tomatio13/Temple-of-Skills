#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CSS_FILE="$SCRIPT_DIR/../assets/pdf-style.css"
CROP_SCRIPT="$SCRIPT_DIR/crop_pdf.py"
VENV_DIR="${VENV_DIR:-.venv}"

PDF_OPTIONS='{"width":"280mm","margin":{"top":"15mm","bottom":"15mm","left":"15mm","right":"15mm"},"printBackground":true,"preferCSSPageSize":true}'

if [[ $# -lt 1 ]]; then
  echo "Usage: convert_md_to_pdf.sh <file1.md> [file2.md ...]" >&2
  exit 1
fi

# Ensure PyMuPDF is available via venv; create/install if missing.
ensure_venv_with_pymupdf() {
  if [[ ! -x "$VENV_DIR/bin/python3" ]]; then
    if command -v uv >/dev/null 2>&1; then
      uv venv "$VENV_DIR"
    else
      python3 -m venv "$VENV_DIR"
    fi
  fi

  if ! "$VENV_DIR/bin/python3" - <<'PY' >/dev/null 2>&1
import fitz
print(fitz.__doc__)
PY
  then
    if command -v uv >/dev/null 2>&1; then
      uv pip install pymupdf
    else
      "$VENV_DIR/bin/python3" -m pip install pymupdf
    fi
  fi
}

ensure_md_to_pdf() {
  if command -v md-to-pdf >/dev/null 2>&1; then
    return 0
  fi

  echo "Error: md-to-pdf is not installed."
  echo "Install md-to-pdf globally with npm? [y/N]"
  read -r install_reply
  if [[ "$install_reply" != "y" && "$install_reply" != "Y" ]]; then
    echo "Aborted: md-to-pdf is required."
    exit 1
  fi

  if command -v npm >/dev/null 2>&1; then
    npm install -g md-to-pdf
  else
    echo "Error: npm is not available. Please install md-to-pdf manually."
    exit 1
  fi
}

ensure_md_to_pdf
ensure_venv_with_pymupdf

for md_file in "$@"; do
  if [[ ! -f "$md_file" ]]; then
    echo "Skip (not found): $md_file" >&2
    continue
  fi

  echo "Converting: $md_file"
  md-to-pdf "$md_file" \
    --pdf-options "$PDF_OPTIONS" \
    --stylesheet "$CSS_FILE" \
    --launch-options '{"args":["--no-sandbox","--disable-setuid-sandbox"]}'

  pdf_file="${md_file%.md}.pdf"
  "$VENV_DIR/bin/python3" "$CROP_SCRIPT" "$pdf_file"
done

echo "Done!"
