# 棒グラフ

## 用途と選択

- カテゴリ別の数量を比較する。長い名称は横棒、二時点の差が主題ならダンベル型を使う。
- 共通の描画・埋め込み規則は [SVG 作図ガイド](../svg-diagrams.md) を使う。

## 必要な情報

- カテゴリ、値、単位、系列名、必要なら比較する二時点。
- 不明な値や関係は推定で補わず、未確認として示すか必要な情報を確認する。

## 配置と描画

- 値vの位置をp=p0+(v-min)/(max-min)×Lで求める。棒はゼロ位置から値の位置まで描き、負数はゼロの反対側へ伸ばす。
- 目盛りと数値ラベルを付ける。カテゴリ間隔を一定にし、積み上げは各区間と合計を照合する。

## 意味と検証

- 棒の軸を途中から切らない。欠損を0にしない。全ゼロは有限の範囲を設定し、0の位置を示す。
- 狭い表示幅では文字を縮める前に縦配置・ラベルの改行・図の分割を行う。データの位置や意味を変える配置変更はしない。

## 派生表現

- **集合棒**：カテゴリ内に系列の棒を並べ、全系列に共通のゼロと尺度を使う。
- **積み上げ棒**：各区間の量と全体量を併記する。異なる基準点から始まる中間区間の厳密な比較には集合棒を使う。
- **ダンベル型**：カテゴリごとに二値を同じ水平軸へ配置し、細線で結ぶ。片方を白丸、もう片方を黒丸にし、両端の実値を表示する。線は差であって途中の経過ではない。
- ダンベルの尺度はゼロを含める。正数のみなら下限0、負数のみなら上限0、正負混在なら両側を含め、全ゼロなら0〜1を使う。欠損端点は補わず欠損と表示する。
- 端点が近接しても距離を引き伸ばさない。点を小さくするか実値を併記する。値ラベルは系列順でなく左右の位置を基準に外側へ置き、端では上へ逃がす。並び順が値・差・固有順のどれか明記する。

## 最小作例

- 甲2、乙4、丙6件を0〜6の同じ尺度で比較する。
- 以下は配置と記号を確認する架空の例。実際の値・名称・関係へ置き換える。同じページに再利用する場合は、すべてのIDと参照を図ごとに変更する。
- SVGを `.mb-figure-frame` に入れ、外側に `figure.mb-figure` と `figcaption` を付ける。完成HTMLへの埋め込み方は共通ガイドを参照する。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 306" width="320" role="img" aria-labelledby="example-bar-title example-bar-desc" style="font-family:var(--mb-font-sans, sans-serif);color:var(--mb-ink, #111110)">
  <title id="example-bar-title">棒グラフの最小例</title>
  <desc id="example-bar-desc">甲2、乙4、丙6件を0〜6の同じ尺度で比較する。</desc>
  <g fill="var(--mb-ink, #111110)">
    <line x1="48" y1="228" x2="284" y2="228" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <line x1="48" y1="228" x2="48" y2="32" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="36" y="233" text-anchor="end" font-size="18">
      <tspan x="36" y="233">0</tspan>
    </text>
    <text x="36" y="143" text-anchor="end" font-size="18">
      <tspan x="36" y="143">3</tspan>
    </text>
    <text x="36" y="53" text-anchor="end" font-size="18">
      <tspan x="36" y="53">6</tspan>
    </text>
    <text x="30" y="20" text-anchor="middle" font-size="18">
      <tspan x="30" y="20">件</tspan>
    </text>
    <rect x="72" y="168" width="40" height="60" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="92" y="156" text-anchor="middle" font-size="18">
      <tspan x="92" y="156">2</tspan>
    </text>
    <text x="92" y="258" text-anchor="middle" font-size="18">
      <tspan x="92" y="258">甲</tspan>
    </text>
    <rect x="148" y="108" width="40" height="120" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="168" y="96" text-anchor="middle" font-size="18">
      <tspan x="168" y="96">4</tspan>
    </text>
    <text x="168" y="258" text-anchor="middle" font-size="18">
      <tspan x="168" y="258">乙</tspan>
    </text>
    <rect x="224" y="48" width="40" height="180" rx="4" fill="var(--mb-surface, #FFFFFF)" stroke="var(--mb-ink, #111110)" stroke-width="1.5"/>
    <text x="244" y="36" text-anchor="middle" font-size="18">
      <tspan x="244" y="36">6</tspan>
    </text>
    <text x="244" y="258" text-anchor="middle" font-size="18">
      <tspan x="244" y="258">丙</tspan>
    </text>
  </g>
</svg>
```

## 出典

- Diagram Design の `type-bar.md` をもとに日本語化・再構成。作例は本統合用に作成。[転用元とライセンス](../diagram-attribution.md)。
