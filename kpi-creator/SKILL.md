---
name: kpi-creator
description: KPI/CSFを決めるためのStep1-2（プロセスのモデル化→CSFの絞り込み→KPI目標設定）を実行する。ユーザーから「売り上げUPのためのKPIを立てる」「CSFとKPIを決めたい」「KPIの目標値を逆算したい」などの依頼が来たときに使う。
---

# KPI-CSF-KPI Flow

## Overview
- Step1-3の流れでCSFとKPIを決定する
- 参照資料として `references/kpi-step.md` を読む

## Workflow Decision Tree
- 目的(KGI)や期間が不明なら先に確認する
- 数式モデルが作れない場合は、売上/利益/費用など上位式から仮モデルを提案し合意を取る
- 変数が多い場合は、可制御性/影響度で優先順位を付けてCSFを絞る

## Step1: プロセスの確認(モデル化)
- 目的(KGI)を1行で数式化する
- 上位式を因数分解して、因果の木を作る
- 例: 売上 = 販売数量 × 平均単価 = (アプローチ量 × 歩留まり率) × 平均単価

### Ask
- KGIは何か(数値/期間)
- 現状値は何か
- 事業の収益ドライバは何か(商品単価、成約率、訪問数など)

## Step2: 絞り込み(CSFの設定)
- 数式の項目を「定数」と「変数」に分ける
- 定数はCSF候補から除外する
- 変数から、現場でコントロール可能かつ影響の大きい項目をCSFに選ぶ
- 必要なら変数を工程に分解し、最重要プロセスを特定する

### Output
- 変数/定数の一覧
- CSF候補リスト
- 最終CSF(1-3個)と理由

## Step3: 目標設定(KPI)
- CSFを数値目標(KPI)に落とし込む
- KGIから逆算してKPI目標を算出する
- 期間と測定頻度を明記する

### Output
- KPI定義(数式/対象/期間/頻度)
- KPI目標値(逆算の根拠付き)

## Output Format
- KGI
- Step1 モデル式
- Step2 CSF
- Step3 KPI目標

## References
- `references/kpi-step.md`
