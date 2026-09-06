# ストーリーマップ

## 用途と選択

- 利用者の行動順と提供範囲の区切りを示す。状態管理はカンバン、感情はジャーニー図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 一人の利用者像、行動順、利用者に見える成果、初回・次回・後続の範囲。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 横に行動順、縦に提供回の範囲を置く。カードは利用者に見える成果で書く。
- 初回提供の直下に区切り線を引き、初回の範囲を明示する。

## 意味と検証

- 優先度で行動順を並べ替えない。区切りのない一覧や内部作業だけのカードを避ける。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 探す・読むの初回機能を公開し、保存機能は次回に回す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 280" width="320" role="img" aria-labelledby="example-story-map-title example-story-map-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-story-map-title">ストーリーマップの最小例</title>
  <desc id="example-story-map-desc">探す・読むの初回機能を公開し、保存機能は次回に回す。</desc>
  <g fill="var(--mb-ink, #111110)">
    <text x="100" y="28" text-anchor="middle" font-size="18">
      <tspan x="100" y="28">探す</tspan>
    </text>
    <text x="242" y="28" text-anchor="middle" font-size="18">
      <tspan x="242" y="28">読む</tspan>
    </text>
    <rect x="42" y="52" width="116" height="60" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="100.0" y="88.0" text-anchor="middle" font-size="18">
      <tspan x="100.0" y="88.0">検索</tspan>
    </text>
    <rect x="184" y="52" width="116" height="60" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="242.0" y="88.0" text-anchor="middle" font-size="18">
      <tspan x="242.0" y="88.0">本文表示</tspan>
    </text>
    <line x1="16" y1="142" x2="304" y2="142" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <text x="160" y="166" text-anchor="middle" font-size="18">
      <tspan x="160" y="166">初回提供の区切り</tspan>
    </text>
    <rect x="184" y="192" width="116" height="60" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="242.0" y="228.0" text-anchor="middle" font-size="18">
      <tspan x="242.0" y="228.0">保存</tspan>
    </text>
    <text x="78" y="228" text-anchor="middle" font-size="18">
      <tspan x="78" y="228">次回</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-story-map.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
