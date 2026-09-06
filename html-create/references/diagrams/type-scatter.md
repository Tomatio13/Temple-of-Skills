# 散布図

## 用途と選択

- 二つの定量変数の関係を示す。三つ目の量を面積に割り当てるならバブル型を使う。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 点ごとのx・y、単位、系列、必要なら第三の非負量。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- xとyを各軸の共通尺度で配置する。点を結ばず、混むラベルだけ位置をずらして引出線を使う。
- 点形を系列ごとに区別し、凡例と軸範囲を付ける。

## 意味と検証

- 点を読みやすさのために測定位置から動かさない。相関から因果を断定しない。対数軸なら正の値に限り、軸に方式を明記する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 派生表現

- **バブル型**：第三の非負量を円の面積へ割り当てる。最大量V、最大半径Rに対して `r = R × sqrt(v / V)` とする。半径を量に比例させない。面積の凡例を付け、0の量は正の最小円へ切り上げず、0または別記号と説明する。
- **ビースウォーム型**：一軸の値を保ち、重なる点だけ直交方向にずらす。一点を一観測として、値の軸方向へは動かさない。衝突条件は円中心間距離が半径の和＋余白以上であること。収まらない場合は図高を増やすか分割し、件数を減らして見せない。
- バブルの欠損量を0とみなさない。ビースウォームの横方向の散らばりは新しい測定値ではないと説明する。

## 最小作例

- 工数2・効果3と工数4・効果5の二案を示す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 306" width="320" role="img" aria-labelledby="example-scatter-title example-scatter-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-scatter-title">散布図の最小例</title>
  <desc id="example-scatter-desc">工数2・効果3と工数4・効果5の二案を示す。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="48" y1="228" x2="284" y2="228" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="48" y1="228" x2="48" y2="32" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="36" y="233" text-anchor="end" font-size="18">
      <tspan x="36" y="233">0</tspan>
    </text>
    <text x="36" y="143" text-anchor="end" font-size="18">
      <tspan x="36" y="143">3</tspan>
    </text>
    <text x="36" y="53" text-anchor="end" font-size="18">
      <tspan x="36" y="53">6</tspan>
    </text>
    <text x="30" y="20" text-anchor="middle" font-size="18">
      <tspan x="30" y="20">効果</tspan>
    </text>
    <circle cx="124" cy="138" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="200" cy="78" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="140" y="120" text-anchor="middle" font-size="18">
      <tspan x="140" y="120">案A</tspan>
    </text>
    <text x="218" y="60" text-anchor="middle" font-size="18">
      <tspan x="218" y="60">案B</tspan>
    </text>
    <text x="48" y="252" text-anchor="middle" font-size="18">
      <tspan x="48" y="252">0</tspan>
    </text>
    <text x="124" y="252" text-anchor="middle" font-size="18">
      <tspan x="124" y="252">2</tspan>
    </text>
    <text x="200" y="252" text-anchor="middle" font-size="18">
      <tspan x="200" y="252">4</tspan>
    </text>
    <text x="276" y="252" text-anchor="middle" font-size="18">
      <tspan x="276" y="252">6</tspan>
    </text>
    <text x="260" y="284" text-anchor="middle" font-size="18">
      <tspan x="260" y="284">工数</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-scatter.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
