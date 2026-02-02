---
name: marp-layout-fix
description: Marpスライドのレイアウト崩れ(オーバーフロー/項目過多/コントラスト不足など)を検出し、Marpの画像出力で全ページPNGを作成してMarkdownを直す作業に使う。Marpスライドの見切れ修正、画像上テキストの視認性改善、全ページの一括エクスポートが必要なときにトリガーする。
---

# Marp Layout Fix

## Overview
Marpの画像出力(`marp --images png`)で全ページPNGを生成し、LLMで修正・再検証を繰り返すための手順と補助スクリプトを提供する。

## Workflow

### 1) 画像エクスポート
```bash
/home/masato/.agents/skills/marp-layout-fix/scripts/export-images.sh \
  /absolute/path/to/slides.md \
  /absolute/path/to/out
```

### 2) 画像を確認してレイアウト崩れを検出
- `references/prompt-template.md` を使ってLLMに修正指示を出す
- 1ページずつ修正し、PNGを再生成して問題が解消するまで反復

### 3) 修正を適用
- Markdown/テーマCSSへ変更を適用
- 必要に応じて再エクスポートで再検証

### 4) クリーンアップ
- 出力ディレクトリのPNGを削除（必要に応じて手動で実施）

## Common Fix Patterns
- オーバーフロー: gap/margin/padding を小さくする、フォントサイズ/行間を調整
- 縦5項目以上: 2列グリッド化、分割スライド化
- コントラスト不足: 背景色と文字色の差を拡大、画像上は半透明背景/影を追加

## Scripts

### `scripts/export-images.sh`
- Marpの画像出力で全ページPNGを生成
- `--allow-local-files` を使うため、ローカルファイル参照がある場合に対応

## References

### `references/prompt-template.md`
- LLMに渡す修正指示テンプレート

## Notes
- 画像出力のファイル名は Marp の連番形式に従う
