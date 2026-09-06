# 役割別データフロー図

## 用途と選択

- 誰がどの段階でデータを作成・加工・利用するかを示す。通信構成だけなら構成図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 役割、段階、処理、データ名と形式、方向、公開範囲。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 行を役割、列を段階にして、処理を交点へ置く。ラベル用の余白を先に確保する。
- 入出力を区別し、役割をまたぐ線に渡すデータを付ける。空セルは空のままにする。

## 意味と検証

- データの出所・加工・利用先が追えるか確認する。線の意味を制御指示と混在させる場合は線種と凡例を分ける。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 収集担当から分析担当へ匿名化済みデータを渡す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 342" width="320" role="img" aria-labelledby="example-data-flow-title example-data-flow-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-data-flow-title">役割別データフロー図の最小例</title>
  <desc id="example-data-flow-desc">収集担当から分析担当へ匿名化済みデータを渡す。</desc>
  <defs>
    <marker id="example-data-flow-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <text x="76" y="24" text-anchor="middle" font-size="18">
      <tspan x="76" y="24">準備</tspan>
    </text>
    <text x="240" y="24" text-anchor="middle" font-size="18">
      <tspan x="240" y="24">利用</tspan>
    </text>
    <g transform="translate(0 32)">
      <rect x="8" y="12" width="304" height="132" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <rect x="8" y="156" width="304" height="132" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <text x="24" y="38" text-anchor="start" font-size="18">
        <tspan x="24" y="38">収集担当</tspan>
      </text>
      <text x="24" y="182" text-anchor="start" font-size="18">
        <tspan x="24" y="182">分析担当</tspan>
      </text>
      <path d="M 128 84 H 152 Q 160 84 160 92 V 222 H 184" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-data-flow-arrow)"/>
      <text x="177" y="138" text-anchor="start" font-size="18">
        <tspan x="177" y="138">匿名データ</tspan>
      </text>
      <rect x="24" y="60" width="104" height="48" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <text x="76.0" y="90.0" text-anchor="middle" font-size="18">
        <tspan x="76.0" y="90.0">匿名化</tspan>
      </text>
      <rect x="184" y="198" width="112" height="48" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <text x="240.0" y="228.0" text-anchor="middle" font-size="18">
        <tspan x="240.0" y="228.0">分析</tspan>
      </text>
    </g>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-data-flow.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
