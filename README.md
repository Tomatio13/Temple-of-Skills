<h1 align="center">Temple-of-Skills</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

個人的に利用しているAgent Skillsを集めているリポジトリです。
各スキルはディレクトリ単位で管理され、`SKILL.md` を起点に手順・ルール・補助資料を参照します。

## 🎯 目的
- 再利用可能なスキル群を一元管理する
- 依頼内容に応じて適切な `SKILL.md` を読み、最小限の参照で作業する
- スキルごとの責務を明確にし、保守性を高める
- 各スキルは独自作成のものだけでなく、Codexなどが提供しているSkillも含む。

## 🧩 構成
- 各スキルは `<skill-name>/` 配下に配置
- 必須: `SKILL.md`
- 任意: `README.md`, `references/`, `scripts/`, `assets/`

## 📚 スキル一覧

### 💻 開発・コード
| スキル | 概要 | パス |
| --- | --- | --- |
| code-simplifier | 機能を変えずにコードを簡素化・整備 | `code-simplifier/` |

### 🔄 Git
| スキル | 概要 | パス |
| --- | --- | --- |
| git-commit-push-pr | コミット/プッシュ/PR作成の手順 | `git-commit-push-pr/` |
| git-main-switch-clean | mainへ戻し、ブランチ整理を補助 | `git-main-switch-clean/` |
| git-release-notes-generator | タグ差分からリリースノート生成 | `git-release-notes-generator/` |

### 📄 資料作成・ドキュメント
| スキル | 概要 | パス |
| --- | --- | --- |
| marp-layout-fix | Marpスライドのレイアウト崩れを検出・修正 | `marp-layout-fix/` |
| marp-slide-creator | Marp形式の資料化（プロンプト作成・Markdown保存） | `marp-slide-creator/` |
| marp-style-applier | Marpスライドデッキにプレゼンテーションデザインスタイルを適用 | `marp-style-applier/` |
| md-to-singlepage-pdf | Markdownを1枚の縦長PDFに変換し余白をトリム | `md-to-singlepage-pdf/` |
| pptx-basic-generator | basic_generator.pyを使ったPowerPoint生成・更新（12種類のテンプレート対応） | `pptx-basic-generator/` |
| svg-illustration | SVG図のルール、レイアウトパターン、埋め込みガイダンス | `svg-illustration/` |
| video-slide-skill | Marp動画スライドの作成フロー（動画対応化・ポータブル配布化） | `video-slide-skill/` |

### ✍️ 文章・レビュー
| スキル | 概要 | パス |
| --- | --- | --- |
| agent-skills-reviewer | Agent Skills の品質・実用性を評価し、SKILL.mdの改善点を指摘 | `agent-skills-reviewer/` |
| document-review | README/ドキュメントの品質レビュー | `document-review/` |
| note-check | 記事を緊張と弛緩の観点で添削し、炎上リスクを回避 | `note-check/` |
| sns-check | SNS投稿を「緊張と弛緩」の観点で添削し、炎上リスクを回避 | `sns-check/` |

### ⚙️ 運用・管理
| スキル | 概要 | パス |
| --- | --- | --- |
| agent-memory | 記憶の保存・想起・整理の依頼に対応 | `agent-memory/` |
| plan | 実行計画の作成・保存・更新・削除 | `plan/` |
| skill-creator | 新しいスキルの作成・更新ガイド | `skill-creator/` |

### 🔗 連携・通知
| スキル | 概要 | パス |
| --- | --- | --- |
| claude-daily-report | Claude Codeの会話履歴を分析し日報を作成 | `claude-daily-report/` |
| codex-daily-report | Codexの会話履歴を分析し日報を作成 | `codex-daily-report/` |
| discord-webhook-poster | Discord Webhookへテキストとマルチメディアファイルを一方向送信 | `discord-webhook-poster/` |

### 🎵 メディア・音声
| スキル | 概要 | パス |
| --- | --- | --- |
| gemini-tts-skill | Gemini TTSで日本語テキストをMP3化し、長文を自動分割して安定生成 | `gemini-tts-skill/` |
| voice-skill | 音声入力を即時実行 | `voice-skill/` |

### 💼 ビジネス
| スキル | 概要 | パス |
| --- | --- | --- |
| kpi-creator | KPI/CSFを決めるためのStep1-2を実行 | `kpi-creator/` |

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
- 基本はMITです
- ただし、他の方から提供されたSkillは提供元のライセンスに準拠します
