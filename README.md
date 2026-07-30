<h1 align="center">Temple-of-Skills</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/skills-40-lightgrey" alt="40 skills"/>
</p>

個人的に利用・管理している Agent Skills を集約したリポジトリです。  
各スキルはディレクトリ単位で管理され、`SKILL.md` を入口に `README.md`、`references/`、`scripts/`、`assets/` などを必要最小限だけ参照する構成を採用しています。

## 🎯 目的

- 再利用可能なスキルを一元管理する
- スキルごとの責務と適用条件を明確にする
- 指示、補助資料、補助スクリプトを同じディレクトリに閉じ込めて保守性を上げる
- 自作スキルと外部由来スキルを同じ運用ルールで扱う

## 🧩 リポジトリ構成

- 各スキルは `<skill-name>/` 配下に配置
- 必須ファイルは `SKILL.md`
- 任意で `README.md`、`README_EN.md`、`references/`、`scripts/`、`assets/`、`agents/` を持つ
- 一部スキルは補助ツールやテンプレートを同梱する

## 🚀 使い方

1. 依頼内容に合うスキルディレクトリを選ぶ
2. 対象スキルの `SKILL.md` を最初に読む
3. `SKILL.md` から参照される補助資料やスクリプトだけを追加で読む
4. 指示に従って作業し、必要なら README や scripts で補完する

## 📚 スキル一覧

現在、トップレベルで `SKILL.md` を持つスキルは 40 個あります。

### 💻 開発・コード

- `apple-design/`: Apple 流の Web UI デザイン、物理モーション、スプリングアニメーション設計指針を提供する
- `code-simplifier/`: 機能を保ったままコードを簡素化し、可読性と保守性を上げる
- `commit/`: 実装後のセルフレビュー、コミット分割、Conventional Commit 作成を支援する
- `plan-code/`: 実装前にコード変更計画を作り、スコープとリスクを整理する
- `plan-bugfix/`: 不具合修正前に再現条件、原因候補、修正方針、テスト計画を整理する
- `pr-feedback/`: PR コメントを分類し、対応方針と返信文案をまとめる
- `skill-creator/`: 新規スキル作成、既存スキル改善、評価ループの進め方を提供する
- `empirical-prompt-tuning/`: プロンプトやスキル指示を実験的に評価し、反復改善する

### 🔄 Git・リリース

- `gh-stars-activity/`: GitHub CLI を使いスター付きリポジトリの指定日以降の更新・リリースを日本語で確認する
- `git-commit-push-pr/`: コミット、プッシュ、PR 作成フローを扱う
- `git-main-switch-clean/`: `main` へ戻し、ローカルブランチ整理を補助する
- `git-release-notes-generator/`: タグ差分からリリースノートを生成する

### 📄 資料・ドキュメント作成

- `document-review/`: README や各種ドキュメントの品質レビューを行う
- `html-output/`: 会話内容や構造化データを視覚的に見やすいローカル HTML ページとして出力する
- `marp-layout-fix/`: Marp スライドの見切れやレイアウト崩れを検出・修正する
- `marp-slide-creator/`: Marp 形式の資料作成を支援する
- `marp-style-applier/`: Marp スライドへデザインスタイルを適用する
- `markdown-reader-skill/`: Markdown の見出し構造把握や部分抽出を効率化する
- `md-to-singlepage-pdf/`: Markdown を縦長 1 ページ PDF に変換し、余白を調整する
- `pptx-basic-generator/`: `basic_generator.py` を使った PowerPoint 生成・更新を支援する
- `svg-illustration/`: SVG 図の作り方、パターン、埋め込み方針をまとめる
- `video-slide-skill/`: 動画化を前提にした Marp スライド制作フローを提供する

### ✍️ 文章・レビュー

- `agent-skills-reviewer/`: Agent Skills の品質、実用性、改善余地をレビューする
- `humanizer-ja/`: AI らしさの強い日本語を人間らしい文章へ書き換える
- `note-check/`: note 記事を「緊張と弛緩」の観点で添削する
- `sns-check/`: SNS 投稿を「緊張と弛緩」の観点で添削する

### ⚙️ 運用・知識管理

- `agent-memory/`: 記憶の保存、検索、整理を行う
- `current-time/`: 現在時刻取得や日時フォーマットを行う
- `handoff/`: 長期化したセッションから文脈や未解決タスクを引き継いだ新セッションへの移行を作成する
- `plan/`: 実行計画の作成、更新、保存、削除を扱う
- `qa-memory-bank/`: 技術 Q&A や知識を蓄積・検索・更新する
- `session-analyzer/`: Claude Code や Codex のセッションログを分析する

### 🔗 レポート・通知

- `claude-daily-report/`: Claude Code の会話履歴から日報を作成する
- `codex-daily-report/`: Codex の会話履歴から日報を作成する
- `discord-webhook-poster/`: Discord Webhook にテキストや添付ファイルを送信する

### 🌐 外部サービス・リサーチ

- `google/`: `gogcli` を使って Gmail、Calendar、Drive、Docs、Sheets、Slides を操作・連携する
- `openweather/`: OpenWeather API で現在天気や予報を取得する
- `rakuten-travel-skill/`: 楽天トラベルを前提に空室や宿泊プランを検索する
- `x-research/`: SocialData API を使って X の投稿や記事を調査し、レポート化する
- `x-search-skill/`: ローカルの `x-search` CLI を使い X の投稿検索や Grok による要約・根拠 URL を取得する

### 🎵 音声・メディア

- `gemini-tts-skill/`: Gemini TTS で日本語テキストを MP3 化する
- `voice-skill/`: 音声入力の実行フローを扱う

### 💼 ビジネス

- `kpi-creator/`: CSF と KPI の整理、目標設定の初期設計を支援する

## 🧭 スキル追加の指針

- 新しいスキルは専用ディレクトリを作る
- `SKILL.md` に目的、適用条件、手順、制約を書く
- 追加資料は `references/`、補助コードは `scripts/` に分離する
- README は概要とセットアップだけに寄せ、運用ルールは `SKILL.md` に寄せる

## 🧾 ライセンス

- ルートのライセンスは `LICENSE` を参照
- 外部由来のスキルや同梱物がある場合は、それぞれの配布条件を優先する
