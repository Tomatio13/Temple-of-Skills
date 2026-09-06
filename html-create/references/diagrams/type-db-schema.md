# データベーススキーマ図

## 用途と選択

- 実テーブルの列・型・制約・外部キーをレビューする。概念モデルは実体関連図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- スキーマ名、テーブル名、列、型、制約、対象の索引、外部キーと削除時動作。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- テーブルを見出しと列行に分け、行高を揃える。主キー（PK）、外部キー（FK）、一意（UQ）、非NULL（NN）を必要な行だけ表示する。
- 外部キーは参照元の列行から参照先の列行へ接続し、参照先とON DELETE動作を記す。索引は別区画に置く。

## 意味と検証

- 列を省くときは省略数を明記する。型・制約・削除時動作が不明なら未確認と書き、推測で補わない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- orders.customer_idがcustomers.idを参照し、削除を制限する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 356" width="320" role="img" aria-labelledby="example-db-schema-title example-db-schema-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-db-schema-title">データベーススキーマ図の最小例</title>
  <desc id="example-db-schema-desc">orders.customer_idがcustomers.idを参照し、削除を制限する。</desc>
  <defs>
    <marker id="example-db-schema-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <rect x="20" y="16" width="280" height="92" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="20" y1="52" x2="300" y2="52" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="42" text-anchor="middle" font-size="18">
      <tspan x="160" y="42">customers</tspan>
    </text>
    <text x="36" y="84" text-anchor="start" font-size="18">
      <tspan x="36" y="84">id: int PK</tspan>
    </text>
    <rect x="20" y="220" width="280" height="112" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="20" y1="256" x2="300" y2="256" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="246" text-anchor="middle" font-size="18">
      <tspan x="160" y="246">orders</tspan>
    </text>
    <text x="36" y="290" text-anchor="start" font-size="18">
      <tspan x="36" y="290">customer_id: int FK</tspan>
    </text>
    <path d="M 300 284 H 310 V 78 H 300" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-db-schema-arrow)"/>
    <text x="148" y="148" text-anchor="middle" font-size="18">
      <tspan x="148" y="148">参照先：customers.id</tspan>
    </text>
    <text x="148" y="174" text-anchor="middle" font-size="18">
      <tspan x="148" y="174">ON DELETE RESTRICT</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-db-schema.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
