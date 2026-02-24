<h1 align="center">qa-memory-bank</h1>

<p align="center">A lightweight local knowledge base for storing and reusing technical Q&A.</p>

<p align="center">
  <img src="https://img.shields.io/badge/bash-5%2B-121011?logo=gnu-bash" alt="bash"/>
  <img src="https://img.shields.io/badge/sqlite-3-003B57?logo=sqlite" alt="sqlite"/>
</p>

<p align="center">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

## 📦 Overview

- `SKILL.md`: Agent-oriented operating instructions
- `references/schema.sql`: Table and index definitions
- `scripts/*.sh`: CLI utilities for daily operations

## 📁 Path Convention (Important)

This project is intended to be used with **relative paths**.

- Define `SKILL_ROOT` as the directory containing `SKILL.md`
- Default DB path: `data/knowledge.db` (relative to `SKILL_ROOT`)
- Run `scripts/*.sh` from `SKILL_ROOT`
- If multiple `knowledge.db` files exist, prefer:
  1. user-specified DB path
  2. `SKILL_ROOT/data/knowledge.db`
  3. other DBs only after confirmation

## 🔧 Installation

Requirements:

- `bash`
- `sqlite3`

Check:

```bash
sqlite3 --version
```

Install `sqlite3` with your OS package manager if missing.

## 🚀 Quick Start

Before running commands, move to `SKILL_ROOT`.

```bash
# 1) Initialize DB
bash scripts/init_db.sh data/knowledge.db

# 2) Generate summary + keywords with LLM
summary="Technical summary from LLM"
keywords="sqlite3,updated_at,keywords"

# 3) Add one Q&A
bash scripts/add_qa.sh data/knowledge.db "Question" "Answer" "$summary" "$keywords"

# 4) Search
bash scripts/search_qa.sh data/knowledge.db "keyword"

# 5) Search with full answer
bash scripts/search_qa.sh data/knowledge.db "keyword" --full
```

## 🛠️ Usage

```bash
# List entries (check id)
bash scripts/list_qa.sh data/knowledge.db

# Update by id
bash scripts/update_qa.sh data/knowledge.db <id> "Question" "Answer" "Summary" "k1,k2,k3"

# Delete by id (always run list -> delete -> list)
bash scripts/delete_qa.sh data/knowledge.db <id>
```

## 🧭 Troubleshooting

If you expect matches but get 0 results:

```bash
pwd
ls -l data/knowledge.db
bash scripts/search_qa.sh data/knowledge.db "keyword" --full
```

This usually means you are pointing to a different `knowledge.db`.

## 📌 Rules

- Do not run handwritten SQL for normal operations; use `scripts/*.sh`
- Generate both `summary` and `keywords` with LLM before insert/update
- Always verify `id` with `list_qa.sh` before and after deletion
- Update `references/schema.sql` when schema changes
