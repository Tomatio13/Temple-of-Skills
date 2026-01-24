<h1 align="center">Agent Skills Reviewer</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
</p>

Agent Skills の品質・実用性を評価し、SKILL.md の改善点を指摘するためのスキルです。レビュー対象は指示文・メタデータ・参照構造・出力形式などに及びます。

## ✨ 特徴

- SKILL.md の品質監査に特化
- メタデータ・指示・構造・検証ループを体系的に評価
- 修正方針まで含めたレビュー出力
- 参照は SKILL.md から 1 階層に限定

## ✅ 必要要件

- 対象の SKILL.md にアクセスできること

## 🚀 使い方

Codex の Skills ディレクトリにコピーしてください（既に存在する場合は上書きになります）。

```bash
cp -pr agent-skills-reviewer ~/.codex/skills/agent-skills-reviewer/
```

Codex 内で `agent-skills-reviewer` を選択してください。

## 🧭 レビュー手順（最小フロー）

1. パラメータで指定された SKILL.md を開く（未指定ならカレント）
2. フロントマター（name/description）を確認
3. 見出し構造を把握し、必要セクションを抽出
4. SKILL.md から直接リンクされている参照ファイルのみ確認
5. 出力フォーマットに従ってレビュー結果を作成

## ✅ チェックリスト

- メタデータ妥当性（name/description）
- トリガー条件の明確さ（いつ使うか）
- 指示の具体性・過不足（自由度の適正）
- 参照構造の健全性（1階層、見通し）
- 例・テンプレの有用性
- 検証/フィードバックループの有無
- 時間依存・環境依存の記述
- セキュリティ/安全性（入力検証など）

## 📤 出力フォーマット

必ず次の構成で返します。

1. **重大な指摘**（あれば）
2. **改善提案**（優先度順）
3. **軽微な指摘**（あれば）
4. **修正案（抜粋）**（必要な箇所のみ）

各指摘は箇条書きで、可能な限りファイル名と行の目安を付け、
「影響」「根拠」「修正方針」をこの順で 1 行ずつ記載します。

## ⚠️ 注意事項

- 断定できない点は「要確認」と明示します。
- 変更による影響やトレードオフを簡潔に述べます。
- 余計な追記より「削る提案」を優先します。

