---
name: agent-skills-reviewer
description: Review an Agent Skill's SKILL.md and directly referenced files when auditing, improving, or refactoring instructions, metadata, safety, workflow, or output quality.
---

# Agent Skills Reviewer

Agent Skills の品質・実用性を日本語で監査し、実行可能な改善案を返す。

## 共通原則

- **必ず**対象の `SKILL.md` を特定する。指定がなければカレントの `SKILL.md` を対象にする。
- **必ず**対象 `SKILL.md` と、その直接参照だけを読んで根拠を集める。
- 情報不足、参照不能、解消不能な矛盾は推測せず `要確認` とする。
- 矛盾は対象 `SKILL.md`、直接参照、その他の説明文書の順に扱う。優先規則がなければ変更を断定しない。
- 対象・根拠・重大度・出力契約・未解決事項を確認してレビューを完了する。

## 参照ルーティング

- 手順・例外・完了条件は [review-workflow.md](references/review-workflow.md) を読む。
- 評価観点と重大度は [quality-rubric.md](references/quality-rubric.md) を読む。
- 結果の作成は [output-contract.md](references/output-contract.md) を読む。
- 変更後の品質確認は [skill-review-evals.md](evals/skill-review-evals.md) を用いて手動Evalを実施する。

## 実行順

1. 対象と根拠を確定する。
2. Rubricで判定し、危険な欠落を `critical` として分離する。
3. 出力契約の固定見出しと必須要素で結果を返す。
4. 変更後は該当Evalを実施し、失敗を修正して再評価する。
