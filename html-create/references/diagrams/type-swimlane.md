# スイムレーン図

## 用途と選択

- 担当者・部門をまたぐ手順と引き渡しを示す。データの役割と形式が主題ならデータフロー図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 担当、各処理の所有者、順序、引き渡し条件。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 担当ごとにレーンを作り、処理を所有者のレーン内に置く。
- 主方向に時間が進むように配置し、レーンをまたぐ線に引き渡し内容を付ける。

## 意味と検証

- 処理を2レーンにまたがせない。共同作業は主担当と協力関係を明記する。レーンごとの処理数を揃えるために架空の処理を加えない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 申請者の申請を担当者が確認する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 310" width="320" role="img" aria-labelledby="example-swimlane-title example-swimlane-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-swimlane-title">スイムレーン図の最小例</title>
  <desc id="example-swimlane-desc">申請者の申請を担当者が確認する。</desc>
  <defs>
    <marker id="example-swimlane-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <rect x="8" y="12" width="304" height="132" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="8" y="156" width="304" height="132" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="24" y="38" text-anchor="start" font-size="18">
      <tspan x="24" y="38">申請者</tspan>
    </text>
    <text x="24" y="182" text-anchor="start" font-size="18">
      <tspan x="24" y="182">担当者</tspan>
    </text>
    <path d="M 128 84 H 152 Q 160 84 160 92 V 222 H 184" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-swimlane-arrow)"/>
    <text x="177" y="138" text-anchor="start" font-size="18">
      <tspan x="177" y="138">申請書</tspan>
    </text>
    <rect x="24" y="60" width="104" height="48" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="76.0" y="90.0" text-anchor="middle" font-size="18">
      <tspan x="76.0" y="90.0">申請</tspan>
    </text>
    <rect x="184" y="198" width="112" height="48" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="240.0" y="228.0" text-anchor="middle" font-size="18">
      <tspan x="240.0" y="228.0">確認</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-swimlane.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
