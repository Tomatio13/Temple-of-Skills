<h1 align="center">Agent Skills Reviewer</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

Agent Skills の `SKILL.md` と直接参照を監査し、根拠付きの改善案を日本語で返すSkillです。Skill本体は共通原則と参照ルーティングだけを持ち、詳細規約と評価資産は分離しています。

## 構成

```text
agent-skills-reviewer/
├── SKILL.md
├── references/
│   ├── review-workflow.md
│   ├── quality-rubric.md
│   └── output-contract.md
└── evals/
    └── skill-review-evals.md
```

## 使い方

CodexのSkillsディレクトリへコピーしてください。

```bash
cp -pr agent-skills-reviewer ~/.codex/skills/agent-skills-reviewer/
```

監査・改善・リファクタリングを依頼すると、Skillは対象 `SKILL.md` を確定してから必要な参照だけを読みます。対象が指定されない場合はカレントディレクトリの `SKILL.md` を使います。

## レビューの保証範囲

- `SKILL.md`、そのfrontmatter、本文、直接リンクされた参照を対象にします。
- 不足情報、アクセス不能な参照、矛盾は推測せず `要確認` として報告します。
- 結果は「重大な指摘」「改善提案」「軽微な指摘」「修正案（抜粋）」の4見出しで返します。
- Skillがもっともらしい回答を返すことと、実際に安全に作業を完了できることは別です。後者は実行環境で別途確認してください。

## 手動Eval

`evals/skill-review-evals.md` には、実務的な自由回答を評価する6ケースと項目別Rubricがあります。Skillまたは参照規約を変更したら該当ケースを実施してください。

- `critical` 項目を1件でも落とした回答は不合格です。
- 通常項目は80%以上を初期合格基準とします。
- 2回の独立採点で不一致だった項目だけを3回目に判定し、実施日・モデル・コミットを記録します。
