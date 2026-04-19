---
name: rakuten-travel-vacancy-skill
description: |
  楽天トラベル前提で、場所・日付・人数を含む宿泊条件から空室や宿泊プランを検索したいときに使う。
  旅行条件を自然文または構造化入力で受け取り、地区コードを解決して VacantHotelSearch を呼び出し、候補ホテルを日本語で返す。
---

# 楽天トラベル空室検索スキル

## 使うタイミング

- 「楽天トラベルで空室を探して」
- 「京都で 2026-05-01 から 1 泊 2 名の空室を探して」
- 「函館の禁煙・朝食付きホテルを調べて」
- 楽天トラベル前提で、場所・日付・人数を含む宿泊条件から空室や宿泊プランを探したいとき

## 必須前提

- 実行には `RAKUTEN_APPLICATION_ID` が必須
- 環境によっては `RAKUTEN_ACCESS_KEY` も必須
- 未設定時は検索を開始せず、不足している設定を明示する

## Setup

実行前に、このスキルのディレクトリに `.venv` があるか確認する。

無ければ先に作成して有効化する:

```bash
test -d .venv || python -m venv .venv
. .venv/bin/activate
```

次に、このスキルで必要な Python 依存を入れる:

```bash
pip install requests
```

このスキルは `.env` に認証情報を置く前提で使う。

```bash
set -a
. ./.env
set +a
```

```bash
RAKUTEN_APPLICATION_ID=your-application-id
RAKUTEN_ACCESS_KEY=your-access-key
RAKUTEN_AFFILIATE_ID=your-affiliate-id
```

このスキルはビルド不要で、通常は次のように実行する:

```bash
PYTHONPATH=src python -m rakuten_travel_skill.cli "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
```

## 入力ルール

- 必須: `場所`, `チェックイン日`, `チェックアウト日`, `人数`
- 任意: `室数`, `価格帯`, `禁煙`, `朝食`, `夕食`, `温泉`
- CLI専用: `--page`, `--hits`, `--max-pages`, `--search-pattern`
- 日付は MUST で絶対日付 `YYYY-MM-DD` を使う

## 任意条件の指定方法

### 自然文で指定する場合

- 価格帯の下限: `最低10000円`
- 価格帯の上限: `最大25000円`
- 室数: `2室`
- 禁煙: `禁煙`
- 朝食付き: `朝食`
- 夕食付き: `夕食`
- 温泉あり: `温泉`

このスキルは、たとえば `最低10000円 最大25000円 禁煙 朝食 2室` のような、上記キーワード表現を自然文へ追加した入力を解釈する。

### CLIで直接指定する場合

- `--page 2`
- `--hits 30`
- `--max-pages 3`
- `--search-pattern 0`
- `--room-num 2`
- `--min-charge 10000`
- `--max-charge 25000`

## 未対応の表現

- `明日`, `来週`, `週末` のような相対日付
- `1泊` のような宿泊数からの自動日付補完
- `安い順`, `人気順` のような自然文ソート指定
- 曖昧な地名からの自動決め打ち

## 入力例

- `京都市で2026-05-01チェックイン 2026-05-02チェックアウト 2名`
- `京都市で2026-05-01チェックイン 2026-05-02チェックアウト 2名 禁煙 朝食`
- `館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名 最低10000円 最大25000円`
- `函館で2026-06-01チェックイン 2026-06-02チェックアウト 3名 2室 温泉`

## 動作方針

1. 入力不足があれば `場所` → `チェックイン日` → `チェックアウト日` → `人数` の順で補う
2. `GetAreaClass` で地区コードを解決する
3. 候補が複数あれば自動選択せず、候補一覧を返す
4. `VacantHotelSearch` を実行する
5. ホテル名、プラン名、料金、評価、住所、詳細 URL を整形して返す

## 検証と再試行

1. detail（詳細地区）で検索する
2. 0件なら small（小地区）まで広げる
3. さらに 0件なら middle（中地区）まで広げる
4. 429 や一時的な 5xx はバックオフして再試行する

## 返却内容

- 検索条件の確認
- API総件数 / 表示件数 / ページ情報 / 取得ページ数
- 候補ホテル一覧
- 料金表示は楽天APIの料金区分 `chargeFlag` に応じて `1人あたり` または `1室あたり` として返す

## 禁止事項

- API キーや環境変数の中身を出力しない
- 未確認の日付を勝手に補完しない
- 複数候補の地区コードを勝手に決めない

## 実行例

```bash
PYTHONPATH=src python -m rakuten_travel_skill.cli "京都市で2026-05-01チェックイン 2026-05-02チェックアウト 2名"
PYTHONPATH=src python -m rakuten_travel_skill.cli "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名 最低10000円 最大25000円"
PYTHONPATH=src python -m rakuten_travel_skill.cli "函館で2026-06-01チェックイン 2026-06-02チェックアウト 3名 2室 禁煙 朝食 温泉"
PYTHONPATH=src python -m rakuten_travel_skill.cli --page 2 --hits 30 "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
PYTHONPATH=src python -m rakuten_travel_skill.cli --page 1 --max-pages 3 --hits 30 "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
PYTHONPATH=src python -m rakuten_travel_skill.cli --page 1 --max-pages 3 --hits 30 --min-charge 10000 --max-charge 25000 "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
```
