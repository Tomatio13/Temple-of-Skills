# 折れ線グラフ

## 用途と選択

- 連続する時間・順序に沿う値の変化を示す。順位だけなら順位推移、二時点ならスロープ型を使う。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 時点、値、単位、系列、欠損、軸範囲。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 時刻と値をそれぞれ共通尺度で座標へ変換し、観測点をpolylineで結ぶ。
- 不等間隔の時刻を等間隔にしない。欠損区間は線を切り、観測していない滑らかな曲線を加えない。

## 意味と検証

- 絶対量が主題ならゼロを含める。軸を切り詰める場合は範囲と理由を示す。系列間の尺度を揃え、線種と直接ラベルで識別する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 派生表現

- **スロープグラフ**：二時点の値を左右に置き、同じ単位・上下限・線形尺度で結ぶ。端点に系列名と両方の値を付ける。軸範囲を明記すればゼロ以外から開始できる。欠損端点は推定せず、除外した系列を説明する。ラベルだけをずらし、点の座標を変えない。
- **リッジライン**：系列ごとの分布を上下に並べる。全系列で同じx範囲・単位・振幅倍率を使い、`y = baseline - amplitude × density` で描く。系列ごとの最大値で個別正規化しない。ヒストグラムか密度推定か、ビン幅または帯域幅、標本数を明記する。観測範囲の途中を0と偽らず、裾が切れる場合は表示する。
- **順位推移（bump）**：3〜6時点の順位を同じ高さの段へ配置し、1位を上にする。線は量でなく順位を示す。同順位の方式を明記し、同順位の点を勝手に上下へ散らさない。欠測は線を切り、開始・終了で対象が違う場合は参加範囲を説明する。
- 派生型の斜線や分布曲線はデータ表現なので直角へ変形しない。いずれも点の座標を保ち、ラベルの調整と図の分割で混雑を解く。

## 最小作例

- 1日2件、2日4件、3日3件の変化を示す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 306" width="320" role="img" aria-labelledby="example-line-title example-line-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-line-title">折れ線グラフの最小例</title>
  <desc id="example-line-desc">1日2件、2日4件、3日3件の変化を示す。</desc>
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
      <tspan x="30" y="20">件</tspan>
    </text>
    <path d="M 84 168 L 160 108 L 236 138" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="84" cy="168" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="84" y="258" text-anchor="middle" font-size="18">
      <tspan x="84" y="258">1日</tspan>
    </text>
    <text x="84" y="154" text-anchor="middle" font-size="18">
      <tspan x="84" y="154">2</tspan>
    </text>
    <circle cx="160" cy="108" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="160" y="258" text-anchor="middle" font-size="18">
      <tspan x="160" y="258">2日</tspan>
    </text>
    <text x="160" y="94" text-anchor="middle" font-size="18">
      <tspan x="160" y="94">4</tspan>
    </text>
    <circle cx="236" cy="138" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="236" y="258" text-anchor="middle" font-size="18">
      <tspan x="236" y="258">3日</tspan>
    </text>
    <text x="236" y="124" text-anchor="middle" font-size="18">
      <tspan x="236" y="124">3</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-line.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
