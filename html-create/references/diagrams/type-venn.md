# ベン図

## 用途と選択

- 2〜3集合の共通部分を説明する。厳密な数量比較には棒グラフや表を優先する。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 集合名、共通部分の意味、必要なら集合量と交差量。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 輪郭線を重ねて共通部分を作り、集合名は円の外、共通部分の説明は重なりの内側に置く。
- 小さな交差領域のラベルは引出線で外へ出す。概念図なら面積非比例と明記する。

## 意味と検証

- 数量比例を主張するなら集合面積と交差面積をともに満たす。等しい半径だけで数量を表現したことにしない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 知識と経験が重なる領域を実践として示す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 280" width="320" role="img" aria-labelledby="example-venn-title example-venn-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-venn-title">ベン図の最小例</title>
  <desc id="example-venn-desc">知識と経験が重なる領域を実践として示す。</desc>
  <g fill="var(--mb-ink, #111110)">
    <circle cx="112" cy="132" r="76" fill="none" stroke="var(--mb-ink, #111110)"/>
    <circle cx="208" cy="132" r="76" fill="none" stroke="var(--mb-ink, #111110)"/>
    <text x="90" y="40" text-anchor="middle" font-size="18">
      <tspan x="90" y="40">知識</tspan>
    </text>
    <text x="234" y="40" text-anchor="middle" font-size="18">
      <tspan x="234" y="40">経験</tspan>
    </text>
    <text x="160" y="138" text-anchor="middle" font-size="18">
      <tspan x="160" y="138">実践</tspan>
    </text>
    <text x="160" y="252" text-anchor="middle" font-size="18">
      <tspan x="160" y="252">概念図：面積は数量を表さない</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-venn.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
