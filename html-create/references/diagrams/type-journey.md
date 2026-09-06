# ユーザージャーニー図

## 用途と選択

- 一人の利用者が段階ごとに何を行い、どう感じるかを示す。感情の情報がなければプロセス図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 一人の利用者像、段階、行動、接点、感情の根拠、問題。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 段階を列に置き、感情を高い・やや高い・中立・やや低い・低いの順序尺度でプロットする。
- 下に行動・接点・問題の行を置く。感情線の斜線は許容し、絵文字で代用しない。

## 意味と検証

- 感情を架空の連続数値にしない。観察と仮説を区別し、複数利用者像の感情線を一枚に重ねない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 発見時は期待、入力時は困惑、完了時は安心する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 288" width="320" role="img" aria-labelledby="example-journey-title example-journey-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-journey-title">ユーザージャーニー図の最小例</title>
  <desc id="example-journey-desc">発見時は期待、入力時は困惑、完了時は安心する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <text x="66" y="28" text-anchor="middle" font-size="18">
      <tspan x="66" y="28">発見</tspan>
    </text>
    <text x="160" y="28" text-anchor="middle" font-size="18">
      <tspan x="160" y="28">入力</tspan>
    </text>
    <text x="254" y="28" text-anchor="middle" font-size="18">
      <tspan x="254" y="28">完了</tspan>
    </text>
    <path d="M 66 82 L 160 164 L 254 82" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <circle cx="66" cy="82" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="66" y="112" text-anchor="middle" font-size="18">
      <tspan x="66" y="112">期待</tspan>
    </text>
    <circle cx="160" cy="164" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="160" y="194" text-anchor="middle" font-size="18">
      <tspan x="160" y="194">困惑</tspan>
    </text>
    <circle cx="254" cy="82" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="254" y="112" text-anchor="middle" font-size="18">
      <tspan x="254" y="112">安心</tspan>
    </text>
    <text x="160" y="234" text-anchor="middle" font-size="18">
      <tspan x="160" y="234">高い・低い・高い（順序尺度）</tspan>
    </text>
    <text x="160" y="264" text-anchor="middle" font-size="18">
      <tspan x="160" y="264">例示した感情：仮説</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-journey.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
