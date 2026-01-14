<h1 align="center">agent-memory</h1>

<p align="center">
  <img src="https://img.shields.io/badge/agent-skill-orange" alt="agent skill"/>
  <img src="https://img.shields.io/badge/Agent%20Skills-lightgrey" alt="Agent Skills"/>
</p>

Codex の「agent-memory」スキル用リポジトリです。ユーザーからの記憶の保存・想起・整理の依頼に対応するための手順・ドキュメントを管理します。

## 概要
- 記憶に関する依頼（例: remember this / save this / what did we discuss）を検知したら本スキルを使用します。
- ローカルの `SKILL.md` を起点に、必要最小限の情報を読み込んで対応します。

## 構成
- `SKILL.md`: スキルの手順・ルール
- `references/`: 必要に応じて参照する補助資料（存在する場合）
- `scripts/`: 作業を自動化するスクリプト（存在する場合）

## 使い方（Codex 側の運用メモ）
1. スキル適用が必要な依頼か判断する
2. `SKILL.md` を開き、必要な範囲だけ読む
3. 指示に従って作業を実施
4. 追加ファイルは必要最小限だけ参照

## ライセンス
TBD
