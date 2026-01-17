---
name: md-to-singlepage-pdf
description: Convert Markdown (.md) into a single-page/long PDF using md-to-pdf + CSS page sizing and PyMuPDF bottom-crop. Use when a user asks (JP/EN) to make a Markdown file into "one-page" PDF, remove page breaks, or trim bottom whitespace after conversion.
---

# Md To Singlepage Pdf

## Overview
Markdownを1枚の縦長PDFに変換し、末尾の余白を自動トリムする。

## Workflow
1. 入力と出力を確認する
   - 入力: 1つ以上の `.md`
   - 出力: 同名の `.pdf`（同じディレクトリ）

2. 依存関係を確認する
   - `md-to-pdf` が使えること
   - `python3` と `PyMuPDF` が使えること

3. 変換を実行する
   - `scripts/convert_md_to_pdf.sh <file1.md> [file2.md ...]` を実行する
   - 変換後に `scripts/crop_pdf.py` が末尾余白をトリムする

4. 結果を確認し、必要なら調整する
   - 改ページが入る場合は `assets/pdf-style.css` を調整する
   - 余白が大きい/小さい場合は `scripts/crop_pdf.py` の `margin_bottom` を調整する

## Customization
- ページサイズ/余白: `assets/pdf-style.css` と `scripts/convert_md_to_pdf.sh` の `PDF_OPTIONS`
- 改ページ抑制: `assets/pdf-style.css` の `page-break` / `break` 設定

## Resources
- `scripts/convert_md_to_pdf.sh`: 変換のエントリーポイント
- `scripts/crop_pdf.py`: 末尾余白トリム
- `assets/pdf-style.css`: 1枚PDF化のためのCSS
