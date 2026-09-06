# 状態遷移図

## 用途と選択

- 注文・接続・ジョブなどの状態と遷移条件を説明する。処理手順だけなら分岐フロー図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 状態、初期状態、終端、イベント、条件、遷移時の処理。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 状態を角丸矩形、初期点を黒丸、終端を二重丸で描く。
- 線には「イベント [条件] / 処理」を必要な部分だけ付ける。逆方向の遷移と自己ループは外側を通す曲線で分ける。

## 意味と検証

- イベントと遷移先を照合し、自己ループと状態を変える遷移を区別する。到達不能状態は誤りか意図か確認する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 待機から開始イベントで実行に移り、完了で終了する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 232" width="320" role="img" aria-labelledby="example-state-title example-state-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-state-title">状態遷移図の最小例</title>
  <desc id="example-state-desc">待機から開始イベントで実行に移り、完了で終了する。</desc>
  <defs>
    <marker id="example-state-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <circle cx="90" cy="8" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <line x1="90" y1="12" x2="90" y2="24" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-state-arrow)"/>
    <line x1="90" y1="64" x2="90" y2="132" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-state-arrow)"/>
    <text x="110" y="104" text-anchor="start" font-size="18">
      <tspan x="110" y="104">開始</tspan>
    </text>
    <rect x="24" y="24" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="50.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="50.0">待機</tspan>
    </text>
    <rect x="24" y="132" width="132" height="40" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="90.0" y="158.0" text-anchor="middle" font-size="18">
      <tspan x="90.0" y="158.0">実行</tspan>
    </text>
    <line x1="90" y1="172" x2="90" y2="202" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-state-arrow)"/>
    <circle cx="90" cy="210" r="8" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)"/>
    <circle cx="90" cy="210" r="4" fill="var(--mb-ink, #111110)" stroke="var(--mb-ink, #111110)"/>
    <text x="140" y="199" text-anchor="middle" font-size="18">
      <tspan x="140" y="199">完了</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-state.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
