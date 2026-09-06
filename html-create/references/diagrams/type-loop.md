# 循環図

## 用途と選択

- 最終段階が最初へ戻り、中央に蓄積する状態がある循環を示す。単なる繰り返し条件はフロー図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 循環の段階、向き、中央に蓄積する状態、段階と中央の関係。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 段階を同じ半径の円上に配置し、中央に蓄積状態を置く。円周上の弧で次の段階へ接続する。
- 弧と箱の交点で経路を切り、矢印先端を次の箱の辺へ合わせる。中央への補助線は循環線と区別する。

## 意味と検証

- 最後から最初への接続を確認する。中央を通る循環矢印や、箱の中心で終わる矢印を避ける。実用図は5〜8段階を目安にし、最小例は幾何の説明用とする。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 観察・改善・実行が循環して知識を蓄積する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 310" width="320" role="img" aria-labelledby="example-loop-title example-loop-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-loop-title">循環図の最小例</title>
  <desc id="example-loop-desc">観察・改善・実行が循環して知識を蓄積する。</desc>
  <defs>
    <marker id="example-loop-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <path d="M 208.00 76.86 A 96 96 0 0 1 251.83 188.00" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-loop-arrow)"/>
    <path d="M 227.76 228.00 A 96 96 0 0 1 92.24 228.00" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-loop-arrow)"/>
    <path d="M 68.17 188.00 A 96 96 0 0 1 112.00 76.86" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-loop-arrow)"/>
    <rect x="112" y="44" width="96" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="70.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="70.0">観察</tspan>
    </text>
    <rect x="195.14" y="188" width="96" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="243.14" y="214.0" text-anchor="middle" font-size="18">
      <tspan x="243.14" y="214.0">改善</tspan>
    </text>
    <rect x="28.86" y="188" width="96" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="76.86" y="214.0" text-anchor="middle" font-size="18">
      <tspan x="76.86" y="214.0">実行</tspan>
    </text>
    <rect x="116" y="134" width="88" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="162.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="162.0">知識</tspan>
    </text>
    <text x="160" y="286" text-anchor="middle" font-size="18">
      <tspan x="160" y="286">蓄積状態を中心に置く</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-loop.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
