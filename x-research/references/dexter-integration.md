# Dexter Integration Notes

この skill は、Dexter へそのまま移植しやすいように責務を分けている。

## そのまま再利用する部分

- `src/core/query-builder.ts`
- `src/core/language.ts`
- `src/core/draftjs-to-markdown.ts`
- `src/core/socialdata-client.ts`
- `src/core/research.ts`
- `src/core/report.ts`

## Dexter 側で新規に作る部分

- `src/tools/search/socialdata-article-search.ts`
  - Dexter の `ToolResult` 形式へ包む薄いアダプタ
- `src/tools/search/index.ts`
  - export 追加
- `src/tools/registry.ts`
  - `SOCIALDATA_API_KEY` がある場合だけ登録
- `src/skills/x-article-research/SKILL.md`
  - 既存 `x-research` と別 skill として定義

## 切り替え方

POC 側の skill 名は `x-research` にしているが、Dexter 側では既存 skill との衝突を避けるため、新しい `x-article-research` を追加する。
その後、呼び出し元の skill 選択ロジックまたは system prompt の誘導文を変更して、新しい skill を優先させる。

## 注意点

- SocialData article endpoint は docs 上で limited access と記載されているため、Dexter 側では明確なエラー文言を返す
- `outputFormat` は Dexter 側では `markdown` を基本にし、必要なら JSON を別フィールドで返す
