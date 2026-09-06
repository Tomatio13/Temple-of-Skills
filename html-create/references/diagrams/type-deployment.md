# 配置図

## 用途と選択

- 環境・ホスト・実行単位・複製数を示す。論理的な通信だけなら構成図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 環境、ネットワーク境界、ホスト、配置物と版、複製数、プロトコルとポート。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 環境の枠の内側にホスト、その内側に配置物を入れる。複製は箱の重複ではなく件数で示す。
- 通信線を実行単位へ接続し、プロトコルとポートを空白部分に記す。

## 意味と検証

- 配置物の版と環境を照合する。境界をまたぐ線、配置先、複製数が明確か確認し、未確認値はそのまま示す。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 本番の実行環境にWebサービスv1を2個配置する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 312" width="320" role="img" aria-labelledby="example-deployment-title example-deployment-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-deployment-title">配置図の最小例</title>
  <desc id="example-deployment-desc">本番の実行環境にWebサービスv1を2個配置する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="12" y="12" width="296" height="280" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="38" y="40" text-anchor="start" font-size="18">
      <tspan x="38" y="40">本番環境</tspan>
    </text>
    <rect x="32" y="68" width="256" height="204" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="48" y="100" text-anchor="start" font-size="18">
      <tspan x="48" y="100">実行ホスト</tspan>
    </text>
    <rect x="56" y="128" width="208" height="96" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160.0" y="182.0" text-anchor="middle" font-size="18">
      <tspan x="160.0" y="182.0">Web v1 / 複製2</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-deployment.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
