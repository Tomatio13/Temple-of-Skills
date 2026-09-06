# ピラミッド・漏斗図

## 用途と選択

- 階層的重要度や基礎から頂点を示す。漏斗は段階ごとの残存人数を示す。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 段階、上下の意味、漏斗なら各段の件数と母数。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 概念ピラミッドは台形を積み、幅が定量を表さないことを示す。
- 数量漏斗は同じ尺度で幅を件数に比例させ、段ごとの件数・率を記す。等幅の段を見栄えだけで縮めない。

## 意味と検証

- 数量と概念の二方式を混ぜない。流入で件数が増えるなら理由を示し、漏斗の形に合わせて値を変えない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 基礎の上に応用、さらに専門を積み重ねる概念図。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 280" width="320" role="img" aria-labelledby="example-pyramid-title example-pyramid-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-pyramid-title">ピラミッド・漏斗図の最小例</title>
  <desc id="example-pyramid-desc">基礎の上に応用、さらに専門を積み重ねる概念図。</desc>
  <g fill="var(--mb-ink, #111110)">
    <polygon points="160,20 208,84 112,84" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <polygon points="112,84 208,84 256,148 64,148" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <polygon points="64,148 256,148 304,212 16,212" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="68" text-anchor="middle" font-size="18">
      <tspan x="160" y="68">専門</tspan>
    </text>
    <text x="160" y="124" text-anchor="middle" font-size="18">
      <tspan x="160" y="124">応用</tspan>
    </text>
    <text x="160" y="188" text-anchor="middle" font-size="18">
      <tspan x="160" y="188">基礎</tspan>
    </text>
    <text x="160" y="252" text-anchor="middle" font-size="18">
      <tspan x="160" y="252">幅は数量を表さない</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-pyramid.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
