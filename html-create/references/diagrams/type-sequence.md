# シーケンス図

## 用途と選択

- 複数の参加者の時系列メッセージを示す。状態そのものの変化は状態遷移図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- 参加者、メッセージ順、要求と応答、条件、同期・非同期の別。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 参加者を上に並べ、下へ伸びる破線を生存線とする。時間は下へ進み、メッセージは水平に描く。
- 要求は実線と塗り矢印、応答は破線と塗り矢印、非同期通知は破線と開いた矢印で区別し凡例を付ける。
- 分岐はalt、任意処理はopt、反復はloopの枠にまとめ、条件とメッセージを離す。活性区間は細い矩形で示す。

## 意味と検証

- 参加者は5以内を目安に分割する。応答先、時間順、自己呼び出し、枠の参加範囲を照合する。通信の線と生存線の交点は許容する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 利用者が受付に要求を送り、受付が結果を返す。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 264" width="320" role="img" aria-labelledby="example-sequence-title example-sequence-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-sequence-title">シーケンス図の最小例</title>
  <desc id="example-sequence-desc">利用者が受付に要求を送り、受付が結果を返す。</desc>
  <defs>
    <marker id="example-sequence-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="var(--mb-ink, #111110)"/>
    </marker>
  </defs>
  <g fill="var(--mb-ink, #111110)">
    <line x1="68" y1="64" x2="68" y2="242" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <line x1="252" y1="64" x2="252" y2="242" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4"/>
    <line x1="68" y1="112" x2="252" y2="112" stroke="var(--mb-ink, #111110)" stroke-width="1.5" marker-end="url(#example-sequence-arrow)"/>
    <text x="160" y="98" text-anchor="middle" font-size="18">
      <tspan x="160" y="98">要求</tspan>
    </text>
    <line x1="252" y1="192" x2="68" y2="192" stroke="var(--mb-ink, #111110)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#example-sequence-arrow)"/>
    <text x="160" y="178" text-anchor="middle" font-size="18">
      <tspan x="160" y="178">結果</tspan>
    </text>
    <rect x="20" y="20" width="96" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="68.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="68.0" y="48.0">利用者</tspan>
    </text>
    <rect x="204" y="20" width="96" height="44" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="252.0" y="48.0" text-anchor="middle" font-size="18">
      <tspan x="252.0" y="48.0">受付</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-sequence.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
