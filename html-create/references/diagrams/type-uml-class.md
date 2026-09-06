# クラス図

## 用途と選択

- 統一モデリング言語（Unified Modeling Language、UML）のクラス・操作・型付き関係を示す。実体と件数だけなら実体関連図を選ぶ。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- クラス、属性、主要操作、継承・実装・所有・関連、多重度。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 箱をクラス名、属性、操作の区画に分ける。高さは内容から決める。
- 継承は実線と白三角、実装は破線と白三角を親側へ向ける。合成は所有側の黒菱形、集約は所有側の白菱形、依存は破線と開矢印。
- 関連には両端の多重度を付ける。通常の矢印マーカーを継承記号に使わない。

## 意味と検証

- 合成と集約のライフサイクルの違いを確認する。操作を省きすぎて実体関連図になっていないか確認する。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 最小作例

- 具体的な保存器が抽象的な保存器を継承し、保存操作を実装する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 312" width="320" role="img" aria-labelledby="example-uml-class-title example-uml-class-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-uml-class-title">クラス図の最小例</title>
  <desc id="example-uml-class-desc">具体的な保存器が抽象的な保存器を継承し、保存操作を実装する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <rect x="48" y="16" width="224" height="80" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="48" y1="56" x2="272" y2="56" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="44" text-anchor="middle" font-size="18">
      <tspan x="160" y="44">保存器</tspan>
    </text>
    <text x="160" y="82" text-anchor="middle" font-size="18">
      <tspan x="160" y="82">+ 保存()</tspan>
    </text>
    <rect x="48" y="208" width="224" height="80" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="48" y1="248" x2="272" y2="248" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="160" y="236" text-anchor="middle" font-size="18">
      <tspan x="160" y="236">具体保存器</tspan>
    </text>
    <text x="160" y="274" text-anchor="middle" font-size="18">
      <tspan x="160" y="274">+ 保存()</tspan>
    </text>
    <line x1="160" y1="208" x2="160" y2="116" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <polygon points="160,96 150,116 170,116" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="200" y="160" text-anchor="middle" font-size="18">
      <tspan x="200" y="160">継承</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-uml-class.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
