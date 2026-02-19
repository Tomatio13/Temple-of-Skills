<h1 align="center">gemini-tts-skill</h1>

<p align="center">
  Script set to generate Japanese speech with Gemini TTS API and export final output as MP3
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Node.js-18%2B-339933?logo=node.js&logoColor=white" alt="Node.js"/>
  <img src="https://img.shields.io/badge/ffmpeg-required-007808" alt="ffmpeg"/>
  <img src="https://img.shields.io/badge/curl-required-00599C" alt="curl"/>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

## ✨ Overview
This project is a CLI toolset that turns Gemini TTS API audio responses (PCM) into practical audio files and exports the final result as `mp3`.

Core flow:
1. Split input text into sentence-based chunks (long-text friendly)
2. Generate speech for each chunk with Gemini TTS API
3. Convert PCM response data to WAV
4. Concatenate WAV parts and transcode to final MP3

Key features:
- Stable long-text synthesis with tunable `--max-chars`
- Flexible output control via `--output-dir` and `--output-base`
- Debug-friendly intermediate artifacts with `--keep-temp`
- `.env`-first API key lookup suitable for local and scripted runs

Typical use cases:
- Voice-over asset generation for videos
- Batch Japanese text narration jobs
- Rapid prototyping of TTS automation pipelines

## ✅ Requirements
- `node` (recommended: 18+)
- `curl`
- `ffmpeg`

## ⚙️ Setup
Create `.env` from `.env.example`.

```bash
cp .env.example .env
```

## 🔐 API Key Lookup Order
`scripts/generate_tts.sh` resolves `GEMINI_API_KEY` in this order:

1. `./.env` (current working directory)
2. `scripts/../.env` (repo root in this project)
3. Environment variable `GEMINI_API_KEY`

## 🚀 Usage
```bash
./scripts/tts_to_mp3.sh \
  --text "Hello. This is a Gemini TTS test." \
  --voice Zephyr \
  --max-chars 300 \
  --output-dir outputs \
  --output-base sample
```

Output:
- `outputs/sample.mp3`

## 🧩 Main Options
- `--text` / `--text-file`: Input text
- `--voice`: Voice name (e.g. `Zephyr`, `Kore`, `Aoede`)
- `--max-chars`: Chunk threshold (recommended: `200-400`)
- `--output-dir`: Output directory
- `--output-base`: Output filename base
- `--keep-temp`: Keep intermediate artifacts

## 🧪 Validation
```bash
TARGET="outputs/sample.mp3"
ffprobe -v error -show_entries stream=codec_name -of default=nw=1:nk=1 "$TARGET"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$TARGET"
```
