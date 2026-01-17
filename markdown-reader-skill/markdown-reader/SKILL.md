---
name: markdown-reader
description: Read Markdown progressively by first getting an outline, then extracting specific sections. Use for any Markdown reading, not just large files.
---

# Markdown を段階的に読む

## いつ使うか
- まず見出し構造を把握し、必要な章だけ抽出したいとき
- Markdown を読むときは基本的にこのスキルを使う

## 前提
- `treemd` がインストール済み
- 対象の Markdown がローカルにある

## 基本手順（段階的読み込み）
1. 見出しツリーを表示する  
   `treemd --tree path/to/doc.md`
2. 読みたい見出し名を正確に選ぶ
3. セクションを抽出する  
   `treemd --section "見出し名" path/to/doc.md`

## 推奨フロー
1. まずは大見出し（H1/H2）で `--tree`
2. 必要な章だけ `--section` で読む
3. さらに細分化が必要なら小見出しで `--section`

## 例
```
treemd --tree README.md
treemd --section "Installation" README.md
```

## 注意点
- `--section` は見出し名の完全一致が基本。表記ゆれに注意する
- 目的の見出しが見つからない場合は、見出しレベルや表記を見直す

## トラブルシューティング
- `treemd: command not found` の場合は `cargo install treemd`
- 期待した内容が出ない場合は見出し名を再確認する
