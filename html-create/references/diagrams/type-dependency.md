# 依存関係図

## 用途と選択

- 共有依存や循環を持つ構造を示す。単一親で循環がなければ階層図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- モジュール、依存先、外部依存の版、循環、入次数。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 依存する側を上、依存先を下の段に置く。矢印の意味を「依存する」と明示する。
- 共有依存への線は接続位置を分ける。循環の戻り線は外周を通し、循環とラベル付けする。

## 意味と検証

- 入次数は実際の依存辺から数える。複数循環がある場合は省略を開示し、対象別に分割する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 画面とバッチが共通部品に依存する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 312" width="320" role="img" aria-labelledby="example-dependency-title example-dependency-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-dependency-title">依存関係図の最小例</title>
  <desc id="example-dependency-desc">画面とバッチが共通部品に依存する。</desc>
  <defs>
    <marker id="example-dependency-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <path d="M 76 64 V 120 Q 76 128 84 128 H 136 V 184" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-dependency-arrow)"/>
    <path d="M 244 64 V 136 Q 244 144 236 144 H 184 V 184" fill="none" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-dependency-arrow)"/>
    <rect x="20" y="20" width="112" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="76.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="76.0" y="48.0">画面</tspan>
    </text>
    <rect x="188" y="20" width="112" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="244.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="244.0" y="48.0">バッチ</tspan>
    </text>
    <rect x="96" y="184" width="128" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="212.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="212.0">共通部品</tspan>
    </text>
    <text x="160" y="258" text-anchor="middle" font-size="18">
      <tspan x="160" y="258">依存する側から依存先へ</tspan>
    </text>
    <text x="160" y="286" text-anchor="middle" font-size="18">
      <tspan x="160" y="286">共通部品への依存数：2</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-dependency.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
