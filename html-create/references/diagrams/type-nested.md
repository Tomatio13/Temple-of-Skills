# 包含図

## 用途と選択

- 範囲や入れ子の包含関係を示す。親子関係の枝を読むなら階層図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 外側と内側の集合・範囲、包含関係、各領域名。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 外側から内側へ矩形を描き、各階層の見出し分と余白を確保する。
- 含まれる要素は親の内側へ完全に収める。包含が意味を運ぶため、同じ関係の矢印は足さない。

## 意味と検証

- 枠の重なりを包含と混同しない。部分的な共通部分はベン図を使う。深い入れ子は別図へ分割する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 組織の内側に部門、その内側にチームがある。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 300" width="320" role="img" aria-labelledby="example-nested-title example-nested-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-nested-title">包含図の最小例</title>
  <desc id="example-nested-desc">組織の内側に部門、その内側にチームがある。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="12" y="12" width="296" height="268" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="32" y="42" text-anchor="start" font-size="18">
      <tspan x="32" y="42">組織</tspan>
    </text>
    <rect x="36" y="64" width="248" height="196" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="56" y="94" text-anchor="start" font-size="18">
      <tspan x="56" y="94">部門</tspan>
    </text>
    <rect x="60" y="120" width="200" height="112" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="182.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="182.0">チーム</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-nested.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
