# 段階別データ品質図

## 用途と選択

- 生データから整形・集計済みデータへの品質段階と利用権限を示す。名称だけの三段図にしない。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 各段階のデータ、変換条件、品質条件、所有者、アクセス主体。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 生・整形・提供の段階を揃え、変換と検査条件を段階間へ置く。
- 各段階に利用者・保存形式を短く記し、権限を持つ対象だけ接続する。

## 意味と検証

- Bronze・Silver・Goldなどの通称は実際の品質条件で説明する。通称からアクセス権を推測しない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 生データを検査して整形し、集計済みデータを提供する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 324" width="320" role="img" aria-labelledby="example-medallion-title example-medallion-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-medallion-title">段階別データ品質図の最小例</title>
  <desc id="example-medallion-desc">生データを検査して整形し、集計済みデータを提供する。</desc>
  <defs>
    <marker id="example-medallion-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <line x1="90" y1="64" x2="90" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-medallion-arrow)"/>
    <text x="110" y="104" text-anchor="start" font-size="18">
      <tspan x="110" y="104">検査</tspan>
    </text>
    <line x1="90" y1="172" x2="90" y2="240" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-medallion-arrow)"/>
    <text x="110" y="212" text-anchor="start" font-size="18">
      <tspan x="110" y="212">集計</tspan>
    </text>
    <rect x="24" y="24" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="50.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="50.0">生データ</tspan>
    </text>
    <rect x="24" y="132" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="158.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="158.0">整形</tspan>
    </text>
    <rect x="24" y="240" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="266.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="266.0">提供</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-medallion.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
