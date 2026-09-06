# 階層図

## 用途と選択

- 単一親を持つ階層・分類を示す。共有依存や循環は依存関係図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 根、親子関係、階層名、末端。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 根を上か左に置き、同じ深さを揃える。兄弟へ分岐する共有幹線は許容し、接続点を明確にする。
- 深さ4、同じ段の子5程度を目安に分割する。矢印なしの枝でも親子関係を読める配置を優先する。

## 意味と検証

- 各子が一つの親に属し、段を飛ばしていないか確認する。省略する枝は件数・対象を明示する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 文書を手順書と解説書に分類する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 236" width="320" role="img" aria-labelledby="example-tree-title example-tree-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-tree-title">階層図の最小例</title>
  <desc id="example-tree-desc">文書を手順書と解説書に分類する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="160" y1="64" x2="160" y2="112" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="76" y1="112" x2="244" y2="112" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="76" y1="112" x2="76" y2="164" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="244" y1="112" x2="244" y2="164" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="96" y="20" width="128" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="48.0">文書</tspan>
    </text>
    <rect x="20" y="164" width="112" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="76.0" y="192.0" text-anchor="middle" font-size="18">
      <tspan x="76.0" y="192.0">手順書</tspan>
    </text>
    <rect x="188" y="164" width="112" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="244.0" y="192.0" text-anchor="middle" font-size="18">
      <tspan x="244.0" y="192.0">解説書</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-tree.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
