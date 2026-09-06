# データ基盤統合図

## 用途と選択

- データプラットフォーム（DP）の情報源・基盤・利用先と接続方式を示す。時間軸は持たせない。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 情報源、基盤内部の機能、利用先、各接続の方式、共通サービス。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 中央を基盤、両側を情報源と利用先にする。狭い画面では上・中央・下へ変える。
- 各接続のプロトコルを記し、多数の線は異なる接続位置へ分散させる。共通サービスは適用する領域へ接続する。

## 意味と検証

- 個々の接続を一本の太い線へ潰さない。多い場合はデータ・認証・監視などの接続面ごとに分ける。特定製品やアイコンを必須にしない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 情報源からHTTPSで基盤へ取り込み、SQLで利用する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 324" width="320" role="img" aria-labelledby="example-dp-integration-title example-dp-integration-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-dp-integration-title">データ基盤統合図の最小例</title>
  <desc id="example-dp-integration-desc">情報源からHTTPSで基盤へ取り込み、SQLで利用する。</desc>
  <defs>
    <marker id="example-dp-integration-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <line x1="90" y1="64" x2="90" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-dp-integration-arrow)"/>
    <text x="110" y="104" text-anchor="start" font-size="18">
      <tspan x="110" y="104">HTTPS</tspan>
    </text>
    <line x1="90" y1="172" x2="90" y2="240" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-dp-integration-arrow)"/>
    <text x="110" y="212" text-anchor="start" font-size="18">
      <tspan x="110" y="212">SQL</tspan>
    </text>
    <rect x="24" y="24" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="50.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="50.0">情報源</tspan>
    </text>
    <rect x="24" y="132" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="158.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="158.0">基盤</tspan>
    </text>
    <rect x="24" y="240" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="266.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="266.0">利用先</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-dp-integration.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
