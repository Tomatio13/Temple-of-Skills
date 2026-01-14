---
name: git-main-switch-clean
description: 現在のGitリポジトリをmainブランチに切り替え、最新のmainをpullし、直前のブランチを削除するかどうかを確認して処理する。mainへ戻して古いローカルブランチを整理したいときに使用する。ブランチ削除は必ず事前にユーザーへ確認する。
---

# Git Main Switch Clean

## Overview

Switch to `main` when the current branch is not `main`, pull latest changes, then ask the user for confirmation before deleting the previous branch.

## Workflow

### 1) Inspect current state

Run:
```bash
git branch --show-current
git status -s
```

If already on `main`, report no changes needed and stop.

If there are uncommitted changes, ask the user whether to:
- commit,
- stash,
- or abort.
Do not switch branches until the user chooses.

### 2) Switch to main

Run:
```bash
git switch main
```

If `main` does not exist, stop and ask the user how to proceed (e.g., use `master` or another default branch).

### 3) Pull latest main

Run:
```bash
git pull --ff-only
```

If the pull fails (e.g., local changes or divergence), stop and ask the user how to proceed.

### 4) Confirm deletion of the previous branch

Ask explicitly before deletion:
> "Delete the previous branch `<branch>` now? (y/n)"

Only delete after the user confirms.

### 5) Delete the previous branch (after confirmation)

Run a safe delete first:
```bash
git branch -d <previous-branch>
```

If it fails due to unmerged commits, ask the user whether to force-delete:
```bash
git branch -D <previous-branch>
```

Do not force-delete unless the user explicitly confirms.
