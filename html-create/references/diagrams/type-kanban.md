# カンバン図

## 用途と選択

- 作業の現在状態と仕掛かり数を示す。処理の矢印が必要ならスイムレーン図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 状態、カード、進行中作業数（Work in Progress、WIP）の上限、阻害要因、確認時点。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 列を状態にし、カードを一つの列だけに置く。列見出しに件数と進行中列の上限を記す。
- 阻害されたカードに理由を付け、超過は「上限超過」と文字で示す。接続線は描かない。

## 意味と検証

- 件数を実カード数から数える。未設定の上限は捏造せず未設定と記す。完了列と待ち列には上限を強制しない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 実施中が2件で上限1件を超え、一件が確認待ち。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 332" width="320" role="img" aria-labelledby="example-kanban-title example-kanban-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-kanban-title">カンバン図の最小例</title>
  <desc id="example-kanban-desc">実施中が2件で上限1件を超え、一件が確認待ち。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="12" y="12" width="140" height="300" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="168" y="12" width="140" height="300" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="82" y="40" text-anchor="middle" font-size="18">
      <tspan x="82" y="40">実施中 2/1</tspan>
    </text>
    <text x="238" y="40" text-anchor="middle" font-size="18">
      <tspan x="238" y="40">完了 0</tspan>
    </text>
    <rect x="24" y="64" width="116" height="60" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="82.0" y="100.0" text-anchor="middle" font-size="18">
      <tspan x="82.0" y="100.0">原稿作成</tspan>
    </text>
    <rect x="24" y="140" width="116" height="92" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="82" y="170" text-anchor="middle" font-size="18">
      <tspan x="82" y="170">確認待ち</tspan>
    </text>
    <text x="82" y="264" text-anchor="middle" font-size="18">
      <tspan x="82" y="264">上限超過</tspan>
    </text>
    <text x="82" y="202" text-anchor="middle" font-size="18">
      <tspan x="82" y="202">阻害：承認</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-kanban.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
