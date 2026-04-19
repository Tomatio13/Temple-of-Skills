<h1 align="center">Rakuten Travel Skill</h1>

<p align="center">
  楽天トラベル API を使って空室候補を検索する CLI / Agent Skill
</p>

## セットアップ

このリポジトリはビルド不要です。通常は共有またはローカルの仮想環境を有効化し、必要な依存だけを入れて使います。

```bash
python -m venv .venv
. .venv/bin/activate
pip install requests
```

必要な環境変数:

- `RAKUTEN_APPLICATION_ID`: 必須
- `RAKUTEN_ACCESS_KEY`: 環境によっては必須
- `RAKUTEN_AFFILIATE_ID`: 任意
- `RAKUTEN_TIMEOUT_SECONDS`: 任意。既定値 `10`
- `RAKUTEN_MAX_RETRIES`: 任意。既定値 `2`
- `RAKUTEN_USER_AGENT`: 任意
- `RAKUTEN_AREA_CACHE_PATH`: 任意。`GetAreaClass` の JSON キャッシュ保存先

このリポジトリでは認証情報を `.env` に置く前提とする。

```bash
set -a
. ./.env
set +a
```

例:

```bash
RAKUTEN_APPLICATION_ID=your-application-id
RAKUTEN_ACCESS_KEY=your-access-key
```

## 使い方

自然文:

```bash
PYTHONPATH=src python -m rakuten_travel_skill.cli "京都市で2026-05-01チェックイン 2026-05-02チェックアウト 2名 禁煙 朝食"
PYTHONPATH=src python -m rakuten_travel_skill.cli --page 2 --hits 30 "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
```

JSON:

```bash
PYTHONPATH=src python -m rakuten_travel_skill.cli --json '{
  "location": "京都市",
  "checkin_date": "2026-05-01",
  "checkout_date": "2026-05-02",
  "adult_count": 2,
  "squeeze_conditions": ["kinen", "breakfast"]
}'
```

## 入力方法

必須項目:

- `location`
- `checkin_date`
- `checkout_date`
- `adult_count`

任意項目:

- `room_num`
- `min_charge`
- `max_charge`
- `squeeze_conditions`
- `hits`
- `page`
- `max_pages`
- `search_pattern`

自然文での指定例:

- `館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名 最低10000円 最大25000円`
- `函館で2026-06-01チェックイン 2026-06-02チェックアウト 3名 2室 禁煙 朝食`
- `京都市で2026-05-01チェックイン 2026-05-02チェックアウト 2名 温泉`

対応している自然文キーワード:

- `最低12345円` -> `min_charge`
- `最大25000円` -> `max_charge`
- `2室` -> `room_num`
- `禁煙` -> `kinen`
- `朝食` -> `breakfast`
- `夕食` -> `dinner`
- `温泉` -> `onsen`

CLI オプションで上書きできる項目:

- `--page 2`
- `--max-pages 3`
- `--hits 30`
- `--search-pattern 0`
- `--room-num 2`
- `--min-charge 10000`
- `--max-charge 25000`

複数ページ取得の例:

```bash
PYTHONPATH=src python -m rakuten_travel_skill.cli --page 1 --max-pages 3 --hits 30 "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
```

## 出力内容

- 検索条件の確認
- API総件数 / 表示件数 / ページ情報 / 取得ページ数
- 候補ホテル一覧
- 料金表示は `chargeFlag` に応じて `1人あたり` または `1室あたり`

## 制約

- 地区コードが複数候補に一致した場合は自動決め打ちしません。
- 相対日付の自然言語解釈は未対応です。`2026-05-01` のような絶対日付で指定してください。
- 実装は検索までで、予約確定やログイン操作は行いません。
- 複数アプリの同時切り替えは未対応です。必要なら `.env` を入れ替えて使います。

## テスト

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## デバッグ

API が 0 件を返しているのか、こちらの解釈が漏れているのか切り分けたい場合は `--debug` を付けます。

```bash
PYTHONPATH=src python -m rakuten_travel_skill.cli --debug "館山で2026-05-08チェックイン 2026-05-09チェックアウト 2名"
```

## TIPS : RAKUTEN_APPLICATION_ID,RAKUTEN_ACCESS_KEYの取得方法

### 手順
1. 自端末のグローバルアドレスを確認する
判らなければ、以下のコマンドで確認できます。
```bash
curl ifconfig.me
```

2. [Rakuten Developers](https://webservice.rakuten.co.jp/)にブラウザでアクセスし、アカウント作成の上でログインする。

3. アプリID発行を選択する。

4. 以下の情報を入力する。

例.
    - アプリケーションの説明：楽天トラベルAPIを利用して空室検索を行うローカル検証用ツール
    - アプリケーションURL: http://localhost:8000/
    - アプリケーションタイプ: API/バックエンドサービス
    - 許可されたIPアドレス: 手順1で確認したグローバルIPアドレス
    - APIアクセススコープ： 楽天トラベルAPI
    - データ利用目的: 楽天トラベルの空室検索条件んい基づき、候補施設とプラン情報を取得してローカルで確認する
    - 予想QDS : 1 リクエスト/秒

5. 正しく入力できてれば、以下の情報が発行されるので控えておく。

- アプリケーションID
- アクセスキー
- アフェリエイトID

上記情報は、「アプリ情報の確認ページ」から確認することは可能です。







### 必要な情報
グローバルアドレスを指定して
