# 組織図

## 用途と選択

- 人・チームの指揮系統、担当、委任を示す。一般的な分類は階層図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 役割・チーム名、直属関係、兼務・助言関係、責任範囲。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 直属関係を主な枝にし、同じ責任段階を揃える。
- 助言・兼務は破線と関係名で区別し、主な報告先と同じ線にしない。個人名より役割を優先できる。

## 意味と検証

- 線が指揮・報告・委任のどれか明記する。共有担当を直属関係として偽装しない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 責任者の下で開発担当と運用担当が分担する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 236" width="320" role="img" aria-labelledby="example-org-chart-title example-org-chart-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-org-chart-title">組織図の最小例</title>
  <desc id="example-org-chart-desc">責任者の下で開発担当と運用担当が分担する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="160" y1="64" x2="160" y2="112" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="76" y1="112" x2="244" y2="112" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="76" y1="112" x2="76" y2="164" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="244" y1="112" x2="244" y2="164" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="96" y="20" width="128" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="48.0">責任者</tspan>
    </text>
    <rect x="20" y="164" width="112" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="76.0" y="192.0" text-anchor="middle" font-size="18">
      <tspan x="76.0" y="192.0">開発担当</tspan>
    </text>
    <rect x="188" y="164" width="112" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="244.0" y="192.0" text-anchor="middle" font-size="18">
      <tspan x="244.0" y="192.0">運用担当</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-org-chart.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
