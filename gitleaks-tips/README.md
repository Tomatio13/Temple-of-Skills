<h1 align="center">gitleaks + pre-commit Setup</h1>

<p align="center">
  <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen" alt="pre-commit"/>
  <img src="https://img.shields.io/badge/gitleaks-v8.30.1-blue" alt="gitleaks"/>
</p>

## 📝 概要

`pre-commit` は、`git commit` の直前に任意のチェックを自動実行するためのフレームワークです。
`gitleaks` は、APIキーやトークンなどのシークレットがソースコードや設定ファイルに含まれていないかを検出するツールです。

この README の目的は、各Gitリポジトリで `gitleaks` を `pre-commit` フックとして簡単に有効化し、誤って認証情報をコミットするリスクを下げることです。

## 🚀 使い方

各Gitリポジトリで、`git init` または `git clone` の後に 1 回だけ次を実行します。

```bash
gitleaks-init
```

## 📦 pre-commitとgitleaksのインストール

### pre-commitのインストール
Ubuntu系環境では、以下のコマンドを実行する。
```bash
sudo apt update
sudo apt install pre-commit
```

### gitleaksをインストールする。
[Gitleaks公式Hub](https://github.com/gitleaks/gitleaks/releases)を確認して、
最新バージョンに合わせてダウンロードするファイルを変更してください。

```bash
# 最新バージョンダウンロード(例: v8.30.1の場合)
wget https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz
tar -xf gitleaks_8.30.1_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# 確認
gitleaks version
```

## 🔧 設定
### `git init`した瞬間に`gitleaks`を自動で有効化する

この設定の目的は、新しく作成するGitリポジトリで `pre-commit` フックを自動的に有効化し、手動設定漏れを減らすことです。

`git init`や`git clone`を実施すると自動的に、`pre-commit install`を自動的に実施されるように設定する。

```bash
# テンプレート用フォルダを作成
mkdir -p ~/.git-template/hooks

# pre-commitをテンプレートとして登録
pre-commit init-templatedir ~/.git-template -t pre-commit -t pre-push

# Gitの全体設定に登録
git config --global init.templateDir ~/.git-template

```

> 注意： 既存のリポジトリには自動設定されません。

### `pre-commit`の設定で`gitleaks`を実行する共通設定ファイルを作成する

この設定の目的は、各リポジトリで同じ `gitleaks` 設定を使い回せるようにし、設定のばらつきを防ぐことです。

- 作成場所: ~/.git-template
- ファイル名: .common-pre-commit-config.yaml
- 内容:
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1  # インストールしたGitleaksのバージョンに合わせる
    hooks:
      - id: gitleaks
```

### `.pre-commit-config.yaml`のコピーと`pre-commit install`を実行するコマンド(エイリアス)を設定する

この設定の目的は、各リポジトリで必要な設定ファイルの配置と `pre-commit` の有効化を 1 コマンドで完了できるようにすることです。

```bash
echo "alias gitleaks-init='cp -p ~/.git-template/.common-pre-commit-config.yaml ./.pre-commit-config.yaml && pre-commit install'" >> ~/.bashrc

source ~/.bashrc
```

> 注意: 既存の`.pre-commit-config.yaml`があるリポジトリでは上書きしないでください。

## ✅ 動作確認

本番適用前に必ず動作確認を実施してください。

```bash
# 確認用ディレクトリ
mkdir leak-test
cd leak-test

# git init
git init

# 各リポジトリで初回のみ実行
gitleaks-init

# ダミーファイルの作成とadd
echo "AWS_KEY=AKIAU7PR8V6Q2Z9X4LMT" > test.txt # gitleaks:allow
git add test.txt

# commit時にleakが検出されれば設定OK
git commit -m "Test leak"
```

> 注意: `# gitleaks:allow`のコメントをつけるとgitleaksのチェック対象外になります。
> 動作確認時はつけずに確認して下さい。

期待結果:

```text
Detect hardcoded secrets...Failed
- hook id: gitleaks
Finding: AWS_KEY=REDACTED
File: test.txt
Line: 1
```

## 🔍 gitleaksを手動で実行する

`pre-commit` を使わずに `gitleaks` を手動実行したい場合は、必要に応じて以下を使い分けます。

### 現在の作業ディレクトリをスキャンする

未コミットのファイルや現在のディレクトリ配下を確認したい場合:

```bash
gitleaks detect --no-git -v
```

### Git履歴を含めてスキャンする

コミット済みの履歴も含めて確認したい場合:

```bash
gitleaks git .
```

### 使い分け

- `gitleaks detect .`
  - 現在の作業ディレクトリ配下を対象にスキャンする
- `gitleaks git .`
  - Git履歴を対象にスキャンする
- まずは `gitleaks detect .` で現在の変更を確認し、必要に応じて `gitleaks git .` を実行する運用が分かりやすい
