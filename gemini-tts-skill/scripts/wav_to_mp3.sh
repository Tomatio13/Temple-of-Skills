#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  wav_to_mp3.sh --input input.wav --output output.mp3 [--quality 2]

Notes:
  quality is LAME VBR quality (0=best, 9=smallest). Recommended: 2.
USAGE
}

INPUT_WAV=""
OUTPUT_MP3=""
QUALITY="2"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)
      INPUT_WAV="${2:-}"
      shift 2
      ;;
    --output)
      OUTPUT_MP3="${2:-}"
      shift 2
      ;;
    --quality)
      QUALITY="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$INPUT_WAV" || -z "$OUTPUT_MP3" ]]; then
  echo "--input and --output are required." >&2
  usage >&2
  exit 1
fi

if [[ ! -f "$INPUT_WAV" ]]; then
  echo "Input WAV file not found: $INPUT_WAV" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required but not found in PATH." >&2
  exit 1
fi

ffmpeg -y -hide_banner -loglevel error \
  -i "$INPUT_WAV" \
  -codec:a libmp3lame -q:a "$QUALITY" \
  "$OUTPUT_MP3"

echo "MP3 saved: $OUTPUT_MP3"
