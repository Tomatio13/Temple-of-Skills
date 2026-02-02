<p align="center">
  <h1 align="center">Marp Layout Fix</h1>
</p>

<p align="center">
  <a href="README_EN.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Marp-CLI-blue" alt="Marp CLI"/>
  <img src="https://img.shields.io/badge/Bash-4.0%2B-green" alt="Bash"/>
  <img src="https://img.shields.io/badge/Node.js-18%2B-brightgreen" alt="Node.js"/>
</p>

A skill/toolkit for detecting and fixing layout issues in Marp slides (overflow, too many items, insufficient contrast, etc.).

## 📋 Overview

This toolkit provides procedures and helper scripts to generate all-page PNGs using Marp's image output feature and iterate through LLM-based corrections and re-verification.

### Supported Issues

- **Overflow**: Bottom of slide is cut off
- **Too many items**: More than 5 vertical items won't fit
- **Insufficient contrast**: Hard to distinguish between background and text colors

## ⚙️ Prerequisites

- [Marp CLI](https://github.com/marp-team/marp-cli) installed
- Bash environment available

### Installing Marp CLI

```bash
npm install -g @marp-team/marp-cli
```

## 🚀 Quick Start

### 1. Export Images

```bash
.agents/skills/marp-layout-fix/scripts/export-images.sh \
  /absolute/path/to/slides.md \
  /absolute/path/to/out
```

### 2. Check Images and Detect Layout Issues

Review the output PNG files and identify problematic pages.

### 3. Send Correction Instructions to LLM

Refer to `references/prompt-template.md` and send correction instructions to the LLM along with the problematic page PNG.

### 4. Apply Corrections and Verify

Modify the Markdown file and re-export to confirm the issue is resolved.

## 🔄 Detailed Workflow

```
┌─────────────────┐
│ 1. PNG Export   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Image Check  │
│    (Issue Detect)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. LLM Fix Plan │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Markdown Fix │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Re-export    │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Fixed? │
    └───┬────┘
        │ No   Yes
        ▼      │
  ┌─────┴──────┐ │
  │ Back to 2   │ │
  └────────────┘ │
                 ▼
            ┌─────────┐
            │ Complete│
            └─────────┘
```

## 📊 Common Fix Patterns

| Issue | Cause | Solution |
|-------|-------|----------|
| Overflow | gap/margin/padding too large | Reduce these values |
| More than 5 vertical items | Physically won't fit in one column | Change to 2-column grid or split slide |
| Insufficient contrast | Similar background and text colors | Increase contrast ratio |
| Text on image | Low visibility | Add bg opacity or drop shadow |

## 🔧 Scripts

### `scripts/export-images.sh`

Generates all-page PNGs using Marp's image output.

```bash
usage: export-images.sh /absolute/path/to/slides.md /absolute/path/to/out
```

**Features**:
- `--images png`: Output in PNG format
- `--allow-local-files`: Supports local file references

**Errors**:
- Marp not installed: `error: marp not found in PATH`
- Missing arguments: Usage message is displayed

## 📚 References

- `references/prompt-template.md`: Template for correction instructions to LLM

## ⚠️ Notes

- PNG output filenames follow Marp's sequential numbering format
- Manually delete output PNGs after verification is complete

## License

MIT License
