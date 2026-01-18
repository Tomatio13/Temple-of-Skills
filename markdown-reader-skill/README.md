<h1 align="center">markdown-reader</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

<p align="center">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

An Agent Skill for progressively reading Markdown. Get the outline first, then extract only the sections you need.

## ✅ What it does
- 🧭 Get a heading outline
- ✂️ Extract only the needed sections
- 🧩 Read step by step for better understanding

## 📥 Expected input
- README.md
- Markdown specs or guides

## 📤 Output (summary)
- Heading outline
- Extracted section content

## 💡 Example prompts
After setting up the skill in your agent, use prompts like:

- "Read this Markdown with markdown-reader"
- "Show the outline first, then read this section"

You can load it incrementally like this:

![screenshot](./assets/screen.png)

## 📦 Prerequisite - Python 3
Python 3 is required. This skill ships with a lightweight treemd-compatible script.
Use the script from the skill's `scripts/` directory.

## 📦 Install this skill
```
git clone https://github.com/Tomatio13/markdown-reader-skill.git
cd markdown-reader-skill
cp -pr markdown-reader ~/.codex/skills
```

Copy it into your agent's skill directory.

## ⚠️ Notes
- `--section` requires an exact heading match
- If a heading is not found, check spelling and hierarchy

## 🗂️ Files
- `markdown-reader/SKILL.md`
- `markdown-reader/scripts/md-index.py`
- `markdown-reader/references/md-index.md`

## Acknowledgements
- Inspired by [treemd](https://github.com/Epistates/treemd.git) for compatible CLI behavior.
