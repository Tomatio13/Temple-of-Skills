---
name: marp-style-applier
description: Marpスライドデッキにプレゼンテーションデザインスタイルを選択して適用する際に使用するスキルです。
---

# Marp Style Applier

## 概要
ユーザが要望するスタイルを選択し、Marpファイルに適用するようにLLMに指示します。

## ワークフロー

1. スタイルを選択する
以下がサポートしているスタイル一覧です。

| ファイル名 | スタイル | コンセプト |
|-----------|---------|-----------|
| [design_minimal.md](./references/design_minimal.md) | 洗練されたミニマル・ポートフォリオ | プロフェッショナル、建築的、エッジの効いたミニマリズム |
| [design_pop.md](./references/design_pop.md) | ビタミン・ポップ / デジタル・ネオ | Digital Pop × Academic |
| [design_editorial.md](./references/design_editorial.md) | モダン・エディトリアル / ライフスタイル雑誌風 | Kinfolkスタイルの雑誌のような美学 |
| [design_sports_active.md](./references/design_sports_active.md) | スポーツ / アスレチック / エナジー | 情熱的、スピーディ、力強い、競争心 |
| [design_stone_glass.md](./references/design_stone_glass.md) | ストーン＆グラス・マテリアル / 建築的モダン | 静謐、堅牢、未来的、高級感 |
| [design_oneline_adult_chic.md](./references/design_oneline_adult_chic.md) | ワンライン・ドローイング / 大人シック | 知性的、流麗、落ち着き、アーティスティック |
| [design_sculpture_pop.md](./references/design_sculpture_pop.md) | 彫刻ポップアート / ヴェイパーウェイヴ | ヴェイパーウェイヴ ＆ ポップアート・シュルレアリスム |
| **[design_neo_brutalism.md](./references/design_neo_brutalism.md)** | **ネオ・ブルータリズム / デジタル・ブルータリティ** | **意図的なダサさ、生々しいまでの正直さ** |
| **[design_y2k.md](./references/design_y2k.md)** | **Y2K / 2000s / ノスタルジック・フューチャー** | **90s〜00sの楽観的未来、キラキラしたメタル** |
| **[design_paper_collage.md](./references/design_paper_collage.md)** | **ペーパー / コラージュ / アナログ・ハンドメイド** | **紙の質感、手描きの揺らぎ、ハサミで切った断片** |

- ユーザがスタイル名を指定した場合は、そのまま使用する。
- ユーザがイメージや雰囲気を説明した場合は、以下の決定キューを使用して最も近いスタイルにマッピングする。
- 2つのスタイルが近い場合は、上位2つを提案し、編集前に選択を求める。

**決定キュー（キーワード -> スタイル）:**
```
- Minimal, architectural, professional, grid, negative space -> design_minimal
- Pop, neon, digital, academic, energetic, techy -> design_pop
- Editorial, magazine, lifestyle, warm, refined -> design_editorial
- Sports, athletic, speed, power, competition -> design_sports_active
- Stone, glass, material, architectural modern, heavy, luxury -> design_stone_glass
- One-line drawing, adult chic, dusty colors, artistic, calm -> design_oneline_adult_chic
- Sculpture pop, vaporwave, surreal collage -> design_sculpture_pop
- Brutal, brutalism, bold borders, raw, ugly, y2k, retro -> design_neo_brutalism
- Y2K, 2000s, chrome, metallic, bubble, sparkle, retro future -> design_y2k
- Paper, collage, analog, handmade, craft, tape, scrapbook -> design_paper_collage
```

2. 選択した仕様を読み込む
- `references/*.md` 内の対応するファイルを開く。

3. LLMに選択したスタイルを適用するように指示する。

4. LLMに選択したスタイルを適用するように指示した結果を確認する。

## リソース

- `references/*.md`: 詳細なスタイル仕様。
- `design_style_mapping.md`: デザインスタイル対応表。
