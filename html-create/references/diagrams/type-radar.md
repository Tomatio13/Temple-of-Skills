# レーダーチャート

## 用途と選択

- 同じ尺度へ正規化した複数の定量基準を比較する。値を精密に比べるなら表や棒グラフを選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 3〜5軸の値、単位、正規化式、尺度上限、系列名。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 角度θ=-π/2+2πi/N、半径r=R×v/Sとして、x=cx+r cosθ、y=cy+r sinθで頂点を求める。
- ゼロ中心から共通目盛りの多角形を描く。系列を実線・破線・点形で区別し、重なるなら図を分ける。

## 意味と検証

- 軸ごとの単位・方向を揃えて正規化する。面積を総合点と解釈しない。軸順を比較図間で変えない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 速度8、保守6、費用4を0〜10に正規化して示す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 316" width="320" role="img" aria-labelledby="example-radar-title example-radar-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-radar-title">レーダーチャートの最小例</title>
  <desc id="example-radar-desc">速度8、保守6、費用4を0〜10に正規化して示す。</desc>
  <g fill="var(--mb-ink, #111110)">
    <polygon points="160.00,112.00 198.11,178.00 121.89,178.00" fill="none" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <polygon points="160.00,68.00 236.21,200.00 83.79,200.00" fill="none" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <line x1="160" y1="156" x2="160.0" y2="68.0" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <text x="160.0" y="43.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="43.0">速度8</tspan>
    </text>
    <line x1="160" y1="156" x2="236.21" y2="200.0" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <text x="262.19" y="220.0" text-anchor="middle" font-size="18">
      <tspan x="262.19" y="220.0">保守6</tspan>
    </text>
    <line x1="160" y1="156" x2="83.79" y2="200.0" stroke="var(--mb-rule, #DFDFDF)" stroke-width="1.5"/>
    <text x="57.81" y="220.0" text-anchor="middle" font-size="18">
      <tspan x="57.81" y="220.0">費用4</tspan>
    </text>
    <polygon points="160.00,85.60 205.73,182.40 129.52,173.60" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="160.0" cy="85.6" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="205.73" cy="182.4" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="129.52" cy="173.6" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="160" y="290" text-anchor="middle" font-size="18">
      <tspan x="160" y="290">尺度：0〜10 / 中間目盛り：5</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-radar.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
