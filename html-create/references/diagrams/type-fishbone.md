# 特性要因図

## 用途と選択

- 一つの観測結果の原因候補を分類する。事故の時系列はタイムラインを選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 観測された結果、実際の原因分類、個別原因、確認状況。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 主軸の先に結果を置き、分類ごとの骨を約60度の斜線で交互に接続する。
- 小原因は短い水平枝へ付ける。原因数から全体幅を決め、左端の枝・右端の結果に余白を残す。

## 意味と検証

- 斜線はこの図の意味に必要なので許容する。候補と確認済み原因を明記し、根拠なく一つの根本原因を断定しない。結果欄に対策を書かない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 遅延という結果について、負荷と手順の原因候補を調べる。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 346" width="320" role="img" aria-labelledby="example-fishbone-title example-fishbone-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-fishbone-title">特性要因図の最小例</title>
  <desc id="example-fishbone-desc">遅延という結果について、負荷と手順の原因候補を調べる。</desc>
  <defs>
    <marker id="example-fishbone-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <line x1="20" y1="160" x2="220" y2="160" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-fishbone-arrow)"/>
    <line x1="100" y1="160" x2="46.88" y2="68" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="172" y1="160" x2="118.88" y2="252" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="76" y1="118" x2="28" y2="118" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="20" y="100" text-anchor="start" font-size="18">
      <tspan x="20" y="100">混雑</tspan>
    </text>
    <line x1="148" y1="202" x2="100" y2="202" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="94" y="228" text-anchor="middle" font-size="18">
      <tspan x="94" y="228">待機</tspan>
    </text>
    <rect x="20" y="28" width="80" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="60.0" y="54.0" text-anchor="middle" font-size="18">
      <tspan x="60.0" y="54.0">負荷</tspan>
    </text>
    <rect x="84" y="252" width="80" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="124.0" y="278.0" text-anchor="middle" font-size="18">
      <tspan x="124.0" y="278.0">手順</tspan>
    </text>
    <rect x="220" y="136" width="84" height="48" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="262.0" y="166.0" text-anchor="middle" font-size="18">
      <tspan x="262.0" y="166.0">遅延</tspan>
    </text>
    <text x="160" y="322" text-anchor="middle" font-size="18">
      <tspan x="160" y="322">原因候補：未確定</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-fishbone.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
