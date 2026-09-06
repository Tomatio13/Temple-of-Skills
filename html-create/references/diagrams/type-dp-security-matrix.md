# データ基盤権限マトリクス

## 用途と選択

- 役割と対象の交点ごとの権限を説明する。関係線や処理順は使わない。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 役割・グループ、対象、各交点の実権限、確認時点。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 列を役割、行を対象にし、各セルに管理・読み書き・読取・不可などの実際の権限を書く。
- 色でなく文字を主情報にする。ロール名と対象名が長い場合は改行や役割ごとの分割を行う。

## 意味と検証

- 空欄を拒否とみなさず、不明と明示する。readなどの分類とSELECTなどの実際の操作権限を区別する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 管理者は保存先を管理でき、利用者は読取のみ可能。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 210" width="320" role="img" aria-labelledby="example-dp-security-matrix-title example-dp-security-matrix-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-dp-security-matrix-title">データ基盤権限マトリクスの最小例</title>
  <desc id="example-dp-security-matrix-desc">管理者は保存先を管理でき、利用者は読取のみ可能。</desc>
  <g fill="var(--mb-ink, #111110)">
    <text x="190" y="36" text-anchor="middle" font-size="18">
      <tspan x="190" y="36">管理者</tspan>
    </text>
    <text x="266" y="36" text-anchor="middle" font-size="18">
      <tspan x="266" y="36">利用者</tspan>
    </text>
    <text x="50" y="102" text-anchor="middle" font-size="18">
      <tspan x="50" y="102">保存先</tspan>
    </text>
    <rect x="150" y="64" width="76" height="64" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="188.0" y="102.0" text-anchor="middle" font-size="18">
      <tspan x="188.0" y="102.0">管理</tspan>
    </text>
    <rect x="234" y="64" width="76" height="64" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="272.0" y="102.0" text-anchor="middle" font-size="18">
      <tspan x="272.0" y="102.0">読取</tspan>
    </text>
    <text x="160" y="182" text-anchor="middle" font-size="18">
      <tspan x="160" y="182">権限は文字で明示する</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-dp-security-matrix.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
