<h1 align="center">plan skill</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-blue" alt="python"/>
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

複雑な開発タスクの実行計画を作成・保存・更新・削除するための Codex スキルです。

## 概要

- 計画の作成（実装計画 / 概要計画）
- 計画ファイルの保存・読込・更新・削除
- `~/.codex/plans` 配下の計画ファイル管理

## 使い方

ユーザーが「計画を作って」「計画ファイルを保存/更新/削除して」などを依頼した場合に使用します。

主な出力は以下のいずれかです。

- チャット上に `# Plan` から始まる計画本文を提示（フロントマター無し）
- 必要に応じて計画を `~/.codex/plans` に保存

## ルール（要約）

- 既存リポジトリは読み取り専用。計画の保存先は `~/.codex/plans` のみ。
- ファイル保存時は YAML フロントマターに `name` と `description` のみを含める。
- 計画名は短く、`lower-case` と `-` で区切る（例: `my-plan-name`）。
- 参照のみの「概要計画」も許可。

## スクリプト

`./scripts` に以下のヘルパーがあります。

- `list_plans.py`: 既存計画の一覧表示
- `read_plan_frontmatter.py`: フロントマター検証
- `create_plan.py`: 計画ファイル作成

## テンプレート

計画本文は `# Plan` から開始し、以下のテンプレートのいずれかを使用します。

- Implementation plan body template
- Overview plan body template

詳細は `SKILL.md` を参照してください。
