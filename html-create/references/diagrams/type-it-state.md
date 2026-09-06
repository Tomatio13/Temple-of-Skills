# 現行IT構成図

## 用途と選択

- 既存の情報技術（IT）環境を部門・業務段階で整理する。将来構成は混在させず別図にする。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 部門または段階、現行システム、手作業、入出力、確認時点と未確認事項。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 列を業務段階、領域を部門に割り当てる。ラベル列と段階見出しの幅を先に確保する。
- システムと手作業は名前と形で区別し、受け渡すデータを線の脇に記す。共通基盤は独立した帯に置く。

## 意味と検証

- 確認済みの現状と推測を区別する。存在しない製品・接続を補わない。多い部門は概要と部門別詳細に分ける。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 受付部門の台帳を、経理部門が手動で転記している。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 216" width="320" role="img" aria-labelledby="example-it-state-title example-it-state-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-it-state-title">現行IT構成図の最小例</title>
  <desc id="example-it-state-desc">受付部門の台帳を、経理部門が手動で転記している。</desc>
  <defs>
    <marker id="example-it-state-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <text x="220" y="48" text-anchor="middle" font-size="18">
      <tspan x="220" y="48">受付部門</tspan>
    </text>
    <text x="220" y="156" text-anchor="middle" font-size="18">
      <tspan x="220" y="156">経理部門</tspan>
    </text>
    <line x1="90" y1="64" x2="90" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-it-state-arrow)"/>
    <text x="110" y="104" text-anchor="start" font-size="18">
      <tspan x="110" y="104">手動転記</tspan>
    </text>
    <rect x="24" y="24" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="50.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="50.0">台帳</tspan>
    </text>
    <rect x="24" y="132" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="158.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="158.0">会計</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-it-state.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
