<h1 align="center">marp-slide-creator</h1>

<p align="center">Marp形式のスライド作成を補助する Agent Skill</p>

> このドキュメントは日本語のみで提供します。

このスキルは、`references/prompt.md` をベースにトピック埋め込み済みの生成プロンプトを作成し、生成したMarp Markdownを `.md` ファイルとして保存するワークフローを提供します。

## 📁 フォルダ構成

- `SKILL.md`: スキル定義（トリガー、入出力、ワークフロー、バリデーション）
- `README.md`: このドキュメント
- `references/prompt.md`: スライド生成用の参照プロンプトテンプレート

## ⚙️ できること

1. `topic` を使って `references/prompt.md` の `{{TOPIC}}` を置換し、Marp向け生成プロンプトを作る
2. 生成済みMarkdown本文を `<output_dir>/<filename>.md` に保存する

## 🎯 想定トリガー

- 「スライド用プロンプトを作って」
- 「この内容をMarkdownファイルに保存して」
- 「Marp前提で資料化したい」

## 🧾 入力仕様

### Prompt generation

- `topic` (required): プレゼンのテーマ

### File creation

- `filename` (required): 出力ファイル名（拡張子省略可）
- `content` (required): 保存するMarkdown本文
- `output_dir` (optional, default `.`): 出力先ディレクトリ

## 🚀 利用手順

1. `references/prompt.md` を開く
2. `{{TOPIC}}` を依頼テーマに置換して、生成プロンプトとして利用する
3. 生成されたMarkdownを `output_dir` 配下に `.md` ファイルとして保存する

## ✅ バリデーションと安全制約

- `filename` に `.md` が無ければ自動補完
- `filename` に `/`, `\\`, `..` を含む場合は停止
- `content` が空の場合は保存しない
- 書き込み不可ディレクトリはエラーとして扱う

## 📌 要件

- 追加ランタイム不要（標準のファイル操作で実行可能）

## 謝辞

@taiyo_ai_gakuseさん作成の [Majin-Slide-MCP](https://github.com/nanameru/Majin-Slide-MCP)を元に本Agent Skillsを作成しました。
公開ありがとうございます。

また、プロンプトを公開して下さった まじんさん も公開ありがとうございます。

