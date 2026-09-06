# 構成図

## 用途と選択

- システムの部品と通信・責任境界を説明する。実行ホストや配置が主題なら配置図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 部品名、役割、方向付きの関係、通信内容、境界。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 主要な流れを縦または横に揃え、同じ責任・信頼境界の部品を領域で囲む。領域、線、箱、ラベルの順に描く。
- 主方向に合う辺から接続し、折れ曲がりは半径6〜8の直角経路にする。別の箱を通過しない。

## 意味と検証

- 各矢印の送信元・宛先・意味を照合する。境界は実在するものだけにし、単なる配置用の枠と混同しない。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 利用者が受付に要求し、受付が保存先を読み書きする。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 324" width="320" role="img" aria-labelledby="example-architecture-title example-architecture-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-architecture-title">構成図の最小例</title>
  <desc id="example-architecture-desc">利用者が受付に要求し、受付が保存先を読み書きする。</desc>
  <defs>
    <marker id="example-architecture-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <line x1="90" y1="64" x2="90" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-architecture-arrow)"/>
    <text x="110" y="104" text-anchor="start" font-size="18">
      <tspan x="110" y="104">要求</tspan>
    </text>
    <line x1="90" y1="172" x2="90" y2="240" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-architecture-arrow)"/>
    <text x="110" y="212" text-anchor="start" font-size="18">
      <tspan x="110" y="212">読み書き</tspan>
    </text>
    <rect x="24" y="24" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="50.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="50.0">利用者</tspan>
    </text>
    <rect x="24" y="132" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="158.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="158.0">受付</tspan>
    </text>
    <rect x="24" y="240" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="266.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="266.0">保存先</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-architecture.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
