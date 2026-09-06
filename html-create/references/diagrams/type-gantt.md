# ガントチャート

## 用途と選択

- 作業の開始・終了・重なりを示す。点の出来事だけならタイムラインを選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- タスク、開始日、終了日、時刻の扱い、依存、節目。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 行をタスク、横を共通の時間軸にする。開始をx、終了との差を幅に変換する。
- 節目は菱形など幅を持たない記号にし、依存線は行間を通す。

## 意味と検証

- 終了が開始より前でないか確認する。日付の両端を含むかを揃える。節目を期間として描かない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 設計が1〜3日、実装が3〜6日に続く。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 250" width="320" role="img" aria-labelledby="example-gantt-title example-gantt-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-gantt-title">ガントチャートの最小例</title>
  <desc id="example-gantt-desc">設計が1〜3日、実装が3〜6日に続く。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="84" y1="48" x2="284" y2="48" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="84" y="30" text-anchor="middle" font-size="18">
      <tspan x="84" y="30">1日</tspan>
    </text>
    <text x="164" y="30" text-anchor="middle" font-size="18">
      <tspan x="164" y="30">3日</tspan>
    </text>
    <text x="284" y="30" text-anchor="middle" font-size="18">
      <tspan x="284" y="30">6日</tspan>
    </text>
    <text x="16" y="98" text-anchor="start" font-size="18">
      <tspan x="16" y="98">設計</tspan>
    </text>
    <text x="16" y="170" text-anchor="start" font-size="18">
      <tspan x="16" y="170">実装</tspan>
    </text>
    <rect x="84" y="76" width="80" height="32" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="164" y="148" width="120" height="32" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="224" text-anchor="middle" font-size="18">
      <tspan x="160" y="224">期間は開始以上・終了未満</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-gantt.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
