# 全体構成図

## 用途と選択

- データ基盤全体の取り込み・処理・保存・提供と実行基盤を俯瞰する。個別接続は統合図へ分ける。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 主要段階、主要サービス、保存先、実行基盤、横断機能。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 段階を主方向に並べ、実行基盤の領域内に主要サービスを置く。
- 共有する認証・監視などは別帯にし、どの領域へ作用するか明記する。

## 意味と検証

- 概要の粒度を揃える。製品名やクラスタを元データにないまま補わない。詳細を省いた場所と別図への対応を示す。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 共通実行基盤に取り込み・保存・提供を配置する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 380" width="320" role="img" aria-labelledby="example-high-level-title example-high-level-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-high-level-title">全体構成図の最小例</title>
  <desc id="example-high-level-desc">共通実行基盤に取り込み・保存・提供を配置する。</desc>
  <defs>
    <marker id="example-high-level-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <rect x="12" y="12" width="296" height="348" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="42" text-anchor="middle" font-size="18">
      <tspan x="160" y="42">共通実行基盤</tspan>
    </text>
    <g transform="translate(66 36)">
      <line x1="90" y1="64" x2="90" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-high-level-arrow)"/>
      <line x1="90" y1="172" x2="90" y2="240" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-high-level-arrow)"/>
      <rect x="24" y="24" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <text x="90.0" y="50.0" text-anchor="middle" font-size="18">
        <tspan x="90.0" y="50.0">取り込み</tspan>
      </text>
      <rect x="24" y="132" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <text x="90.0" y="158.0" text-anchor="middle" font-size="18">
        <tspan x="90.0" y="158.0">保存</tspan>
      </text>
      <rect x="24" y="240" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
      <text x="90.0" y="266.0" text-anchor="middle" font-size="18">
        <tspan x="90.0" y="266.0">提供</tspan>
      </text>
    </g>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-high-level.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
