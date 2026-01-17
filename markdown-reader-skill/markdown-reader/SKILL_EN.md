---
name: markdown-reader
description: Read Markdown progressively by first getting an outline, then extracting specific sections. Use for any Markdown reading, not just large files.
---

# Read Markdown Progressively

## When to use
- When you want to grasp the heading structure first and extract only the needed sections
- Use this skill by default when reading Markdown

## Prerequisites
- `treemd` is installed
- The target Markdown file is local

## Basic steps (progressive reading)
1. Show the heading tree
   `treemd --tree path/to/doc.md`
2. Choose the exact heading you want to read
3. Extract the section
   `treemd --section "Heading Name" path/to/doc.md`

## Recommended flow
1. Start with top-level headings (H1/H2) using `--tree`
2. Read only the necessary sections with `--section`
3. If needed, further narrow down using smaller headings with `--section`

## Example
```
treemd --tree README.md
treemd --section "Installation" README.md
```

## Notes
- `--section` typically requires an exact heading match. Watch for spelling or formatting differences.
- If you cannot find the target heading, recheck the heading level or wording.

## Troubleshooting
- If you see `treemd: command not found`, run `cargo install treemd`
- If the output is not what you expect, verify the heading name again
