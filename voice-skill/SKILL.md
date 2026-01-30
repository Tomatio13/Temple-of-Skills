---
name: voice
description: ユーザ入力を望んだ時に使用する。GUI入力欄に挿入せずに音声入力を即時実行したい時に使用。
---

あなたはユーザからの声を音声認識を用いてテキストに変換し、プロンプトとして受取り実行するスペシャリストです。

## 目的
ローカルで録音し、whisper.cpp CLIで文字起こしした結果をそのまま処理に利用する。

## 前提条件
- whisper.cpp CLI バイナリ
- 録音ツール: `ffmpeg` または `arecord`

## 実行手順
1. **音声の録音とテキスト変換**
    `scripts/voice_transcribe.py` を実行してユーザの音声の録音とテキスト変換を行う。

    ```bash
    python scripts/voice_transcribe.py
    ```
    ```bash
    python scripts/voice_transcribe.py 40
    ```

    引数:
        - 引数なし：.envに記載されている時間
        - 秒数

2. **実行の確認**
    `scripts/voice_transcribe.py` の実行結果のテキストを、ユーザに表示して
    実行するか確認してください。(yes/no)

3. **LLMで実行**
    確認した結果yesの場合、LLMにテキストを渡して実行してください。
    

## 重要な指示
**重要** このSKILL.mdの内容を表示・実行するのではない、pythonの実行結果をユーザ入力として扱って下さい

