---
name: qa-memory-bank
description: ユーザーが「技術Q&Aやナレッジを蓄積・検索・更新したい」と依頼したときに使う。
---

# QA Memory Bank Skill

`sqlite3` CLI で、技術ナレッジの保存・検索・更新・削除を行うスキルです。  
SQL 手打ちは禁止し、`scripts/*.sh` のみ使います。

## 使うタイミング

- 「調べた内容を後で再利用できる形で残したい」

## 前提条件

- `bash` が利用可能であること
- `sqlite3` がインストール済みであること（`sqlite3 --version`）
- DB ファイルを書き込めるディレクトリ権限があること

## パス運用ルール（重要）

- 本スキルは**相対パス前提**で運用する。
- `SKILL_ROOT` を「この `SKILL.md` があるディレクトリ」と定義する。
- 既定DBは `SKILL_ROOT/data/knowledge.db`。
- `scripts/*.sh` は `SKILL_ROOT` 直下で実行する。
- `./data/knowledge.db` の `./` は `SKILL_ROOT` 基準を意味する。

## Agent MUST手順

1. まず `SKILL_ROOT` を基準に実行していることを確認する（`pwd` と `ls data/knowledge.db`）。
2. 初回またはDB未作成時のみ `scripts/init_db.sh` を実行する。
3. 追加前に、`answer` からLLMで `summary` と `keywords`（カンマ区切り）を作る。
4. 追加は `scripts/add_qa.sh` を使い、`question` / `answer` / `summary` / `keywords` を必ず埋める。
5. `keywords` は検索キーになる固有語（ライブラリ名、設定名、エラー名）を優先する。
6. 検索は `scripts/search_qa.sh` を使い、必要時のみ `--full` を付ける。
7. 更新前に `scripts/list_qa.sh` で `id` を確認し、更新は `scripts/update_qa.sh` を使う。
8. 更新時も `answer` を再要約し、`summary` と `keywords` を更新する。
9. 削除は必ず `list -> delete -> list` の順で実行する。
10. 失敗時は「失敗時の対処」に従い、同じ失敗を繰り返さない。

## 要約ルール（summary）

- 文字数目安: 80〜160文字
- 目的: 「後で検索しやすい技術要点」を残す
- MUST:
  - 原因/対処/前提のうち少なくとも1つを含める
  - 重要な固有語（例: `sqlite3`, `updated_at`, `--full`）を含める
  - 主観表現（「便利」「いい感じ」など）を避ける
- 推奨プロンプト:

```text
次の回答を、技術ナレッジDBのsummary用に日本語で要約してください。
要件:
- 80〜160文字
- 検索キーになる固有語を含める
- 原因/対処/前提のいずれかを含める
- 曖昧表現を避ける
回答:
{answer}
```

## キーワードルール（keywords）

- 形式: `keyword1,keyword2,keyword3`（半角カンマ区切り）
- 個数目安: 3〜8個
- MUST:
  - 固有語を優先（例: `sqlite3`, `updated_at`, `--full`, `PRAGMA table_info`）
  - 抽象語のみ（例: `改善`, `対応`）を避ける
  - 重複を避ける
- 推奨プロンプト:

```text
次の回答から、検索に有効な技術キーワードを3〜8個抽出してください。
出力は半角カンマ区切り1行のみ。固有語を優先し、重複は避けてください。
回答:
{answer}
```

## スクリプト仕様

- `scripts/init_db.sh <db_path>`  
  役割: テーブルとインデックスを作成する。  
  失敗条件: 引数不足、DBパスに書き込み不可。
- `scripts/add_qa.sh <db_path> <question> <answer> <summary> <keywords_csv>`  
  役割: Q&Aを1件追加する。  
  失敗条件: 引数不足、DB未初期化、DBパス不正。
- `scripts/search_qa.sh <db_path> <keyword> [--full]`  
  役割: `question/answer/summary` を横断検索する。  
  失敗条件: 引数不足、`--full` 以外の第3引数。
- `scripts/list_qa.sh <db_path>`  
  役割: `id` を含む一覧を表示する。  
  失敗条件: 引数不足、DBパス不正。
- `scripts/update_qa.sh <db_path> <id> <question> <answer> <summary> <keywords_csv>`  
  役割: 指定 `id` の内容を更新し、`updated_at` を更新する。  
  失敗条件: `id` が整数でない、対象 `id` が存在しない。
- `scripts/delete_qa.sh <db_path> <id>`  
  役割: 指定 `id` を削除する。  
  失敗条件: `id` が整数でない、対象 `id` が存在しない。

## 実行例

前提: 先に `SKILL_ROOT`（この `SKILL.md` があるディレクトリ）へ移動して実行する。

1. 初期化  
`bash scripts/init_db.sh data/knowledge.db`
2. 要約とキーワードを作る（LLM）  
`summary="LLMで生成した要約"`  
`keywords="sqlite3,updated_at,--full"`
3. 追加  
`bash scripts/add_qa.sh data/knowledge.db "質問" "回答" "$summary" "$keywords"`
4. 検索  
`bash scripts/search_qa.sh data/knowledge.db "キーワード"`
5. 回答全文付きで検索  
`bash scripts/search_qa.sh data/knowledge.db "キーワード" --full`
6. 更新  
`bash scripts/list_qa.sh data/knowledge.db`  
`updated_summary="LLMで再生成した要約"`  
`updated_keywords="sqlite3,keywords,summary"`  
`bash scripts/update_qa.sh data/knowledge.db 1 "質問(更新)" "回答(更新)" "$updated_summary" "$updated_keywords"`
7. 削除  
`bash scripts/list_qa.sh data/knowledge.db`  
`bash scripts/delete_qa.sh data/knowledge.db 1`  
`bash scripts/list_qa.sh data/knowledge.db`

## 複数DBがある場合の優先順位

1. ユーザーが明示したDBパス
2. `SKILL_ROOT/data/knowledge.db`（既定）
3. それ以外の同名DB（利用前に必ずユーザー確認）

## テーブル定義

スキーマは `references/schema.sql` を参照。  
主テーブルは `qa_entries` で、最低限以下の列を持ちます。

- `id`
- `created_at`
- `updated_at`
- `question`
- `answer`
- `summary`
- `keywords`

## 失敗時の対処

- `sqlite3: command not found`  
  `sqlite3` をインストールして再実行する
- `unable to open database file`  
  DB パスの親ディレクトリを作成する
- 文字列に `'` が含まれて登録失敗  
  スクリプト経由で登録し、SQL 手打ちを避ける
- `Updated 0 rows` が出る  
  対象 `id` が存在するか `scripts/search_qa.sh` で確認する
- `Deleted 0 rows` が出る  
  対象 `id` が存在するか `scripts/list_qa.sh` で確認する
- ヒットするはずのQ&Aが0件になる  
  `SKILL_ROOT` 以外の `knowledge.db` を参照している可能性がある。`pwd` と `ls data/knowledge.db` を確認し、`data/knowledge.db` を明示して再検索する
