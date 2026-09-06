# ウォードリーマップ

## 用途と選択

- 価値連鎖と進化段階から内製・購入の判断を整理する。実行時の通信は構成図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 利用者の要求、依存する機能、可視性、発生・個別開発・製品・汎用化の段階。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 縦は利用者からの可視性、横は四つの進化段階にする。点の位置が意味を持つため、依存線は斜めの直線を許容する。
- 予測する進化は右向きの破線矢印で依存線と区別する。

## 意味と検証

- 可視性と進化を数値スコアにしない。位置は判断と根拠を記し、予測を確定した事実と混同しない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 利用者の検索要求が、製品化された検索機能と汎用基盤に依存する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 340" width="320" role="img" aria-labelledby="example-wardley-title example-wardley-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-wardley-title">ウォードリーマップの最小例</title>
  <desc id="example-wardley-desc">利用者の検索要求が、製品化された検索機能と汎用基盤に依存する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="32" y1="264" x2="304" y2="264" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="24" y="28" text-anchor="middle" font-size="18">
      <tspan x="24" y="28">可視</tspan>
    </text>
    <text x="36" y="316" text-anchor="middle" font-size="18">
      <tspan x="36" y="316">不可視</tspan>
    </text>
    <line x1="100" y1="60" x2="100" y2="264" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <line x1="168" y1="60" x2="168" y2="264" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <line x1="236" y1="60" x2="236" y2="264" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <text x="64" y="286" text-anchor="middle" font-size="18">
      <tspan x="64" y="286">発生</tspan>
    </text>
    <text x="132" y="286" text-anchor="middle" font-size="18">
      <tspan x="132" y="286">個別</tspan>
    </text>
    <text x="200" y="286" text-anchor="middle" font-size="18">
      <tspan x="200" y="286">製品</tspan>
    </text>
    <text x="268" y="286" text-anchor="middle" font-size="18">
      <tspan x="268" y="286">汎用</tspan>
    </text>
    <line x1="132" y1="64" x2="200" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="200" y1="132" x2="268" y2="200" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="132" cy="64" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="200" cy="132" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="268" cy="200" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <rect x="216" y="113" width="78" height="26" fill="var(--mb-surface, #FFFFFF)"/>
    <text x="132" y="48" text-anchor="middle" font-size="18">
      <tspan x="132" y="48">検索要求</tspan>
    </text>
    <text x="218" y="134" text-anchor="start" font-size="18">
      <tspan x="218" y="134">検索機能</tspan>
    </text>
    <text x="268" y="238" text-anchor="middle" font-size="18">
      <tspan x="268" y="238">基盤</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-wardley.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
