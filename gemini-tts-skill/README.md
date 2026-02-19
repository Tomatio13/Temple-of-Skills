<h1 align="center">gemini-tts-skill</h1>

<p align="center">
  Gemini TTS APIで日本語テキストを音声化し、最終的にMP3を生成するスクリプト集
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

## ✨ 概要
このプロジェクトは、Gemini TTS API の音声レスポンス（PCM）を扱いやすい音声ファイルに変換し、最終成果物を `mp3` として出力するためのCLIツールセットです。

主な処理フロー:
1. テキストを文単位で自動分割（長文対応）
2. Gemini TTS API でチャンクごとに音声生成
3. PCMレスポンスをWAVへ変換
4. WAVを結合し、最終的にMP3へ変換

主な特徴:
- 長文入力でも `--max-chars` で安定生成しやすい
- `--output-dir` / `--output-base` で出力先を柔軟に制御
- `--keep-temp` で中間JSON/WAVを保持してデバッグ可能
- `.env` 優先のAPIキー解決で運用環境に合わせやすい

想定ユースケース:
- 動画ナレーション用の音声素材作成
- 日本語テキストの読み上げバッチ生成
- TTSパイプラインのプロトタイプ検証

## ✅ 必要要件
- `node` (推奨: 18以上)
- `curl`
- `ffmpeg`

## ⚙️ セットアップ
`.env.example` を参考に `.env` を作成します。

```bash
cp .env.example .env
```

## 🔐 APIキーの読み出し順
`scripts/generate_tts.sh` は次の順で `GEMINI_API_KEY` を参照します。

1. `./.env`（実行時のカレントディレクトリ）
2. `scripts/../.env`（このリポジトリでは実質ルートの`.env`）
3. 環境変数 `GEMINI_API_KEY`

## 🚀 使い方
```bash
./scripts/tts_to_mp3.sh \
  --text "こんにちは。Gemini TTSの音声テストです。" \
  --voice Zephyr \
  --max-chars 300 \
  --output-dir outputs \
  --output-base sample
```

出力:
- `outputs/sample.mp3`

## 🧩 主なオプション
- `--text` / `--text-file`: 入力テキスト
- `--voice`: 音声名（例: `Zephyr`, `Kore`, `Aoede`）
- `--max-chars`: 分割閾値（推奨: `200-400`）
- `--output-dir`: 出力先フォルダ
- `--output-base`: 出力ファイル名ベース
- `--keep-temp`: 中間ファイル保持

## 🧪 検証
```bash
TARGET="outputs/sample.mp3"
ffprobe -v error -show_entries stream=codec_name -of default=nw=1:nk=1 "$TARGET"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$TARGET"
```
