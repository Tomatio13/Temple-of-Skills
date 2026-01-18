---
name: markdown-reader
description: Read Markdown progressively by first getting an outline, then extracting specific sections. Use for any Markdown reading, not just large files.
compatibility: Requires Python 3. Runs scripts from the skill's scripts/ directory.
---

# Read Markdown Progressively

## When to use
- When you want to grasp the heading structure first and extract only the needed sections
- Use this skill by default when reading Markdown

## Prerequisites
- Python 3 is available
- Use `scripts/md-index.py`
- The target Markdown file is local

## Basic steps (progressive reading)
1. Show the heading tree
   `python3 scripts/md-index.py --tree path/to/doc.md`
2. Choose the exact heading you want to read
3. Extract the section
   `python3 scripts/md-index.py --section "Heading Name" path/to/doc.md`

## Recommended flow
1. Start with top-level headings (H1/H2) using `--tree`
2. Read only the necessary sections with `--section`
3. If needed, further narrow down using smaller headings with `--section`

## Example
```
python3 scripts/md-index.py --tree README.md
python3 scripts/md-index.py --section "Installation" README.md
```

## Notes
- `--section` typically requires an exact heading match. Watch for spelling or formatting differences.
- If you cannot find the target heading, recheck the heading level or wording.

## Troubleshooting
- If you see `python3: command not found`, install Python 3
- If you see `No input provided`, pass a Markdown file or pipe stdin
- If the output is not what you expect, verify the heading name again
