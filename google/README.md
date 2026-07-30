# Google Workspace Skill

Google Workspace integration using the `gog` CLI.

## 📌 概要 (Overview)
このスキルは、`gog` CLI (`gogcli`) を用いて Google Workspace (Gmail, Calendar, Drive, Docs, Sheets, Slides) を操作・連携するための AI エージェント向けスキルです。

## 👥 著者と公開元 (Credits)
このスキルは、以下の著者および GitHub リポジトリで公開されています。
- **著者 (Author):** [odyssey4me](https://github.com/odyssey4me)
- **公開元 (Repository):** [odyssey4me/agent-skills](https://github.com/odyssey4me/agent-skills)

## ⚙️ セットアップ & 認証 (Setup & Authentication)
前提条件となる `gog` CLI のインストールや Google Cloud Console での認証手順については、詳細なガイドが [SKILL.md](SKILL.md) に記載されています。そちらを参照してセットアップを行ってください。

主な流れ:
1. `gog` CLI のインストール (Homebrew またはバイナリ直接ダウンロード)
2. `credentials.json` の設定 (`gog auth credentials set ...`)
3. サービス連携 of 認証 (`gog auth add ...`)
4. 接続確認 (`gog auth doctor`)

## 📖 使い方 (Usage)
詳細な運用ルールやコマンド一覧については、同じディレクトリ内の以下のドキュメントを参照してください。

- **コア指示書 (Main Guide):** [SKILL.md](SKILL.md)
- **参照資料 (References):**
  - [認証・セットアップ詳細](references/configuration.md)
  - [権限一覧](references/permissions.md)
  - [Gmail コマンド詳細](references/gmail.md)
  - [Calendar コマンド詳細](references/calendar.md)
  - [Drive コマンド詳細](references/drive.md)
  - [Docs コマンド詳細](references/docs.md)
  - [Docs 高度なワークフロー](references/docs-workflows.md)
  - [Sheets コマンド詳細](references/sheets.md)
  - [Slides コマンド詳細](references/slides.md)
