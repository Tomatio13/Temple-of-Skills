<h1 align="center">video-slide-skill</h1>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Marp_CLI-required-0A84FF" alt="Marp CLI"/>
</p>

This repository is a collection of **Agent Skills** for Marp video-slide workflows.  
Each directory is designed as an independently triggerable Skill (`SKILL.md` + required `scripts/` and `references/`).

## 📌 Purpose of This Repository

- Goal: provide reusable procedural knowledge for Codex/Agents
- Unit: one folder = one Skill
- Design: keep workflows in `SKILL.md`, move detailed specs to `references/`, and deterministic operations to `scripts/`

## 🧩 Skills

### 1. `video-marp-authoring`

- Role: convert non-video Marp into video-enabled Marp (`*-video.md`)
- Core files:
  - `video-marp-authoring/SKILL.md`
  - `video-marp-authoring/scripts/generate_video_marp.py`
  - `video-marp-authoring/references/blueprint-schema.md`
  - `video-marp-authoring/references/video-pitch-deck-template.md`
- Typical capabilities:
  - layout-driven generation in `blueprint` mode
  - compatibility conversion in `preserve` mode

### 2. `video-marp-packager`

- Role: package video-enabled Marp into a portable bundle
- Core files:
  - `video-marp-packager/SKILL.md`
  - `video-marp-packager/scripts/build_portable_bundle.py`
  - `video-marp-packager/references/offline-fonts.md`
- Typical capabilities:
  - Marp HTML generation
  - click navigation injection
  - video collection and path rewriting
  - optional font/license bundling
  - archive generation at `portable/<deck>.tar.gz`

## 🗂️ Repository Structure

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

## 🛠️ Maintenance Rules

- Define trigger conditions clearly in `description` of each `SKILL.md` frontmatter
- Keep procedural instructions in `SKILL.md`; move long details to `references/`
- Move repeated/deterministic logic into `scripts/`
- Keep each Skill independent and focused

## 🚀 Quick Usage Flow

1. Use `video-marp-authoring` to generate `*-video.md`
2. Use `video-marp-packager` to generate `portable/<deck>.tar.gz`
3. Verify HTML output, video playback, and bundled assets

## ✅ Runtime Prerequisites

- Python 3.10+
- `marp` CLI for running `video-marp-packager`

## 🎬 Recommended Video Source

For video assets, we recommend using royalty-free videos by tommyvideo on the following page:  
https://pixabay.com/users/3092371/?tab=videos&order=latest&pagi=1
