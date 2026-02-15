---
name: marp-slide-creator
description: Marp形式の資料化依頼時に、referenceテンプレートを使ってスライド生成プロンプトを作成し、生成済みMarkdownを.mdへ保存するAgent Skill
---

# Majin Slide Skill

## Overview

このSkillは次の2機能を提供します。

1. `topic` を `references/prompt.md` に埋め込んでMarp向け生成プロンプトを作成
2. 生成済みMarkdownを `.md` ファイルとして保存

## Prerequisites

- `references/prompt.md` が存在すること

## Triggers

以下の依頼で利用します。

- 「スライド用プロンプトを作って」
- 「この内容をMarkdownファイルに保存して」
- 「Marp前提で資料化したい」

以下は対象外です。

- 既存Markdownの添削や要約のみを求める依頼
- Marp以外の形式（例: PowerPoint直接生成）のみを求める依頼

## Inputs

### Prompt generation

- `topic` (required): プレゼンのテーマ

### File creation

- `filename` (required): 出力ファイル名（拡張子省略可）
- `content` (required): 保存するMarkdown本文
- `output_dir` (optional, default `.`): 出力先ディレクトリ

## Workflow

### 1) Generate prompt from reference

- `references/prompt.md` を開く
- `{{TOPIC}}` をユーザー指定トピックに置換して提示する
- 参照ファイルの構造は維持し、不要な改変をしない

### 2) Save markdown slide file
- `filename` に `.md` がなければ補完する
- `output_dir` が存在しなければ作成する
- `output_dir/<filename>.md` へ `content` をUTF-8で保存する

## Error handling

- `content` が空の場合は保存しない
- 書き込み不可ディレクトリはエラーとして明示する
- `filename` に `.md` がなければ自動補完
- `filename` にパス区切り（`/`, `\`）や `..` が含まれる場合は例外で停止

## Validation loop

1. 生成後に、出力がMarp向け指示として成立しているか確認する
2. 保存後に、出力先に `.md` が作成され、先頭見出しと `---` 区切りを確認する
3. 問題があれば入力（`topic`、本文、ファイル名）を修正して再実行する

## Notes
- 出力内容の品質は入力トピックの具体性に依存
- 参照ファイルは `references/` 配下のみを利用する
