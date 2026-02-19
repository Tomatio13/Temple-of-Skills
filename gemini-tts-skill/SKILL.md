---
name: gemini-tts-mp3
description: Gemini TTSで日本語テキストをMP3化し、長文を自動分割して安定生成したいときに使う。
---

# Gemini TTS MP3 Skill

## 前提
- APIキーは次の順で参照する
  1. `./.env`
  2. `scripts/../.env`（リポジトリ直下）
  3. 環境変数 `GEMINI_API_KEY`（最後のフォールバック）
- `node`（推奨: 18以上）と `curl` が利用可能
- `ffmpeg` がインストール済み

## クイックスタート
1. `.env` を作成する
```bash
cat > .env <<'EOF'
GEMINI_API_KEY=your-api-key
EOF
```

2. 一括実行でMP3を作る（長文は文単位で自動分割）
```bash
./scripts/tts_to_mp3.sh \
  --text "こんにちは。Gemini TTSの音声テストです。" \
  --voice Zephyr \
  --max-chars 300 \
  --output-dir outputs \
  --output-base sample
```

3. 出力を確認する
- `sample.mp3`

## 主要スクリプト
- `scripts/generate_tts.sh`
  - Gemini APIへリクエストして `response.json` を保存
- `scripts/decode_pcm_to_wav.js`
  - `inlineData.data` をPCMとしてデコードしWAV化
- `scripts/split_text_chunks.js`
  - 文単位でテキストを分割し、長文を複数チャンクにする
- `scripts/wav_to_mp3.sh`
  - `ffmpeg` でWAVをMP3へ変換
- `scripts/tts_to_mp3.sh`
  - 分割 -> TTS -> WAV結合 -> MP3変換を一括実行

## 推奨設定
- MP3品質: `-q:a 2`（LAME VBR、高音質と容量のバランスが良い）
- 音声モデル: `gemini-2.5-flash-preview-tts`
- 音声名の例: `Zephyr`, `Kore`, `Aoede`
- 分割文字数: `--max-chars 200-400`（初期値は`300`、破綻する場合は小さくする）

## 追加オプション
- `--output-dir`: 出力先フォルダを指定する（デフォルト: `.`）
- `--max-chars`: 長文分割の閾値を指定する（推奨: `200-400`）
- `--keep-temp`: 中間ファイル（JSON/WAV/チャンク）を保持する
- オプション利用例:
```bash
./scripts/tts_to_mp3.sh \
  --text "中間ファイルも保存します" \
  --output-dir outputs \
  --output-base debug \
  --max-chars 250 \
  --keep-temp
```

## 実行後検証（必須）
```bash
TARGET="outputs/sample.mp3"  # 実際の --output-dir/--output-base に合わせて変更
ffprobe -v error -show_entries stream=codec_name -of default=nw=1:nk=1 "$TARGET"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$TARGET"
```
- `codec_name` が `mp3`
- `duration` が 0 より大きいこと

## 運用メモ
- `gemini-2.5-flash-preview-tts` が失敗する場合は `--model` で切り替えて確認する
- 長文で不安定な場合は `--max-chars` を小さくして再実行する
- API失敗時は5秒待機して手動で最大3回まで再実行する
- APIキーはログ・画面共有・履歴に出さない（`GEMINI_API_KEY` を直接表示しない）
- `.env` は `GEMINI_API_KEY=...` 形式で記述する（行末コメントは付けない）

## トラブルシュート
- `GEMINI_API_KEY is not set.`
  - `./.env` または `scripts/../.env` に `GEMINI_API_KEY=...` があるか確認する
  - なければ環境変数 `GEMINI_API_KEY` を設定する
- `ffmpeg is required but not found in PATH.`
  - ffmpegをインストールしてPATHを通す
- `Audio data not found in response JSON.`
  - APIエラーやレスポンス形式変更を確認する
- `--max-chars must be a positive integer.`
  - 分割文字数を正の整数で指定する
