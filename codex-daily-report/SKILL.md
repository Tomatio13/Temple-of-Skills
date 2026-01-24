---
name: codex-daily-report
description: Codexの会話履歴(~/.codex/session配下)を分析し、日報を作成します。Codexの会話ログを基に日報を作成したい時に使用してください。
---

あなたは、Codexの会話履歴から所定テンプレに沿った日報を作成するスペシャリストです。

## 前提
- Python 3 が利用可能
- `~/.codex/session` を読み取れる権限がある
- 日付の基準はローカルタイムゾーン

## 実行手順

1. **出力先の設定（必要なら）**
   `config.json` の `output_dir` を変更してください。
   例: `~/ai_daily`
   **環境変数** `DAILY_REPORT_OUTPUT_DIR` でも上書き可能です。設定されている場合は環境変数が優先されます。

2. **データ収集**
   `scripts/collect.py` を実行して当日の会話データを収集してください:
   ```bash
   python3 scripts/collect.py
   ```
   引数:
   - 引数なし: 今日のデータ
   - `-y`: 昨日のデータ
   - `-d YYYY-MM-DD`: 特定の日付

   **※ 自動保存**: 中間データは `${output_dir}/YYYY/MM/YYYY-MM-DD_data.json` に保存されます

3. **LLM用プロンプト生成**
   `scripts/prepare_prompt.py` を実行してLLM向けプロンプトを標準出力に出してください:
   ```bash
   python3 scripts/prepare_prompt.py
   ```
   **※ 中間データはこのタイミングで削除されます**（必要なら `--keep-temp` を付ける）

4. **LLMで最終生成**
   `prepare_prompt.py` の出力をCodex側のLLMに渡して、Markdownを出力してください。

5. **日報の保存**
   生成されたMarkdownを `scripts/save_report.py` で保存してください:
   ```bash
   python3 scripts/save_report.py -d YYYY-MM-DD < report.md
   ```
   - 人向け日報: `${output_dir}/YYYY/MM/YYYY-MM-DD_codex_daily.md`

6. **フォーマットの参照**
   具体的なテンプレートと抽出ルールは `references/prompt_daily.md` を参照してください。

## 重要な指示

- **要約重視**: ログをそのまま羅列せず、内容を要約して簡潔に記載
- **日本語**: 全て日本語で出力
- **具体性**: 具体的な内容を記載（「コマンド実行」などではなく、何のためのコマンドか）
- **時系列**: 時系列順に整理
- **簡潔さ**: 各項目は簡潔にまとめる
- **必須要素**: 作業内容/成果/次の一手を含める
