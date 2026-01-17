<h1 align="center">md-to-singlepage-pdf</h1>


<p align="center">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/node.js-18%2B-339933?logo=node.js&logoColor=white" alt="Node.js"/>
  <img src="https://img.shields.io/badge/npm-required-CB3837?logo=npm&logoColor=white" alt="npm"/>
  <img src="https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyMuPDF-required-2B579A" alt="PyMuPDF"/>
  <img src="https://img.shields.io/badge/md--to--pdf-required-000000" alt="md-to-pdf"/>
</p>

<p align="center">Agent Skill for converting Markdown (.md) into a single long-page PDF. This skill bundles instructions, scripts, and assets to run <code>md-to-pdf</code> and trim bottom whitespace with PyMuPDF.</p>

## ✨ Features

- Skill package: instructions + scripts + assets in one folder
- Produces a single long-page PDF without page breaks
- Unifies page size, margins, and style via CSS
- Automatically trims redundant bottom whitespace after conversion
- Supports batch conversion for multiple files

## 📎 Agent Skills

- Website: `https://agentskills.io/home`
- This repository follows the Agent Skills format (SKILL.md + scripts/assets/resources).

## 📦 Requirements

- Node.js / npm (for `md-to-pdf`)
- Python 3 (for PyMuPDF)
- `uv` is optional but speeds up venv creation and installs

## 📥 Installation

### 1) Install md-to-pdf (if missing)

```bash
npm install -g md-to-pdf
```

If `md-to-pdf` is missing, `scripts/convert_md_to_pdf.sh` will prompt you.

### 2) PyMuPDF

`convert_md_to_pdf.sh` automatically creates `.venv` and installs PyMuPDF.

### 3) Install the Agent Skill

Copy this repository into the Skills folder for Codex or Claude Code.

```bash
git clone https://github.com/Tomato13/md-to-singlepage-pdf.git
cd md-to-singlepage-pdf
cp -pr md-to-singlepage-pdf ~/.codex/skills
```

## 🚀 Usage

Give an instruction like this to Codex or Claude Code:

```text
Convert the Markdown file document.md into a single long-page PDF.
```

The output will be `document.pdf`.

## ⚙️ How it works

- `assets/pdf-style.css` sets a large page size
- `md-to-pdf` renders the PDF
- `scripts/crop_pdf.py` detects and trims bottom whitespace

## 🛠️ Customization

- Adjust page size and margins via `assets/pdf-style.css` `@page`
- Tune bottom padding with `margin_bottom` in `scripts/crop_pdf.py`

## ⚠️ Notes

- Very large images can leave unexpected whitespace
- `md-to-pdf` uses Chromium under the hood

## Acknowledgements

Thanks to @shown_it for publishing
[zenn: Convert a Markdown document to a PDF without page breaks](https://zenn.dev/lnest_knowledge/articles/91a1893b3f92f3).

## 📄 License

MIT License
