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

<p align="center">Markdown（.md）を「1ページの長尺PDF」に変換するためのAgent Skillです。<code>md-to-pdf</code> でPDF化し、PyMuPDFで下部の余白を自動トリミングするための指示・スクリプト・アセットをまとめています。</p>


## ✨ 特徴

- Agent Skillとして指示・スクリプト・アセットを同梱
- ページ分割を避けた“長尺1ページ”のPDFを生成
- CSSでページサイズ・余白・見た目を統一
- 変換後の無駄な下余白を自動クロップ
- 複数ファイルの一括変換に対応

## 📎 Agent Skills

- 公式サイト: `https://agentskills.io/home`
- 本リポジトリは Agent Skills 形式（SKILL.md + scripts/assets/resources）に準拠しています。

## 📦 必要環境

- Node.js / npm（`md-to-pdf` のため）
- Python 3（PyMuPDF用）
- `uv` があれば仮想環境作成と依存導入が高速化されます（任意）

## 📥 インストール

### 1) md-to-pdf の導入（未インストールの場合）

```bash
npm install -g md-to-pdf
```

※ `scripts/convert_md_to_pdf.sh` 実行時に未インストールだと確認が出ます。

### 2) PyMuPDF

`convert_md_to_pdf.sh` が自動で `.venv` を作成し、PyMuPDF を導入します。


### 3. Agent Skillのインストール

CodexやClaude CodeのSkillsフォルダにコピーしてください。

```bash
git clone https://github.com/Tomato13/md-to-singlepage-pdf.git
cd md-to-singlepage-pdf
cp -pr md-to-singlepage-pdf ~/.codex/skills
```


## 🚀 使い方

CodexやClaud CodeなどのLLMに対して、以下のように指示を出してください。
```text
Markdownファイル document.mdを1ページの長尺PDFに変換してください。
```

document.pdfが生成されます。

## ⚙️ 仕組み

- `assets/pdf-style.css` でページサイズを大きく指定
- `md-to-pdf` でPDF化
- `scripts/crop_pdf.py` で最下部の余白を検出してトリミング

## 🛠️ カスタマイズ

- ページサイズや余白は `assets/pdf-style.css` の `@page` を変更
- 余白の追加量（下部）は `scripts/crop_pdf.py` の `margin_bottom` を調整

## ⚠️ 注意事項

- PDF内に極端に大きい画像がある場合、意図しない余白が残ることがあります
- `md-to-pdf` は内部で Chromium を使用します


## 謝辞
[zenn : マークダウン文書を改ページなしのPDFに変換する](https://zenn.dev/lnest_knowledge/articles/91a1893b3f92f3)
を公開してくださった @shown_it さんに感謝します。


## 📄 ライセンス

MIT License
