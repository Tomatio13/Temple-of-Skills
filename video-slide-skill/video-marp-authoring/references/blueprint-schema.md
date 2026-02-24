# Blueprint Schema (Skill 1)

LLMが入力Marpを読んで、このJSON設計図を作る。Pythonはこの設計図を検証して最終MDをレンダリングする。

## JSON構造

```json
{
  "frontmatter_overrides": {
    "title": "AI-Powered Data Analytics",
    "author": "Your Name"
  },
  "slides": [
    {
      "layout": "cover",
      "video": "videos/slide1.mp4",
      "fields": {
        "LOGO": "OPTIMAL AI",
        "SLIDE_TITLE": "AI-Powered Data Analysis",
        "SLIDE_SUBTITLE": "Unlocking Business Potential",
        "SLIDE_META": "By Team",
        "PAGE_NUM": "001"
      }
    }
  ]
}
```

## 必須

- `slides[]` は必須
- 各スライドで `layout`, `video` は必須

## layout 値

- `cover`
- `intro`
- `grid`
- `quote`
- `outro`

`references/video-pitch-deck-template.md` 内の `<!-- Layout N: ... -->` 名と一致させる。

## fields

- プレースホルダ名に対応する値を渡す。
- 未指定だと一部はデフォルト補完される（`LOGO`, `CONTACT_*` など）。
- 置換されずに `{{...}}` が残るとエラーになる。

## 運用

1. LLMが入力Marpを読み、スライドごとに `layout` と `fields` を決める。
2. ユーザーからページ別動画指定を受け、`video` を埋める。
3. `generate_video_marp.py --mode blueprint --blueprint-file ...` で生成する。
