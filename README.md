<h1 align="center">Temple-of-Skills</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

Codex 用の Agent Skill を集約したリポジトリです。各スキルはディレクトリ単位で管理され、`SKILL.md` を起点に手順・ルール・補助資料を参照します。

## 🎯 目的
- 再利用可能なスキル群を一元管理する
- 依頼内容に応じて適切な `SKILL.md` を読み、最小限の参照で作業する
- スキルごとの責務を明確にし、保守性を高める

## 🧩 構成
- 各スキルは `<skill-name>/` 配下に配置
- 必須: `SKILL.md`
- 任意: `README.md`, `references/`, `scripts/`, `assets/`

## 📚 スキル一覧
| スキル | 概要 | パス |
| --- | --- | --- |
| agent-memory | 記憶の保存・想起・整理の依頼に対応 | `agent-memory/` |
| code-simplifier | 機能を変えずにコードを簡素化・整備 | `code-simplifier/` |
| document-review | README/ドキュメントの品質レビュー | `document-review/` |
| git-commit-push-pr | コミット/プッシュ/PR作成の手順 | `git-commit-push-pr/` |
| git-main-switch-clean | mainへ戻し、ブランチ整理を補助 | `git-main-switch-clean/` |
| git-release-notes-generator | タグ差分からリリースノート生成 | `git-release-notes-generator/` |
| plan | 実行計画の作成・保存・更新・削除 | `plan/` |

## ✅ 使い方（概要）
1. 依頼内容に合うスキルを選ぶ
2. 対象スキルの `SKILL.md` を読み、必要最小限の情報だけ参照
3. 指示に従って作業を実行

## 📦 インストール
- このリポジトリを配置し、各スキルの `SKILL.md` を参照できる状態にする

## 🧭 スキル追加の指針
- 新しいスキルは専用ディレクトリを作成
- `SKILL.md` に目的・適用条件・手順・制約を明記
- 補助資料やスクリプトは必要最小限に限定

## 🧾 ライセンス
MIT
