# 極座標チャート

## 用途と選択

- 周期カテゴリごとの一つの非負量を、放射状の棒・点で示す。多基準の系列比較はレーダーを選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 周期順のカテゴリ、非負値、単位、共通上限。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 角度はカテゴリ順、半径r=R×v/Sは数量に対応させる。中心からの線と終点の点で示し、同心円に目盛りを付ける。
- 放射状ロリポップを既定とし、点を多角形で結ばない。等角扇形の面積で量を示す場合は別方式と明記してr=R×sqrt(v/S)を使う。

## 意味と検証

- 負数を外向き半径に変換しない。全ゼロでは上限1など有限の尺度を取り、中心に0を示す。カテゴリを量の大小で並べ替えて周期を壊さない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 朝2、昼4、夜6を0〜6の半径で示す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 316" width="320" role="img" aria-labelledby="example-polar-title example-polar-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-polar-title">極座標チャートの最小例</title>
  <desc id="example-polar-desc">朝2、昼4、夜6を0〜6の半径で示す。</desc>
  <g fill="var(--mb-ink, #111110)">
    <circle cx="160" cy="156" r="44" fill="none" stroke="var(--mb-rule, #DFDFDF)"/>
    <circle cx="160" cy="156" r="88" fill="none" stroke="var(--mb-rule, #DFDFDF)"/>
    <line x1="160" y1="156" x2="160.0" y2="68.0" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <line x1="160" y1="156" x2="160.0" y2="126.67" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="160.0" cy="126.67" r="5" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="160.0" y="43.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="43.0">朝2</tspan>
    </text>
    <line x1="160" y1="156" x2="236.21" y2="200.0" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <line x1="160" y1="156" x2="210.81" y2="185.33" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="210.81" cy="185.33" r="5" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="262.19" y="220.0" text-anchor="middle" font-size="18">
      <tspan x="262.19" y="220.0">昼4</tspan>
    </text>
    <line x1="160" y1="156" x2="83.79" y2="200.0" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <line x1="160" y1="156" x2="83.79" y2="200.0" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="83.79" cy="200.0" r="5" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="57.81" y="220.0" text-anchor="middle" font-size="18">
      <tspan x="57.81" y="220.0">夜6</tspan>
    </text>
    <text x="160" y="290" text-anchor="middle" font-size="18">
      <tspan x="160" y="290">尺度：0〜6 / 中間目盛り：3</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-polar.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
