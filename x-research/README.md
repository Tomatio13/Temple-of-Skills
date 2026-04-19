# X Research Skill (SocialData)

SocialData API を使って X の投稿を収集し、必要に応じて記事本文取得・重複除去・整列・レポート出力まで行う Skill です。

## できること

- `searchMode=articles`
  - `url:x.com/i/article` を対象に検索
  - article detail API で本文取得
  - Draft.js 風コンテンツを Markdown 化
  - タイトル + 著者で重複除去
- `searchMode=posts`
  - 通常ポスト検索
  - センチメントや論点収集向け
  - `TSLA (bullish OR upside OR catalyst)` のような query を直接扱える

## 必要な環境変数

```bash
export SOCIALDATA_API_KEY=your_api_key
```

## 実行スクリプト

```bash
bun run scripts/run-search.ts [options]

# or, from the workspace root
bun run skills/x-research/scripts/run-search.ts [options]
```

この skill は skill 配下の `scripts/run-search.ts` と `lib` で自己完結している。通常利用では `src/core` を読まずにこのスクリプトを直接実行する。

## 主なオプション

- `--query`
- `--search-mode articles|posts`
- `--min-faves <number>`
- `--since YYYY-MM-DD`
- `--until YYYY-MM-DD`
- `--language-filter ja|other|all`
- `--output-format markdown|json|both`
- `--type Latest|Top`
- `--max-pages <number>`
- `--max-items <number>`
- `--skip-full-article`

## Query 例

### 記事収集

```bash
bun run scripts/run-search.ts \
  --search-mode articles \
  --query "生成AI" \
  --min-faves 100 \
  --since YYYY-MM-DD \
  --until YYYY-MM-DD \
  --language-filter ja \
  --output-format both \
  --max-pages 2 \
  --max-items 10
```

```bash
bun run scripts/run-search.ts \
  --search-mode articles \
  --query "bitcoin OR crypto OR macro" \
  --min-faves 200 \
  --since YYYY-MM-DD \
  --until YYYY-MM-DD \
  --language-filter all \
  --output-format markdown \
  --max-pages 3 \
  --max-items 15
```

### センチメント / ポスト検索

```bash
bun run scripts/run-search.ts \
  --search-mode posts \
  --query "TSLA (bullish OR upside OR catalyst)" \
  --min-faves 50 \
  --since YYYY-MM-DD \
  --until YYYY-MM-DD \
  --output-format both \
  --max-pages 2 \
  --max-items 20
```

```bash
bun run scripts/run-search.ts \
  --search-mode posts \
  --query "NVDA (bearish OR downside OR risk)" \
  --min-faves 30 \
  --since YYYY-MM-DD \
  --until YYYY-MM-DD \
  --output-format markdown \
  --max-pages 2 \
  --max-items 20
```

## 出力形式

- `markdown`: readable report
- `json`: structured payload
- `both`: markdown + structured payload

## 注意点

- `language-filter` はプロフィール文面ベースの一次判定
- `articles` モードでは article detail API の結果をキャッシュする
- `posts` モードでは article detail API を呼ばない
- 実際のルーティングルールは [SKILL.md](./SKILL.md) を参照
