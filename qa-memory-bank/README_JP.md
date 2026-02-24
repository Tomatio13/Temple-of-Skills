<h1 align="center">qa-memory-bank</h1>

<p align="center">技術Q&Aをローカルに蓄積し、再利用するための軽量ナレッジベースです。</p>

<p align="center">
  <img src="https://img.shields.io/badge/bash-5%2B-121011?logo=gnu-bash" alt="bash"/>
  <img src="https://img.shields.io/badge/sqlite-3-003B57?logo=sqlite" alt="sqlite"/>
</p>

<p align="center">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

## 📦 概要

- `SKILL.md`: Agent向け運用指示
- `references/schema.sql`: テーブル/インデックス定義
- `scripts/*.sh`: 日常運用用CLIスクリプト

## 📁 パス運用（重要）

本プロジェクトは**相対パス前提**で運用します。

- `SKILL_ROOT` は `SKILL.md` があるディレクトリ
- 既定DBは `data/knowledge.db`（`SKILL_ROOT` 基準）
- `scripts/*.sh` は `SKILL_ROOT` で実行
- `knowledge.db` が複数ある場合の優先順位:
  1. ユーザー明示のDBパス
  2. `SKILL_ROOT/data/knowledge.db`
  3. それ以外は確認後に利用

## 🔧 インストール

前提:

- `bash`
- `sqlite3`

確認:

```bash
sqlite3 --version
```

未導入の場合は、OS標準のパッケージマネージャーで `sqlite3` を導入してください。

## 🚀 クイックスタート

実行前に `SKILL_ROOT` へ移動してください。

```bash
# 1) DB初期化
bash scripts/init_db.sh data/knowledge.db

# 2) LLMで要約とキーワードを作成
summary="LLMで生成した要約"
keywords="sqlite3,updated_at,keywords"

# 3) 1件追加
bash scripts/add_qa.sh data/knowledge.db "質問" "回答" "$summary" "$keywords"

# 4) 検索
bash scripts/search_qa.sh data/knowledge.db "キーワード"

# 5) 回答全文付きで検索
bash scripts/search_qa.sh data/knowledge.db "キーワード" --full
```

## 🛠️ 使い方

```bash
# 一覧表示（id確認）
bash scripts/list_qa.sh data/knowledge.db

# id指定で更新
bash scripts/update_qa.sh data/knowledge.db <id> "質問" "回答" "要約" "k1,k2,k3"

# id指定で削除（必ず list -> delete -> list で確認）
bash scripts/delete_qa.sh data/knowledge.db <id>
```

## 🧭 トラブルシュート

ヒットするはずなのに0件の場合:

```bash
pwd
ls -l data/knowledge.db
bash scripts/search_qa.sh data/knowledge.db "キーワード" --full
```

別の `knowledge.db` を参照している可能性が高いです。

## 📌 運用ルール

- 通常運用ではSQL手打ちを避け、`scripts/*.sh` を使う
- insert/update前に、LLMで `summary` と `keywords` を生成する
- 削除前後は `list_qa.sh` で `id` を確認する
- スキーマ変更時は `references/schema.sql` を更新する
