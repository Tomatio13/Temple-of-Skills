# レイヤー図

## 用途と選択

- 抽象度・責任・技術の層を示す。大小の順位はピラミッド、包含は包含図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 各層、上位下位の意味、層間の依存、横断機能。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 横帯を縦に積み、ラベルと説明を分ける。上から下の意味を図の説明に書く。
- 横断機能は別の縦帯にし、実際に覆う範囲を明示する。

## 意味と検証

- 層の上下を時系列と誤解させない。隣接するだけで依存を断定せず、必要な関係だけ線で示す。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 表示・業務・保存の責任を三層に分ける。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240" width="320" role="img" aria-labelledby="example-layers-title example-layers-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-layers-title">レイヤー図の最小例</title>
  <desc id="example-layers-desc">表示・業務・保存の責任を三層に分ける。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="40" y="24" width="240" height="56" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="58.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="58.0">表示</tspan>
    </text>
    <rect x="40" y="96" width="240" height="56" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="130.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="130.0">業務</tspan>
    </text>
    <rect x="40" y="168" width="240" height="56" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="202.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="202.0">保存</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-layers.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
