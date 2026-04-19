---
name: x-research
description: Use this skill whenever the user wants to research X/Twitter with SocialData API, including normal post sentiment searches and long-form article searches. Trigger it for date ranges, likes thresholds, Japanese filtering, article extraction, deduplication, engagement ranking, reusable report output, or sentiment-style queries such as "TSLA (bullish OR upside OR catalyst)".
---

# X Research Skill (SocialData)

SocialData API を使って X の投稿を収集し、必要に応じて article 本文を取得し、重複除去と並び替えを行ってレポート化する。将来的に Dexter へ移植しやすいよう、再利用しやすい出力を優先する。

## Execution Rule

- MUST: bundled script を直接使う。`cwd` が skill directory の場合は `scripts/run-search.ts`、workspace root の場合は `skills/x-research/scripts/run-search.ts` を使う。
- MUST: 通常の検索依頼では skill 配下の `lib` だけを前提に実行する。
- MUST NOT: デバッグや改修でない限り `src/core/*.ts` を読まない。
- MUST NOT: 検索前に型定義や内部実装の確認を始めない。
- MUST: まず必要なパラメータを決めてスクリプトを実行し、その結果を要約する。

## Inputs

ユーザー要件を次のパラメータに落とし込む:

- `query`: 必須。検索テーマまたは X query
- `searchMode`: 任意。`articles` または `posts`。デフォルトは `articles`
- `minFaves`: 任意。最低いいね数。ノイズが多いときに引き上げる
- `since`: 任意。開始日 `YYYY-MM-DD`
- `until`: 任意。終了日 `YYYY-MM-DD`
- `languageFilter`: 任意。`ja`、`other`、`all`。デフォルトは `all`
- `outputFormat`: 任意。`markdown`、`json`、`both`。デフォルトは `markdown`
- `type`: 任意。`Latest` または `Top`。通常は `Latest`
- `maxPages`: 任意。検索ページ数。網羅性が必要なときに増やす
- `maxItems`: 任意。処理件数の上限
- `fetchFullArticle`: 任意。`searchMode=articles` のときだけ有効。デフォルトは有効

## Workflow

1. SocialData 検索クエリを組み立てる。`searchMode=articles` のときだけ `url:x.com/i/article` を付ける。返信を明示的に求められない限り `-filter:replies` を維持する。
2. `/twitter/search` をページネーションし、必要件数または `next_cursor` の終端まで取得する。
3. 各 hit をプロフィール情報から `ja` / `other` に一次分類する。
4. `searchMode=articles` のときだけ `/twitter/article/{tweetId}` を取得し、キャッシュがあれば再利用する。
5. `articles` の場合は Draft.js 風コンテンツを Markdown に変換する。`posts` の場合はポスト本文をそのまま扱う。
6. `title + author` で重複除去し、もっとも likes が高いものを残す。
7. エンゲージメント順に並べる。
8. 指定された `outputFormat` で返す。

## Validation Loop

- ノイズが多い:
  - `minFaves` を上げる
  - `query` をより具体的にする
- 件数が少ない:
  - `query` を広げる
  - `languageFilter=all` に戻す
  - `maxPages` を増やす
- article 本文が不要:
  - `searchMode=posts` を使う
  - または `fetchFullArticle` を無効にする
- 速報性を上げたい:
  - `since` と `until` を狭める
- 網羅性を上げたい:
  - `maxPages` と `maxItems` を増やす

## Query examples

以下は出発点の例。ユーザーが速報性・網羅性・ノイズ削減のどれを重視するかに応じて、likes 閾値、期間、language filter、page 数を調整する。

### 記事収集パターン

- Japanese AI articles:
  - `query="生成AI"` with `searchMode=articles`
- Bitcoin or macro article posts:
  - `query="bitcoin OR crypto OR macro"` with `searchMode=articles`
- Company-specific long-form posts:
  - `query="Tesla OR TSLA"` with `searchMode=articles`
- Product or policy commentary:
  - `query="OpenAI OR ChatGPT OR policy"` with `searchMode=articles`

These will be combined with:

- `url:x.com/i/article`
- `-filter:replies`
- optional `min_faves:...`
- optional `since:YYYY-MM-DD`
- optional `until:YYYY-MM-DD`

### ポスト / センチメント探索パターン

- Tesla bullish sentiment:
  - `query="TSLA (bullish OR upside OR catalyst)"` with `searchMode=posts`
- Nvidia bearish or risk discussion:
  - `query="NVDA (bearish OR downside OR risk)"` with `searchMode=posts`
- Bitcoin debate:
  - `query="bitcoin (bullish OR bearish OR catalyst)"` with `searchMode=posts`
- Macro reaction search:
  - `query="FOMC (bullish OR bearish OR reaction)"` with `searchMode=posts`
- Sector reaction search:
  - `query="semiconductor (bullish OR weakness OR catalyst)"` with `searchMode=posts`

These will be combined with:

- `-filter:replies`
- optional `min_faves:...`
- optional `since:YYYY-MM-DD`
- optional `until:YYYY-MM-DD`

### 完成形クエリ例

SocialData に実際に送るクエリは、次の完成形を基準に考える:

- `生成AI url:x.com/i/article -filter:replies min_faves:100 since:YYYY-MM-DD until:YYYY-MM-DD`
- `bitcoin OR crypto OR macro url:x.com/i/article -filter:replies min_faves:200 since:YYYY-MM-DD until:YYYY-MM-DD`
- `TSLA (bullish OR upside OR catalyst) -filter:replies min_faves:50 since:YYYY-MM-DD until:YYYY-MM-DD`
- `NVDA (bearish OR downside OR risk) -filter:replies min_faves:30 since:YYYY-MM-DD until:YYYY-MM-DD`

## Bundled scripts

補助スクリプトで再現可能な実行を行う:

```bash
bun run scripts/run-search.ts --search-mode articles --min-faves 100 --since YYYY-MM-DD --until YYYY-MM-DD --output-format both

# or, from the workspace root
bun run skills/x-research/scripts/run-search.ts --search-mode articles --min-faves 100 --since YYYY-MM-DD --until YYYY-MM-DD --output-format both
```

ローカル保存が必要なら、カレントワークスペースに出力する。ファイル名は `x-research-report.md` または `x-research-report.json` を推奨する。

## Response Template

最終応答は次の順に固定する:

1. `Query Summary`
2. `Search Mode`
3. `Top Findings`
4. `Caveats`

- `markdown`: 人間向けの読みやすい要約
- `json`: 機械処理向けの構造化出力
- `both`: 上記の両方が必要な場合
- センチメントや論点探索には `searchMode=posts` を使う。例: `TSLA (bullish OR upside OR catalyst)`

## Failure Handling

- `SOCIALDATA_API_KEY` が無い場合は、推測実行せず停止する。
- SocialData が未設定であることを明確に伝える。
- 一般的な X センチメントだけが必要な場合でも、SocialData が無いなら別の検索経路が必要だと伝える。

## Notes

- `SOCIALDATA_API_KEY` は必須。環境変数からのみ読み込み、ハードコードしない。
- 日本語判定はプロフィール文面ベースの一次判定であり、完全ではない。
- article 本文がキャッシュ由来かどうかが重要な場合は、その旨を明記する。
