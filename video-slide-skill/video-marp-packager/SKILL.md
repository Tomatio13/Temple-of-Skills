---
name: video-marp-packager
description: 動画対応Marp Markdownをクリック遷移可能なHTMLへ変換し、必要動画・ローカルフォント・ライセンス文書を収集して portable/deck-name.tar.gz を生成するときに使う。
---

# Video Marp Packager

## Overview

動画対応Marpを配布可能なポータブル構成へ変換する。HTML生成、クリック遷移注入、動画収集、フォント同梱、tar.gz作成を一括で行う。

## Workflow

1. ユーザーに動画対応Marpファイルを指定してもらう。
2. 必要に応じて動画探索ベースディレクトリを指定してもらう。
3. オフラインフォント再現を行う場合、`.woff2` フォントディレクトリとライセンスファイルを指定してもらう。
4. `scripts/build_portable_bundle.py` を実行する。
5. 生成された `portable/<deck-name>.tar.gz` の内容を確認する。

## Command

```bash
python skills/video-marp-packager/scripts/build_portable_bundle.py \
  marp/input-video.md \
  --output-root portable \
  --video-base . \
  --font-dir ./fonts/plus-jakarta-sans \
  --font-license ./fonts/plus-jakarta-sans/OFL.txt
```

## Output

- `portable/<deck-name>/marp/<deck-name>.html`
- `portable/<deck-name>/public/videos/*.mp4`
- `portable/<deck-name>/fonts/*.woff2`（指定時）
- `portable/<deck-name>/LICENSES/*`（指定時）
- `portable/<deck-name>.tar.gz`
