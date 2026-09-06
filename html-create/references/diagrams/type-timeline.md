# タイムライン

## 用途と選択

- 出来事の日時や間隔を説明する。作業期間はガントチャート、通信順はシーケンス図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 出来事、日時、時間単位、範囲、必要なら時差。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 日時を共通の線形尺度へ変換し、出来事を軸上の点に置く。
- ラベルを上下にずらすか縦向きの軸にし、密集部分は別図に拡大する。軸を省略するときは切れ目を表示する。

## 意味と検証

- 不等間隔の出来事を等間隔にしない。順序だけの図なら「時間間隔は非比例」と明記する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 開始が1日、確認が3日、公開が6日に起きる。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 300" width="320" role="img" aria-labelledby="example-timeline-title example-timeline-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-timeline-title">タイムラインの最小例</title>
  <desc id="example-timeline-desc">開始が1日、確認が3日、公開が6日に起きる。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="60" y1="40" x2="60" y2="260" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="60" cy="40" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="60" cy="128" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="60" cy="260" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="80" y="46" text-anchor="start" font-size="18">
      <tspan x="80" y="46">1日：開始</tspan>
    </text>
    <text x="80" y="134" text-anchor="start" font-size="18">
      <tspan x="80" y="134">3日：確認</tspan>
    </text>
    <text x="80" y="266" text-anchor="start" font-size="18">
      <tspan x="80" y="266">6日：公開</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-timeline.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
