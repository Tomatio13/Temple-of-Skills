---
name: markdown-reader
description: Read Markdown progressively by first getting an outline, then extracting specific sections. Use for any Markdown reading, not just large files.
compatibility: Requires Python 3. Runs scripts from the skill's scripts/ directory.
---

# Markdown を段階的に読む

## いつ使うか
- まず見出し構造を把握し、必要な章だけ抽出したいとき
- Markdown を読むときは基本的にこのスキルを使う

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
- 目的の見出しが見つからない場合は、見出しレベルや表記を見直す

## トラブルシューティング
- `python3: command not found` の場合は Python 3 をインストール
- `No input provided` が出た場合は Markdown ファイルを指定するか stdin を渡す
- 期待した内容が出ない場合は見出し名を再確認する
