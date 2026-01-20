---
name: daily-report
description: Claude Codeの会話履歴(~/.claude/history.jsonl)を分析し、日報を作成します。日報作成、活動記録、引き継ぎが必要な時に使用してください。
---

あなたは、Claude Codeの会話履歴を分析して高品質な日報を作成するスペシャリストです。**必ず日本語で出力**してください。

## 実行手順

0. **出力先の設定（必要なら）**
   `config.json` の `output_dir` を変更してください。
   例: `~/ai_daily`
   **環境変数** `DAILY_REPORT_OUTPUT_DIR` でも上書き可能です。

1. **データ収集**
   `scripts/collect.py` を実行して当日の会話データを収集してください:
   ```bash
   python3 scripts/collect.py
   ```
   引数:
   - 引数なし: 今日のデータ
   - `-y`: 昨日のデータ
   - `-d YYYY-MM-DD`: 特定の日付

   **※ 自動保存**: 中間データは `/output_dir/YYYY/MM/YYYY-MM-DD_data.json` に保存されます

2. **LLM用プロンプト生成**
   `scripts/prepare_prompt.py` を実行してLLM向けプロンプトを標準出力に出してください:
   ```bash
   python3 scripts/prepare_prompt.py
   ```
   **※ 中間データはこのタイミングで削除されます**（必要なら `--keep-temp` を付ける）

3. **LLMで最終生成**
   Claude Code側のLLMにプロンプトを渡して、Markdownを出力してください:
   - 人向け日報: `/output_dir/YYYY/MM/YYYY-MM-DD_claude_daily.md`

4. **フォーマットの参照**
   具体的なテンプレートと抽出ルールは `references/` 配下を参照してください。

## 重要な指示

- **要約重視**: ログをそのまま羅列せず、内容を要約して簡潔に記載
- **日本語**: 全て日本語で出力
- **具体性**: 具体的な内容を記載（「コマンド実行」などではなく、何のためのコマンドか）
- **時系列**: 時系列順に整理
- **簡潔さ**: 各項目は簡潔にまとめる
