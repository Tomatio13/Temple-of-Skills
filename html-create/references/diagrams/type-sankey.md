# サンキー図

## 用途と選択

- 数量の分岐・合流を帯幅で示す。分岐のない減少は漏斗図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 各流れの量、単位、段階、流入出、損失や増加。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 全図で一つの倍率kを使い、帯幅をk×量にする。各接続に重ならない幅区間を割り当てる。
- 帯は閉じたBezierパスで作り、両制御点のxを列間の中点へ置く。矢印は付けず、段階順で方向を示す。

## 意味と検証

- 節点ごとに流入・流出と量を照合し、損失は独立した流れで示す。小さい帯は拡大・分割または開示した集約で扱い、最小幅への切り上げで量を変えない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 全6件が成功4件と失敗2件へ分かれる。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 324" width="320" role="img" aria-labelledby="example-sankey-title example-sankey-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-sankey-title">サンキー図の最小例</title>
  <desc id="example-sankey-desc">全6件が成功4件と失敗2件へ分かれる。</desc>
  <g fill="var(--mb-ink, #111110)">
    <path d="M 52 56 C 160 56 160 40 268 40 L 268 136 C 160 136 160 152 52 152 Z" fill="var(--mb-rule, #DFDFDF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <path d="M 52 152 C 160 152 160 208 268 208 L 268 256 C 160 256 160 200 52 200 Z" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="40" y="56" width="12" height="144" rx="0" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="268" y="40" width="12" height="96" rx="0" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="268" y="208" width="12" height="48" rx="0" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="48" y="32" text-anchor="middle" font-size="18">
      <tspan x="48" y="32">全6</tspan>
    </text>
    <text x="258" y="24" text-anchor="middle" font-size="18">
      <tspan x="258" y="24">成功4</tspan>
    </text>
    <text x="258" y="192" text-anchor="middle" font-size="18">
      <tspan x="258" y="192">失敗2</tspan>
    </text>
    <text x="160" y="296" text-anchor="middle" font-size="18">
      <tspan x="160" y="296">帯幅：24座標単位 / 件</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-sankey.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
