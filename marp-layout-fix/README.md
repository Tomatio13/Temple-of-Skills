<p align="center">
  <h1 align="center">Marp Layout Fix</h1>
</p>

<p align="center">
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Marp-CLI-blue" alt="Marp CLI"/>
  <img src="https://img.shields.io/badge/Bash-4.0%2B-green" alt="Bash"/>
  <img src="https://img.shields.io/badge/Node.js-18%2B-brightgreen" alt="Node.js"/>
</p>

Marpスライドのレイアウト崩れ（オーバーフロー、項目過多、コントラスト不足など）を検出し、修正するためのスキル・ツールセットです。

## 📋 概要

Marpの画像出力機能を使用して全ページのPNGを生成し、LLMによる修正・再検証を繰り返すための手順と補助スクリプトを提供します。

### 対応する問題

- **オーバーフロー**: スライド下部が切れる
- **項目過多**: 縦5項目以上が収まらない
- **コントラスト不足**: 背景色と文字色の見分けがつきにくい

## ⚙️ 前提条件

- [Marp CLI](https://github.com/marp-team/marp-cli) がインストールされていること
- Bash環境が利用可能であること

### Marp CLI のインストール

```bash
npm install -g @marp-team/marp-cli
```

## 🚀 クイックスタート

### 1. 画像のエクスポート

```bash
.agents/skills/marp-layout-fix/scripts/export-images.sh \
  /absolute/path/to/slides.md \
  /absolute/path/to/out
```

### 2. 画像を確認してレイアウト崩れを検出

出力されたPNGファイルを確認し、問題のあるページを特定します。

### 3. LLMに修正指示を出す

`references/prompt-template.md` を参考に、問題のあるページのPNGと共にLLMへ修正指示を渡します。

### 4. 修正の適用と検証

Markdownファイルを修正し、再度エクスポートして問題が解消されたことを確認します。

## 🔄 ワークフロー詳細

```
┌─────────────────┐
│ 1. PNGエクスポート│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. 画像確認      │
│    (問題検出)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. LLMで修正案作成│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Markdown修正  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. 再エクスポート │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ 問題解消?│
    └───┬────┘
        │ No   Yes
        ▼      │
  ┌─────┴──────┐ │
  │ 2.へ戻る   │ │
  └────────────┘ │
                 ▼
            ┌─────────┐
            │ 完了    │
            └─────────┘
```

## 📊 よくある修正パターン

| 問題 | 原因 | 対処 |
|------|------|------|
| オーバーフロー | gap/margin/paddingが大きすぎる | これらの値を小さく調整 |
| 縦5項目以上 | 1カラムでは物理的に収まらない | 2列グリッドに変更、またはスライド分割 |
| コントラスト不足 | 背景色と文字色の同系色 | 背景色と文字色のコントラスト比を拡大 |
| 画像上の文字 | 視認性が低い | bg不透明度やドロップシャドウを追加 |

## 🔧 スクリプト

### `scripts/export-images.sh`

Marpの画像出力で全ページPNGを生成します。

```bash
usage: export-images.sh /absolute/path/to/slides.md /absolute/path/to/out
```

**機能**:
- `--images png`: PNG形式で出力
- `--allow-local-files`: ローカルファイル参照に対応

**エラー**:
- Marpがインストールされていない場合: `error: marp not found in PATH`
- 引数が不足している場合: 使用方法が表示されます

## 📚 参考文献

- `references/prompt-template.md`: LLMに渡す修正指示のテンプレート

## ⚠️ 注意事項

- 画像出力のファイル名はMarpの連番形式に従います
- 出力されたPNGは検証完了後に手動で削除してください

## ライセンス

MIT License
