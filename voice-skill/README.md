<h1 align="center">voice-skill</h1>
<p align="center">Agent Skill for recording from microphone and transcribing with whisper.cpp.</p>
<p align="center">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/python-3.x-blue.svg" alt="python">
  <img src="https://img.shields.io/badge/ffmpeg-required-brightgreen.svg" alt="ffmpeg">
  <img src="https://img.shields.io/badge/whisper.cpp-required-orange.svg" alt="whisper.cpp">
</p>

## ✅ Requirements

- Python 3
- Recording tool: `arecord` (ALSA) or `ffmpeg`
- whisper.cpp CLI binary (`whisper-cli`)

## ⚙️ How it works

1. Record audio locally with `arecord` or `ffmpeg`.
2. Transcribe with whisper.cpp CLI.
3. Show the transcription to the user and ask for confirmation to run it.
4. If yes, pass the text to the LLM as the prompt to execute.

## 🚀 Usage

Copy this skill into your Claude Code or Codex Skills folder, then run the
`voice` command. You will be asked whether to execute the transcribed text;
answer `yes` or `no`.

Screenshot (JP UI):

![screen](./assets/screen_jp.png)

## 🔧 Environment variables

This skill relies on external commands for recording and transcription.

### Recording

You need `ffmpeg` or `arecord`. Configure these variables:

- `VOICE_RECORDER`: Force `arecord` or `ffmpeg`.
- `VOICE_SECONDS`: Default recording seconds if no CLI arg is given.
- `VOICE_SILENCE_SECONDS`: If > 0, stop on silence (ffmpeg only).
- `VOICE_SILENCE_NOISE`: Silence threshold for ffmpeg. Default: `-40dB`.

### Transcription

You need whisper.cpp. Configure these variables:

- `WHISPER_BIN` or `WHISPER_CPP`: Path to whisper.cpp CLI binary.
- `WHISPER_CMD`: Full command template. Use `{bin}`, `{model}`, `{audio}`, `{out}`.
- `WHISPER_MODEL_DIR`: Directory to store models.
- `WHISPER_MODEL`: Model filename. Default: `ggml-base.bin`.
- `WHISPER_ARGS`: Extra args appended to the default whisper command.

### .env example

Create a file like the following and place it under `scripts/`.

```env
# whisper.cpp CLI binary (required: full path to the executable)
WHISPER_BIN=/path/to/whisper.cpp/build/bin/whisper-cli
WHISPER_CMD="{bin} -m {model} -f {audio} -l ja -otxt -of {out}"
# Model settings (default: ggml-base.bin)
WHISPER_MODEL=ggml-small.bin
WHISPER_MODEL_DIR=~/whisper_models
# Recording settings
VOICE_RECORDER=ffmpeg
VOICE_SECONDS=20
# Auto-stop on silence (ffmpeg only)
VOICE_SILENCE_SECONDS=2
VOICE_SILENCE_NOISE=-40dB
```

- `WHISPER_BIN` must be the executable path, not a directory.
- If the model is missing, it is auto-downloaded into `WHISPER_MODEL_DIR`.
- Using `ffmpeg` enables auto-stop on silence.

## 🧰 Install (minimal)

Install or build the dependencies, then point `WHISPER_BIN` to the whisper.cpp
binary and ensure `ffmpeg` or `arecord` is available on your PATH.

## 📝 Notes

- WAV/TXT are created under a temporary directory and deleted automatically
  when the script finishes.

## 🔗 References

- whisper.cpp: https://github.com/ggml-org/whisper.cpp
- ffmpeg: https://ffmpeg.org
