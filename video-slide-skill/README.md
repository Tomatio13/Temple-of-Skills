<h1 align="center">video-slide-skill</h1>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Marp_CLI-required-0A84FF" alt="Marp CLI"/>
</p>

このリポジトリは、Marp 動画スライド作成フロー向けの **Agent Skills 集** です。  
各ディレクトリは「単体でトリガー可能な Skill（`SKILL.md` + 必要な scripts/references）」として構成されています。

## 📌 このリポジトリの位置づけ

- 目的: Codex/Agent に手順知識を渡し、動画スライド作業を再現可能にする
- 単位: 1フォルダ = 1 Skill
- 実装方針: `SKILL.md` はワークフロー中心、詳細仕様は `references/`、再利用可能処理は `scripts/`

## 🧩 Skills 一覧

### 1. `video-marp-authoring`

- 役割: 非動画 Marp を動画背景対応 Marp (`*-video.md`) に変換
- 中核ファイル:
  - `video-marp-authoring/SKILL.md`
  - `video-marp-authoring/scripts/generate_video_marp.py`
  - `video-marp-authoring/references/blueprint-schema.md`
  - `video-marp-authoring/references/video-pitch-deck-template.md`
- 代表的な処理:
  - `blueprint` モードでレイアウト駆動生成
  - `preserve` モードで既存構造を維持しつつ動画化

### 2. `video-marp-packager`

- 役割: 動画対応 Marp を配布可能なポータブル bundle に変換
- 中核ファイル:
  - `video-marp-packager/SKILL.md`
  - `video-marp-packager/scripts/build_portable_bundle.py`
  - `video-marp-packager/references/offline-fonts.md`
- 代表的な処理:
  - Marp HTML 生成
  - クリック遷移注入
  - 動画収集・パス置換
  - 任意フォント/ライセンス同梱
  - `portable/<deck>.tar.gz` 生成

## 🗂️ リポジトリ構造

```text
video-slide-skill/
├── video-marp-authoring/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── video-marp-packager/
    ├── SKILL.md
    ├── scripts/
    └── references/
```

## 🛠️ メンテナンスルール（このリポジトリ向け）

- Skill のトリガー条件は各 `SKILL.md` の frontmatter `description` に明確に書く
- 手順の本体は `SKILL.md`、詳細仕様や長文は `references/` に分離する
- 繰り返し実行・決定的処理は `scripts/` に切り出す
- Skill 単位で独立性を保ち、不要な補助ドキュメントを増やしすぎない

## 🚀 クイック利用フロー

1. `video-marp-authoring` で `*-video.md` を生成する
2. `video-marp-packager` で `portable/<deck>.tar.gz` を生成する
3. 出力 HTML と動画同梱状態を確認する

## ✅ スクリプト実行前提

- Python 3.10+
- `video-marp-packager` 実行時は `marp` CLI が必要

## 🎬 推奨動画ソース

利用する動画は、以下サイトに掲載されているライセンスフリーの tommyvideo さんの動画を推奨します。  
https://pixabay.com/users/3092371/?tab=videos&order=latest&pagi=1
