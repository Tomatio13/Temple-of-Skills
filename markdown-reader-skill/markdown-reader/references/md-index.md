# md-index

`treemd` 互換のコマンド仕様（最低限）に合わせた、軽量Markdown CLIです。

対応機能:
- 見出しツリー表示: `--tree`
- セクション抽出: `-s/--section`（完全一致を優先、なければ部分一致）

## Usage

```bash
# ツリー表示
./md-index.py --tree README.md

# セクション抽出（完全一致/部分一致）
./md-index.py -s "Installation" README.md

# stdin
cat README.md | ./md-index.py --tree
cat README.md | ./md-index.py -s "Usage"
```

## Notes

- コードフェンス内の見出しは無視します。
- セクション抽出は、指定見出し直下から同レベル以上の次見出し直前までを返します。
- 部分一致が複数ヒットした場合はエラーになります。
