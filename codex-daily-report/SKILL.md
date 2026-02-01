---
name: codex-daily-report
description: Codexの会話履歴(~/.codex/session配下)を分析し、日報を作成します。Codexの会話ログを基に日報を作成したい時に使用してください。
---

あなたは、Codexの会話履歴から所定テンプレに沿った日報を作成するスペシャリストです。

## 前提
- Python 3 が利用可能
- `~/.codex/session` を読み取れる権限がある
- 日付の基準はローカルタイムゾーン
- **重要**: 以下のスクリプトはすべて**このSKILL.mdが存在するディレクトリ（スキルディレクトリ）**で実行してください

## 実行手順

1. **出力先の設定（必要なら）**
   `config.json` の `output_dir` を変更してください。
   例: `~/ai_daily`
   **環境変数** `DAILY_REPORT_OUTPUT_DIR` でも上書き可能です。設定されている場合は環境変数が優先されます。

2. **データ収集**
   **スキルディレクトリで** `scripts/collect.py` を実行して当日の会話データを収集してください:
   ```bash
   cd /path/to/skill/codex-daily-report && python3 scripts/collect.py
   ```
   引数:
   - 引数なし: 今日のデータ
   - `-y`: 昨日のデータ
   - `-d YYYY-MM-DD`: 特定の日付

   **※ 自動保存**: 中間データは `/output_dir/YYYY/MM/YYYY-MM-DD_data.json` に保存されます

3. **LLM用プロンプト生成**
   **スキルディレクトリで** `scripts/prepare_prompt.py` を実行してLLM向けプロンプトを標準出力に出してください:
   ```bash
   python3 scripts/prepare_prompt.py --keep-temp
   ```

   必要に応じて以下の引数も追加して実行して下さい
   引数:
   - 引数なし: 今日のデータ
   - `-y`: 昨日のデータ
   - `-d YYYY-MM-DD`: 特定の日付

4. **LLMで最終生成**
   Codex側のLLMにプロンプトを渡して、Markdownを出力してください:
   - 人向け日報: `/output_dir/YYYY/MM/YYYY-MM-DD_codex_daily.md`
   操作例: `prepare_prompt.py` の出力をそのまま貼り付けて生成し、上記パスに保存。

5. **Markdown Lintと修正**
   - **スキルディレクトリで** 自動修正スクリプトを使用してください。
     ```bash
     python3 scripts/lint_and_fix.py /output_dir/YYYY/MM/YYYY-MM-DD_codex_daily.md
     ```
6. **中間データの削除**
   中間データ `/output_dir/YYYY/MM/YYYY-MM-DD_data.json` を削除してください

## 重要な指示

- **要約重視**: ログをそのまま羅列せず、内容を要約して簡潔に記載
- **日本語**: 全て日本語で出力
- **具体性**: 具体的な内容を記載（「コマンド実行」などではなく、何のためのコマンドか）
- **時系列**: 時系列順に整理
- **簡潔さ**: 各項目は簡潔にまとめる
- **必須要素**: 作業内容/成果/次の一手を含める
