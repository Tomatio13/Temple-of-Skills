---
name: markdown-reader
description: 見出し構造の把握や部分抽出が必要な Markdown 読解に使う。短文は通常読解でよい。
compatibility: Python 3 が必要。スキル内の scripts/ ディレクトリのスクリプトを実行する。
---

# Markdown を段階的に読む

## いつ使うか
- まず見出し構造を把握し、必要な章だけ抽出したいとき
- 章単位での引用・確認が必要なとき
- 数行程度の短い Markdown は通常読解で十分

## 前提
- Python 3 が利用可能
- スクリプト `scripts/md-index.py` を使用
- 対象の Markdown がローカルにある

## 基本手順（段階的読み込み）
1. 見出しツリーを表示する  
   `python3 scripts/md-index.py --tree path/to/doc.md`
2. 読みたい見出し名を正確に選ぶ
3. セクションを抽出する  
   `python3 scripts/md-index.py --section "見出し名" path/to/doc.md`
   ※ スキルディレクトリで実行するか、`scripts/md-index.py` を絶対パスで指定する

## 推奨フロー
1. まずは大見出し（H1/H2）で `--tree`
2. 必要な章だけ `--section` で読む
3. さらに細分化が必要なら小見出しで `--section`

## 例
```
python3 scripts/md-index.py --tree README.md
python3 scripts/md-index.py --section "Installation" README.md
```

## 注意点
- `--section` は見出し名の完全一致が基本。表記ゆれに注意する
- 大小文字・全角半角・記号の差は区別される前提で一致させる
- 目的の見出しが見つからない場合は、見出しレベルや表記を見直す

## トラブルシューティング
- `python3: command not found` の場合は Python 3 をインストール
- `No input provided` が出た場合は Markdown ファイルを指定するか stdin を渡す
- `scripts/md-index.py` が見つからない場合は作業ディレクトリかパスを確認
- 期待した内容が出ない場合は見出し名を再確認する
