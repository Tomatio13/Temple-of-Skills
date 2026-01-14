<h1 align="center">git-release-notes-generator</h1>

<p align="center">
  <img src="https://img.shields.io/badge/git-tool-blue" alt="git"/>
  <img src="https://img.shields.io/badge/bash-compatible-green" alt="bash"/>
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

Gitタグ間のコミット履歴とコード差分から、カテゴリ別・統計付きのリリースノートを作成する Agent Skill です。
Issue番号抽出、差分の詳細補足、重要度順の並び替えまで行います。

## 📦 インストール
- このリポジトリの `SKILL.md` を Codex の skills ディレクトリに配置
- Git が利用可能な環境で実行

## ✅ できること
- 指定タグ間のコミット/差分/統計の収集
- Issue番号（#数字）の抽出
- 変更内容のカテゴリ分類（新機能/バグ修正/性能/ドキュメント/設定/その他）
- 重要度順の整理
- 統計付きリリースノートの生成

## 🧩 想定入力
- Gitリポジトリ
- 前回タグ / 現在タグ

## ▶️ 使い方
1. 対象リポジトリへ移動
2. 前回タグと現在タグを指定して依頼

## 🛠️ 必要コマンド（抜粋）
```bash
# コミット取得
git log [前回のタグ]..[現在のタグ] --pretty=format:"%h %s"

# 差分取得
git diff [前回のタグ] [現在のタグ] --name-status
git diff [前回のタグ] [現在のタグ]

# 統計
コミット数: git log [前回のタグ]..[現在のタグ] --oneline | wc -l
貢献者数: git log [前回のタグ]..[現在のタグ] --format="%an" | sort -u | wc -l
変更ファイル数: git diff --name-only [前回のタグ] [現在のタグ] | wc -l
```

## 📤 出力形式（概要）
- タグ名と日付
- カテゴリ別の変更点
- 統計（コミット数/貢献者数/変更ファイル数/追加削除行数）

## 🧾 出力例（短縮）
```
## Release Notes: v1.2.0 -> v1.3.0
- ✨ 新機能: xxx (#123)
- 🐛 修正: yyy (#124)

### 統計
- コミット数: 12
- 貢献者数: 3
- 変更ファイル数: 18
- 追加/削除行数: +420 / -210
```

## 🧪 使い方例
- 「v1.2.0 と v1.3.0 のリリースノートを作って」
- 「前回タグ v2.1.0、現在タグ v2.2.0 でまとめて」

## ⚠️ 注意
- Issue番号が見つからない場合は「確認が必要」と明記します。
- 破壊的変更や重要変更は強調します。

## 謝辞
- [Github](https://github.com/Sunwood-ai-labs/MysticLibrary/tree/main/prompts/coding)
