<h1 align="center">Codex Daily Report</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>

Codex の会話履歴（`~/.codex/session` 配下）を解析し、日報作成のためのAgent Skillです。

## ✨ 特徴

- 指定日の会話ログを収集して中間データ化
- 日報生成用のプロンプトを自動生成
- Git の変更統計（コミット数・追加/削除行数など）を集計
- 出力先は `config.json` または環境変数で切り替え可能

## ✅ 必要要件

- Python 3.x
- Codex の会話履歴が `~/.codex/session` 配下に存在すること

## 🚀 使い方

CodexのSkillsディレクトリにコピーしてください（既に存在する場合は上書きになります）。

```bash
cp -pr codex-daily-report ~/.codex/skills/daily-report/
```

Codex内で`/daily-report`を選択してください。


## 📅 日付指定

- **昨日のデータ**  
`/daily-report -y`

- **特定日付（YYYY-MM-DD）**  
`/daily-report -d 2026-01-18`

## 📦 出力先の設定

`config.json` の `output_dir` を変更するか、環境変数 `DAILY_REPORT_OUTPUT_DIR` で上書きできます。

- `config.json` 例（`~` は展開されないためフルパス推奨）:
  ```json
  {
    "output_dir": "~/ai_daily"
  }
  ```

- 環境変数:
  ```bash
  export DAILY_REPORT_OUTPUT_DIR=~/ai_daily
  ```

## 🗂️ 生成データ

- **中間データ**: `/output_dir/YYYY/MM/YYYY-MM-DD_data.json`
  - `prepare_prompt.py` 実行時に削除（`--keep-temp` で保持可能）
- **日報の最終 Markdown**: `/output_dir/YYYY/MM/YYYY-MM-DD_codex_daily.md`
  - 生成は LLM 側で実施
  - 生成後に `scripts/save_report.py` で保存

## 🧩 テンプレート

- `references/prompt_daily.md` をプロンプトテンプレートとして使用します。

## ⚠️ 注意事項

- 履歴ファイルが存在しない場合はエラーになります。
- Git 統計は `.git` が存在するプロジェクトのみ集計します。
- 個人情報や機密情報の取り扱いに注意してください。
