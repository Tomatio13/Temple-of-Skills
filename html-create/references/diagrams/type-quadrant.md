# 四象限図

## 用途と選択

- 二つの軸による位置付け・優先順位・シナリオ比較に使う。定量の相関なら散布図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 軸の意味と方向、分類境界、対象の位置、判断根拠。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 二軸の交点を決め、軸端に意味を記す。項目は点と短い直接ラベルで示す。
- シナリオ型では点を置かず、四つの領域に名前と説明を置く。

## 意味と検証

- 位置が測定値か判断かを示す。境界上の項目を無断で移動しない。二軸で意味が変わらない重複概念を選ばない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## シナリオ型の使い方

- 四つの領域を同じ二軸で定義し、それぞれに具体的なシナリオ名を付ける。
- 領域には説明を置き、点の座標や面積で量を表さない。軸の意味と各領域の説明が一致するか確認する。
- ページ独自の書体・背景・色は追加せず、共通の白地と黒線を使う。

## 最小作例

- 効果と工数の二軸に改善案を置く。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 280" width="320" role="img" aria-labelledby="example-quadrant-title example-quadrant-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-quadrant-title">四象限図の最小例</title>
  <desc id="example-quadrant-desc">効果と工数の二軸に改善案を置く。</desc>
  <defs>
    <marker id="example-quadrant-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <line x1="44" y1="228" x2="292" y2="228" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-quadrant-arrow)"/>
    <line x1="44" y1="228" x2="44" y2="32" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-quadrant-arrow)"/>
    <line x1="168" y1="56" x2="168" y2="228" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <line x1="44" y1="138" x2="276" y2="138" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <text x="44" y="20" text-anchor="middle" font-size="18">
      <tspan x="44" y="20">効果</tspan>
    </text>
    <text x="270" y="256" text-anchor="middle" font-size="18">
      <tspan x="270" y="256">工数</tspan>
    </text>
    <circle cx="100" cy="96" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="104" y="78" text-anchor="middle" font-size="18">
      <tspan x="104" y="78">改善案</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-quadrant.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
