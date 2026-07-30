# gh-stars-activity

GitHubのスター付きリポジトリの更新状況を、JST日時・リポジトリ名・更新概要（日本語）で一覧表示するClaude Code Agent Skillです。

## 必要要件

- [gh (GitHub CLI)](https://cli.github.com/) がインストール済み
- `gh auth login` で認証済み

## 使い方

Claude Code上で `/gh-stars-activity` を実行すると、直近2日間に更新のあったスター付きリポジトリの一覧を日本語概要付きで表示します。

### スクリプト単体での実行

```bash
# デフォルト（2日前〜現在）
bash scripts/stars_activity.sh

# 指定日以降
bash scripts/stars_activity.sh 2026-05-20

# リリースがあったリポジトリのみ（出力を絞る場合）
bash scripts/stars_activity.sh --releases-only

# JSON形式で出力
bash scripts/stars_activity.sh --json

# 件数制限（API呼び出しを抑える場合）
bash scripts/stars_activity.sh --limit=20

# 組み合わせ
bash scripts/stars_activity.sh 2026-05-20 --releases-only --json --limit=30
```

### 出力例

```
2026/05/28 06:04  google-gemini/gemini-cli [v0.45.0-preview.0]
  - fix(cli): ignore unmapped vim normal keys (#27102)
  - fix(core): prevent blacklist bypass in mcp list (#27377)
  - fix(core): suppress PTY resize EBADF errors (#27461)

2026/05/28 05:22  Mintplex-Labs/anything-llm [v1.13.0]
  - feat: add Cerebras as an LLM provider (#5699)
  - docs: list all cloud embedding providers (#5701)
  - v1.13.0 release (#5693)
```

## ファイル構成

```
gh-stars-activity/
├── SKILL.md                   # エージェント用メタデータ + 指示
├── README.md                  # このファイル
└── scripts/
    └── stars_activity.sh      # メインスクリプト
```

## ライセンス

MIT
