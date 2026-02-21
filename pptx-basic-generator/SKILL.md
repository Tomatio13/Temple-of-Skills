---
name: pptx-basic-generator
description: basic_generator.py を使った PowerPoint 生成・更新に特化したスキル。SLIDES_TO_USE / SLIDE_CONTENT の編集、テンプレートID(1-12)の適用、生成失敗時のトリアージと再実行が必要な場合に使用する。
---

# PPTX Basic Generator

`basic_generator.py` を使って、設定編集から `.pptx` 生成までを再現性高く実行する。

## 前提条件（MUST）

- Python 3.x を利用可能にする。
- 依存パッケージは仮想環境で管理する。
- `python-pptx` 未導入の場合、必ず仮想環境を作成してからインストールする。
- インストール場所は、指示があったフォルダとする。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install python-pptx
```

## ワークフロー

1. 対象ファイルを特定する。
- 既定はscripts直下の `basic_generator.py`。
- 指示があったにファイルに`basic_generator.py`をコピーして利用する。
- 同名ファイルが複数ある場合、ユーザーに対象を確認する。
- 実行前に対象パスを `TARGET_PY` として確定する。

2. 設定セクションを更新する。
- MUST: 通常のコンテンツ更新では `SLIDES_TO_USE` と `SLIDE_CONTENT` のみ編集する。
- MUST: `SLIDE_CONTENT` のキーは `output_index`（`1,2,3...`）として扱う。
- `SLIDE_TEMPLATES` / レイアウト関数 / テーマは、ユーザーが明示的に要求した場合のみ変更する。

3. データ整合性を検証する。
- グラフ: `len(categories)` と各 `series.values` の長さを一致させる。
- テーブル: 全行の列数を `len(columns)` に一致させる。
- タイムライン: `timeline_items` は最大4件。
- 固定レイアウト（9-12）は推奨件数上限を守る。

4. 生成を実行する。
- MUST: 固定コマンドではなく確定済みパスを使う。
- 実行: `python <TARGET_PY>`
- 生成物: `outputs/<script_name>.pptx` を確認する（例: `outputs/basic_generator.pptx`）。

5. 失敗時は再検証ループを回す。
- エラー原因を特定する（設定不整合 / テンプレ名不一致 / 実行環境不足）。
- 根本原因を修正する。
- 再実行して生成物を再確認する。

## テンプレート対応

- テンプレートIDと必須キーは `references/template-map.md` を参照する。

## トラブルシュート

- `Template not found`:
  - `SLIDE_TEMPLATES[slide_id]["template"]` が `TEMPLATES` に存在するか確認する。
- 内容が空・一部欠落:
  - `SLIDE_CONTENT` キーが `slide_id` ではなく `output_index` になっているか確認する。
- グラフ描画不良:
  - `series` が空でないか、`values` 長が `categories` と一致するか確認する。
- テーブル生成エラー:
  - 各行の列数が `columns` 数と一致するか確認する。

## 出力フォーマット

- Changes: 変更した設定キー（`SLIDES_TO_USE` / `SLIDE_CONTENT` の対象 index）
- Result: 生成ファイルパス
- If failed: 根本原因と適用した修正
