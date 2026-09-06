# ツリーマップ

## 用途と選択

- 全体に対する各部分の量を面積で示す。正確な順位比較は棒グラフを選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- カテゴリ階層、非負量、単位、全体量、その他への集約内容。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 長方形全体の面積Aを、値vに対してA×v/Σvで分割する。共通尺度の長方形で隙間なく領域を割り当てる。
- 名前と値を内側へ置き、狭い区画は番号と外側の一覧で結ぶ。

## 意味と検証

- 負数は扱わない。全ゼロなら面積図を描かず「合計0」と表示する。区画を広げて文字を収めない。内側余白を面積比例に含めるか明記し、集約時は対象を開示する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 全12件を甲6、乙4、丙2の面積に分ける。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 288" width="320" role="img" aria-labelledby="example-treemap-title example-treemap-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-treemap-title">ツリーマップの最小例</title>
  <desc id="example-treemap-desc">全12件を甲6、乙4、丙2の面積に分ける。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="16" y="48" width="144" height="216" rx="0" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="160" y="48" width="144" height="144" rx="0" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <rect x="160" y="192" width="144" height="72" rx="0" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="88" y="156" text-anchor="middle" font-size="18">
      <tspan x="88" y="156">甲6</tspan>
    </text>
    <text x="232" y="124" text-anchor="middle" font-size="18">
      <tspan x="232" y="124">乙4</tspan>
    </text>
    <text x="232" y="234" text-anchor="middle" font-size="18">
      <tspan x="232" y="234">丙2</tspan>
    </text>
    <text x="160" y="28" text-anchor="middle" font-size="18">
      <tspan x="160" y="28">合計12件 / 面積比例</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-treemap.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
