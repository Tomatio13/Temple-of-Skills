# 実体関連図

## 用途と選択

- 実体関連（Entity Relationship、ER）図は、概念・論理モデルの実体と多重度を示す。物理列と型が主題ならデータベーススキーマ図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 実体、識別子、主な属性、関係、関係両端の最小・最大件数。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 実体名と属性欄を区切り、関連する実体を近くに置く。
- 関係線の両端に1、0..1、0..*、1..*などの多重度を記す。通常の処理方向の矢印で代用しない。

## 意味と検証

- 両端の任意性と多重度を照合する。名称と表記を統一し、概念上の関係を勝手に物理外部キーと断定しない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 顧客1件に注文0件以上が対応し、各注文は顧客1件を持つ。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 236" width="320" role="img" aria-labelledby="example-er-title example-er-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-er-title">実体関連図の最小例</title>
  <desc id="example-er-desc">顧客1件に注文0件以上が対応し、各注文は顧客1件を持つ。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="80" y="20" width="160" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="48.0">顧客</tspan>
    </text>
    <rect x="80" y="166" width="160" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="194.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="194.0">注文</tspan>
    </text>
    <line x1="160" y1="64" x2="160" y2="166" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="180" y="90" text-anchor="start" font-size="18">
      <tspan x="180" y="90">1</tspan>
    </text>
    <text x="180" y="150" text-anchor="start" font-size="18">
      <tspan x="180" y="150">0..*</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-er.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
