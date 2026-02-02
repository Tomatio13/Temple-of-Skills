# Marp Layout Fix Prompt Template

以下を埋めてLLMへ渡す。

指示:
Markdownファイル名: {MARKDOWN_FILENAME}
対象ページ番号: {TARGET_PAGE_NUMBER}
PNGフルパス: {PNG_FULLPATH}

対象ページのPNG画像を参照し、以下の事象があればMarkdownファイルを修正してください。
- オーバーフロー(下部が切れる)
  - 原因: gap/margin/paddingが大きすぎる
  - 対処: gap/margin/paddingを小さくする方向で調整
- 縦5項目以上が収まらない
  - 原因: 1カラムでは物理的に収まらない
  - 対処: 2列グリッドに変更、またはスライド分割
- コントラスト不足
  - 原因: 背景色と文字色の同系色で見にくい
  - 対処: 背景色と文字色のコントラスト比を十分に確保
  - 画像上に文字を置く場合: bg不透明度やドロップシャドウで視認性を高める

修正後、コマンドでPNGを再生成し、問題がなくなるまで繰り返す。
../scripts/export-images.sh
