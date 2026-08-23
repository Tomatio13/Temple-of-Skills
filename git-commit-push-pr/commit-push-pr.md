---
allowed-tools: Bash(git checkout --branch:*), Bash(git switch --create:*), Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(git log:*), Bash(git push:*), Bash(git commit:*), Bash(gh auth status:*), Bash(gh pr list:*), Bash(gh pr create:*), Bash(gh pr view:*), Bash(gh pr edit:*)
description: Create logical commits, push a branch, and open a verified pull request
---

## Context

- Current git status: !`git status --short --branch`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task

Publish only the changes in the user's requested scope.

1. Inspect staged, unstaged, and untracked files, the current branch, the default branch, remotes, and any existing pull request for the current head branch.
2. If the current branch is `main` or `master`, create a descriptive branch before committing.
3. Plan commits by reason and reviewer value. Do not default to one commit.
   - Keep one behavior change with its tests and required documentation.
   - Split independent features, fixes, refactors, formatting, or dependency changes.
   - If a commit summary needs to join unrelated purposes with "and", split it.
   - Do not split only because files differ.
4. Stage explicit paths or hunks. Never use `git add -A`.
5. Before each commit:
   - Review `git diff --cached --stat` and `git diff --cached`.
   - Run relevant tests, formatting, lint, and `git diff --check`.
   - Do not ignore failures or include unrelated changes.
6. Create each commit with a concise English Conventional Commit message unless the user requests another language.
7. Review the complete branch diff and commit series, then push the branch to `origin` with an upstream. Do not force-push unless explicitly requested.
8. Create or update the pull request:
   - Reuse an existing pull request for the same head branch.
   - Write a real body from the complete branch diff and actual verification results.
   - Use a body file with `gh pr create --body-file` or `gh pr edit --body-file`.
   - Never submit an empty body or claim tests that were not run.

Use this body structure:

```markdown
## Summary

- <user-visible or maintainer-visible outcome>
- <why the change is needed>

## Changes

- <important implementation, test, and documentation changes>

## Verification

- `<command actually run>` — passed

## Notes

- <known limits, unverified areas, or "None">
```

9. Re-read the pull request with `gh pr view --json url,title,body,headRefName,baseRefName`.
   - Confirm the body is non-empty and contains `Summary`, `Changes`, `Verification`, and `Notes`.
   - Confirm the title, head, base, claims, and verification match the current branch.
   - If the body is missing or stale, repair it once with `gh pr edit --body-file` and re-read it.
   - If verification still fails, report the pull request URL and mismatch instead of claiming success.
10. Report the branch, pull request URL, commit hashes and subjects, verification results, pull request body verification, and any remaining changes or blockers.
