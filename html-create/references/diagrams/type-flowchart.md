# 分岐フロー図

## 用途と選択

- 条件で処理が分岐する場合に使う。分岐のない手順は番号付き説明を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 開始・終了、処理、条件、各分岐の行き先。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 上から下を主方向にし、処理は矩形、条件は菱形、開始・終了は丸みの強い形にする。
- 条件から出るすべての線に結果を付ける。菱形の出口が多ければ条件を分ける。

## 意味と検証

- 条件の結果が網羅され、どの分岐も処理または終了へ到達するか確認する。意味のない循環を作らない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 入力が有効なら保存し、無効なら修正を依頼する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 256" width="320" role="img" aria-labelledby="example-flowchart-title example-flowchart-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-flowchart-title">分岐フロー図の最小例</title>
  <desc id="example-flowchart-desc">入力が有効なら保存し、無効なら修正を依頼する。</desc>
  <defs>
    <marker id="example-flowchart-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <path d="M 112 102 V 186" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-flowchart-arrow)"/>
    <path d="M 194 70 H 232 Q 240 70 240 78 V 186" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-flowchart-arrow)"/>
    <text x="90" y="154" text-anchor="middle" font-size="18">
      <tspan x="90" y="154">有効</tspan>
    </text>
    <text x="267" y="142" text-anchor="middle" font-size="18">
      <tspan x="267" y="142">無効</tspan>
    </text>
    <polygon points="112,38 194,70 112,102 30,70" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="112" y="76" text-anchor="middle" font-size="18">
      <tspan x="112" y="76">入力検査</tspan>
    </text>
    <rect x="64" y="186" width="96" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="112.0" y="214.0" text-anchor="middle" font-size="18">
      <tspan x="112.0" y="214.0">保存</tspan>
    </text>
    <rect x="192" y="186" width="96" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="240.0" y="214.0" text-anchor="middle" font-size="18">
      <tspan x="240.0" y="214.0">修正依頼</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-flowchart.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
