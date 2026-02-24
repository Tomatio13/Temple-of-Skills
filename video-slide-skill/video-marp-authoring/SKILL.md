---
name: video-marp-authoring
description: 非動画のMarp Markdownを動画背景対応のMarpへ新規変換する。スライドごとの動画割当をユーザーに列挙指定してもらい、video-pitch-deck準拠のスタイル（bg-video/layer/glass/grid等）を反映した `*-video.md` を生成するときに使う。
---

# Video Marp Authoring

## Overview

非動画Marpを、スライドごとに背景動画を持つMarpへ変換する。元ファイルは変更せず、新規ファイルを作成する。
LLMが `video-pitch-deck` テンプレートを基に構成を設計し、Pythonはその設計図を検証・レンダリングする。

## Workflow

1. ユーザーに変換元Marpファイルを指定してもらう。
2. LLMが入力Marpを読み、各スライドを `cover / intro / grid / quote / outro` のどれで組むか決める。
3. ユーザーにページごとの動画を列挙してもらい、LLMが blueprint JSON を作る。
4. `scripts/generate_video_marp.py --mode blueprint` を実行して `*-video.md` を新規生成する。
5. 出力ファイルを確認し、テンプレート再現（色調・グリッド・glass）と動画割当を検証する。

## Blueprint First

設計図JSONの仕様は `references/blueprint-schema.md` を参照する。
サンプルは `references/blueprint-sample.json` を参照する。

## Style Reuse

再利用スタイルは `references/video-pitch-deck-template.md` を基準とする。`marp/video-pitch-deck.md` をテンプレート化したもので、色調・ガラス表現・グリッド構成を再現できる。

- `--mode blueprint`: LLM設計図を適用してテンプレートレイアウトを組み立てる（推奨）
- `--mode preserve`: 元スライド構造を維持しつつ動画対応化（簡易互換）

## Command

```bash
python skills/video-marp-authoring/scripts/generate_video_marp.py \
  marp/input.md \
  marp/input-video.md \
  --mode blueprint \
  --blueprint-file skills/video-marp-authoring/references/blueprint-sample.json \
  --strict-count
```

互換モード（preserve）:

```bash
python skills/video-marp-authoring/scripts/generate_video_marp.py \
  marp/input.md \
  marp/input-video.md \
  --mode preserve \
  --map-file /tmp/video-map.txt
```
