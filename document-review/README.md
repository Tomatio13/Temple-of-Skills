<h1 align="center">document-review</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

ドキュメント/READMEの品質レビューと改善提案を行うための Agent Skill です。
タイトルやバッジの中央揃え、言語切り替えバッジ、絵文字の活用、インストール/使用方法の明確さ、スクリーンショットの有無などをチェックし、英日ドキュメントの一貫性も評価します。

## できること
- ドキュメント品質チェック（中央揃え、バッジ配置、絵文字活用、手順の明確さ）
- 英語/日本語ドキュメントの一貫性チェック
- 問題点の指摘と具体的な改善提案の提示
- 重要な改善点の修正例（Markdown/HTML）提示
- 可能な範囲での自動修正と変更内容の報告

## 想定入力
- README.md / README_JP.md
- 設計・仕様・ガイドなどのドキュメント

## 出力形式（概要）
- チェックリスト項目ごとの評価（[✅/❌/⚠️]）
- 問題がある場合のみ、原因と改善提案
- 重要点の具体的な修正例
- 実施した自動修正内容の報告

## 使い方例
- 「この README を document-review でチェックして」
- 「英日 README の一貫性を確認して」

## チェックリスト（抜粋）
### 📝 ドキュメントの品質確認
- タイトルの中央揃え
- ヘッダー画像の中央揃え
- 技術スタックバッジの配置
- 言語切り替えバッジの配置
- 絵文字の活用
- インストール手順/使用方法の明確さ
- スクリーンショット/図の有無

### 📚 ドキュメンテーション全体の一貫性
- 英日ドキュメントの有無
- タイトル/言語バッジの統一
- 内容の簡素化とコード参照
- 冗長表現の排除
- 用語の一貫性

## 言語切り替えバッジ例
```markdown
<p align="center">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>
```

## 注意
- 情報不足の場合は「確認が必要」と明示します。
- 指摘は簡潔に、改善提案は具体的に記述します。
- 英語版の作成は必ずユーザーに確認してから行います。
