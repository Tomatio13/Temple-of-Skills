<p align="center">
  <h1>PPTX Basic Generator</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
</p>

<p align="center">
  日本企業向けハイデザインPowerPointプレゼンテーション生成システム
</p>

---

## 📖 概要

`pptx-basic-generator`は、設定ファイルを編集するだけでプロフェッショナルな品質のPowerPoint資料を自動生成するPythonツールです。12種類のテンプレートを備え、日本のビジネスシーンに適した青×白の洗練されたデザインをテーマとして採用しています。

## ✨ 特徴

- **12種類のテンプレート** - 表紙、目次、グラフ、テーブル、カード、タイムラインなど
- **簡単な3ステップ操作** - 設定編集から実行までの手順がシンプル
- **可変コンテンツ対応** - 箇条書き、グラフ、テーブルのデータサイズに応じて自動調整
- **日本企業向けデザイン** - メイリオフォント、コーポレートブルーのカラースキーム
- **python-pptxベース** - PowerPointファイルを直接生成

## 📦 インストール

### 依存関係

- Python 3.x
- python-pptx

### セットアップ

```bash
# 仮想環境の作成
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# または .venv\Scripts\activate  # Windows

# パッケージのインストール
python -m pip install --upgrade pip
python -m pip install python-pptx
```

## 🚀 使い方

### 基本的なワークフロー

1. **`SLIDES_TO_USE` でスライド構成を決める**

   使用したいテンプレート番号を配列で指定します。順序が反映され、同じ番号の複数回使用も可能です。

   ```python
   SLIDES_TO_USE = [1, 2, 3, 4, 5, 1]
   # 表紙(1) → 目次(2) → 棒グラフ(3) → 円グラフ(4) → テーブル(5) → 表紙(1)
   ```

2. **`SLIDE_CONTENT` でテキスト内容を編集**

   キーは出力順（1始まり）で指定します。

   ```python
   SLIDE_CONTENT = {
       1: {"title": "表紙タイトル", "subtitle": "...", "credit": "..."},
       2: {"title": "目次", "items": ["項目1", "項目2", ...]},
       3: {"title": "売上推移", "categories": [...], "series": [...], ...},
   }
   ```

3. **実行**

   ```bash
   python scripts/basic_generator.py
   ```

   `outputs/basic_generator.pptx` が生成されます。

## 📋 テンプレート一覧

| ID | テンプレート名 | 必須キー | 説明 |
|----|----------------|----------|------|
| 1 | 表紙 | `title`, `subtitle`, `credit` | タイトルスライド |
| 2 | 目次（リスト） | `title`, `subtitle`, `items[]` | 箇条書きリスト |
| 3 | 左グラフ・右テキスト | `title`, `categories[]`, `series[]`, `text_items[]` | 棒グラフ |
| 4 | 左テキスト・右グラフ | `title`, `categories[]`, `series[]`, `text_items[]` | 円グラフ |
| 5 | 左テーブル・右テキスト | `title`, `columns[]`, `rows[][]`, `text_items[]` | テーブル |
| 6 | 左テキスト・右グラフ | `title`, `categories[]`, `series[]`, `text_items[]` | 折れ線グラフ |
| 7 | カードグリッド | `title`, `subtitle`, `items[]` | 4枚カードレイアウト |
| 8 | 左テキスト・右画像 | `title`, `subtitle`, `text_items[]` | 画像プレースホルダー |
| 9 | 3ポイント（丸囲み） | `title`, `subtitle`, `items[]` | 3項目固定レイアウト |
| 10 | ポイントリスト（コンパクト） | `title`, `subtitle`, `items[]` | 最大4項目 |
| 11 | ポイントリスト（大） | `items[]` | 最大3項目 |
| 12 | タイムライン | `title`, `subtitle`, `timeline_items[]` | 最大4項目 |

詳細なスキーマは [`references/template-map.md`](references/template-map.md) を参照してください。

## 💡 データ構造の例

### グラフ（棒/折れ線）

```python
{
    "categories": ["Q1", "Q2", "Q3", "Q4"],
    "series": [
        {"name": "2024年", "values": [100, 120, 140, 160]},
        {"name": "2025年", "values": [110, 130, 150, 170]}
    ],
    "chart_type": "COLUMN_CLUSTERED"  # or "LINE"
}
```

### グラフ（円）

```python
{
    "categories": ["A社", "B社", "C社", "その他"],
    "series": [
        {"name": "シェア", "values": [35, 25, 20, 20]}
    ],
    "chart_type": "PIE"
}
```

### テーブル

```python
{
    "columns": ["項目", "2023年", "2024年"],
    "rows": [
        ["売上", "100億", "120億"],
        ["利益", "10億", "15億"]
    ]
}
```

## 📁 プロジェクト構造

```
pptx-basic-generator/
├── SKILL.md                    # スキル定義ファイル
├── README.md                   # 本ファイル
├── scripts/
│   └── basic_generator.py      # メインスクリプト
├── agents/
│   └── openai.yaml             # OpenAI エージェント設定
├── references/
│   └── template-map.md         # テンプレートスキーマ詳細
└── outputs/                    # 生成ファイル出力先
    └── basic_generator.pptx
```

## 🔧 トラブルシュート

| エラー | 原因 | 対策 |
|--------|------|------|
| `Template not found` | テンプレート名不一致 | `SLIDE_TEMPLATES[slide_id]["template"]` が存在するか確認 |
| 内容が空・一部欠落 | キー不一致 | `SLIDE_CONTENT` キーが `output_index` になっているか確認 |
| グラフ描画不良 | データ長不一致 | `values` 長が `categories` と一致するか確認 |
| テーブル生成エラー | 列数不一致 | 各行の列数が `columns` 数と一致するか確認 |

## 🎨 デザインテーマ

### Modern Japan Theme（デフォルト）

- **カラースキーム**: 青×白
  - Primary: `#00529B`（コーポレートブルー）
  - Secondary: `#0072C6`（アクセントブルー）
  - Accent: `#418FDE`（ライトブルー）
- **フォント**: メイリオ（日本語）/ Segoe UI（英語）

## 謝辞
本SKillは、まつにぃ(@yugen_matuni)さんが公開して下さったPythonコードをベースにして作成しています。
公開してくださりありがとうございます。
[Python1つでPPTXが作成できる方法](https://note.com/yugen_matuni/n/ndbd3cc5cff90)

## 📄 ライセンス

MIT License

## 🤝 貢献

バグ報告や機能リクエストはIssueにてお願いいたします。
