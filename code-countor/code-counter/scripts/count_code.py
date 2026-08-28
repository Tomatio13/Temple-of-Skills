#!/usr/bin/env python3
"""count_code.py — ソースコードの行数を言語別・ファイル別に集計する。

行種別の定義:
  空行      = 空白のみの行
  コメント行 = 行頭(空白を除く)がコメント記号で始まる行。ブロックコメント内の行を含む
  コード行   = 上記以外の行(総行数 - コメント行 - 空行)

Python の docstring(トリプルクォート)は文字列リテラルとしてコード行に数える。
文字列リテラル内のコメント記号(URL の "//", "#" など)は誤検知しない。
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# 言語定義
# ---------------------------------------------------------------------------

LANGS: dict[str, dict] = {
    #                行コメント         ブロックコメント            文字列リテラル
    "Python":      dict(ext=[".py", ".pyw", ".pyi"], line=["#"], block=[],
                        strings=['"""', "'''", '"', "'"]),
    "JavaScript":  dict(ext=[".js", ".mjs", ".cjs", ".jsx"], line=["//"], block=[("/*", "*/")],
                        strings=['"', "'", "`"]),
    "TypeScript":  dict(ext=[".ts", ".tsx", ".mts", ".cts"], line=["//"], block=[("/*", "*/")],
                        strings=['"', "'", "`"]),
    "Java":        dict(ext=[".java"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "Kotlin":      dict(ext=[".kt", ".kts"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "Scala":       dict(ext=[".scala"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "Dart":        dict(ext=[".dart"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "Swift":       dict(ext=[".swift"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "C":           dict(ext=[".c", ".h"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "C++":         dict(ext=[".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx", ".tcc", ".ipp"],
                        line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "C#":          dict(ext=[".cs"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "Objective-C": dict(ext=[".m", ".mm"], line=["//"], block=[("/*", "*/")], strings=['"', "'"]),
    "Go":          dict(ext=[".go"], line=["//"], block=[("/*", "*/")], strings=['"', "`"]),
    "Rust":        dict(ext=[".rs"], line=["//"], block=[("/*", "*/")], strings=['"']),
    "Ruby":        dict(ext=[".rb"], line=["#"], block=[("=begin", "=end")], strings=['"', "'"]),
    "PHP":         dict(ext=[".php"], line=["//", "#"], block=[("/*", "*/")], strings=['"', "'"]),
    "Shell":       dict(ext=[".sh", ".bash", ".zsh"], line=["#"], block=[], strings=['"', "'"]),
    "PowerShell":  dict(ext=[".ps1", ".psm1", ".psd1"], line=["#"], block=[("<#", "#>")],
                        strings=['"', "'"]),
    "R":           dict(ext=[".r"], line=["#"], block=[], strings=['"', "'"]),
    "Perl":        dict(ext=[".pl", ".pm"], line=["#"], block=[], strings=['"', "'"]),
    "Lua":         dict(ext=[".lua"], line=["--"], block=[("--[[", "]]")], strings=['"', "'"]),
    "Zig":         dict(ext=[".zig"], line=["//"], block=[], strings=['"', "'"]),
    "Julia":       dict(ext=[".jl"], line=["#"], block=[("#=", "=#")], strings=['"', "'"]),
    "Haskell":     dict(ext=[".hs"], line=["--"], block=[("{-", "-}")], strings=['"']),
    "OCaml":       dict(ext=[".ml", ".mli"], line=[], block=[("(*", "*)")], strings=['"']),
    "F#":          dict(ext=[".fs", ".fsx"], line=["//"], block=[("(*", "*)")], strings=['"']),
    "SQL":         dict(ext=[".sql"], line=["--"], block=[("/*", "*/")], strings=["'"]),
    "HTML":        dict(ext=[".html", ".htm", ".xhtml"], line=[], block=[("<!--", "-->")],
                        strings=['"', "'"]),
    "XML":         dict(ext=[".xml", ".svg", ".plist"], line=[], block=[("<!--", "-->")],
                        strings=['"', "'"]),
    "Vue":         dict(ext=[".vue"], line=[], block=[("<!--", "-->")], strings=['"', "'"]),
    "CSS":         dict(ext=[".css"], line=[], block=[("/*", "*/")], strings=['"', "'"]),
    "SCSS":        dict(ext=[".scss", ".sass", ".less"], line=["//"], block=[("/*", "*/")],
                        strings=['"', "'"]),
    "LaTeX":       dict(ext=[".tex", ".sty", ".cls"], line=["%"], block=[], strings=[]),
    "YAML":        dict(ext=[".yaml", ".yml"], line=["#"], block=[], strings=['"', "'"]),
    "TOML":        dict(ext=[".toml"], line=["#"], block=[], strings=['"', "'"]),
    "INI":         dict(ext=[".ini", ".cfg", ".conf"], line=[";", "#"], block=[], strings=[]),
    "Markdown":    dict(ext=[".md", ".markdown"], line=[], block=[("<!--", "-->")], strings=[]),
    "JSON":        dict(ext=[".json"], line=[], block=[], strings=['"']),
    "Makefile":    dict(ext=[".mk"], names=["makefile", "gnumakefile"], line=["#"], block=[],
                        strings=['"', "'"]),
    "Vim script":  dict(ext=[".vim"], line=['"'], block=[], strings=[]),
}

EXT_TO_LANG = {}
for _name, _def in LANGS.items():
    for _ext in _def.get("ext", []):
        EXT_TO_LANG[_ext] = _name
NAME_TO_LANG = {}
for _name, _def in LANGS.items():
    for _base in _def.get("names", []):
        NAME_TO_LANG[_base] = _name

EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "bower_components", "vendor",
    "__pycache__", ".venv", "venv", "env", ".tox", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".eggs", "site-packages", "dist", "build", "target", "out",
    "coverage", ".idea", ".vscode", ".next", ".nuxt", "obj",
}

BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tiff", ".pdf",
    ".zip", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".tar", ".jar", ".war",
    ".exe", ".dll", ".so", ".dylib", ".a", ".o", ".obj", ".class", ".pyc", ".pyo",
    ".wasm", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp3", ".mp4", ".mov",
    ".avi", ".mkv", ".wav", ".flac", ".ogg", ".db", ".sqlite", ".sqlite3",
    ".xls", ".xlsx", ".doc", ".docx", ".ppt", ".pptx", ".psd", ".ai",
}

OTHER_LANG = "その他"
MAX_KNOWN_BYTES = 5 * 1024 * 1024   # 既知言語のファイル上限
MAX_OTHER_BYTES = 1 * 1024 * 1024   # 未知の拡張子のファイル上限


@dataclass
class FileStat:
    path: str
    language: str
    total: int
    code: int
    comment: int
    blank: int


# ---------------------------------------------------------------------------
# 行種別の判定
# ---------------------------------------------------------------------------

def classify(text: str, lang_def: dict) -> tuple[int, int, int, int]:
    """テキストを (総行数, コード行, コメント行, 空行) に分類する。"""
    line_markers = lang_def["line"]
    block_pairs = lang_def["block"]
    string_delims = sorted(lang_def["strings"], key=len, reverse=True)

    lines = text.splitlines()
    total = len(lines)
    code = comment = blank = 0
    in_block_close: str | None = None   # 現在いるブロックコメントの終端記号
    in_string: str | None = None        # 現在いる文字列リテラルのデリミタ

    for raw in lines:
        if raw.strip() == "":
            blank += 1
            continue
        saw_code = False
        is_comment = False
        j, length = 0, len(raw)
        while j < length:
            if in_block_close is not None:
                idx = raw.find(in_block_close, j)
                if idx == -1:
                    j = length
                else:
                    j = idx + len(in_block_close)
                    in_block_close = None
                continue
            if in_string is not None:
                delim = in_string
                while j < length:
                    if raw[j] == "\\":
                        j += 2
                        continue
                    if raw.startswith(delim, j):
                        # 閉じ区切りも文字列リテラルの一部(docstring の """ 単独行など)なのでコード扱い
                        j += len(delim)
                        in_string = None
                        saw_code = True
                        break
                    if not raw[j].isspace():
                        saw_code = True
                    j += 1
                continue
            ch = raw[j]
            if ch.isspace():
                j += 1
                continue
            matched = False
            # ブロックコメント開始。Lua の "--" と "--[[" のように行コメントと
            # 前方共通する記号があるため、行コメントより先に判定する
            for opener, closer in block_pairs:
                if raw.startswith(opener, j):
                    if not saw_code:
                        is_comment = True
                    idx = raw.find(closer, j + len(opener))
                    if idx == -1:
                        in_block_close = closer
                        j = length
                    else:
                        j = idx + len(closer)
                    matched = True
                    break
            if matched:
                if is_comment:
                    break
                continue
            for marker in line_markers:
                if raw.startswith(marker, j):
                    if not saw_code:
                        is_comment = True
                    matched = True
                    break
            if matched:
                break
            for delim in string_delims:
                if raw.startswith(delim, j):
                    in_string = delim
                    j += len(delim)
                    saw_code = True
                    matched = True
                    break
            if matched:
                continue
            saw_code = True
            j += 1
        if is_comment or (in_block_close is not None and not saw_code):
            comment += 1
        elif saw_code:
            code += 1
        else:
            comment += 1
    return total, code, comment, blank


def classify_plain(text: str) -> tuple[int, int, int, int]:
    """コメント記法が不明なテキスト: コメント行は 0 として数える。"""
    lines = text.splitlines()
    total = len(lines)
    blank = sum(1 for line in lines if line.strip() == "")
    return total, total - blank, 0, blank


def looks_binary(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return b"\x00" in f.read(8192)
    except OSError:
        return True


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# ディレクトリ走査
# ---------------------------------------------------------------------------

def collect_files(target: Path, no_ignore: bool) -> list[FileStat]:
    stats: list[FileStat] = []
    excludes = set() if no_ignore else EXCLUDE_DIRS
    for root, dirnames, filenames in os.walk(target):
        dirnames[:] = sorted(d for d in dirnames if d not in excludes)
        for fname in sorted(filenames):
            fpath = Path(root) / fname
            ext = fpath.suffix.lower()
            if ext in BINARY_EXTS:
                continue
            lang = EXT_TO_LANG.get(ext)
            if lang is None and not ext:
                lang = NAME_TO_LANG.get(fname.lower())
            try:
                size = fpath.stat().st_size
            except OSError:
                continue
            if lang is not None:
                if size > MAX_KNOWN_BYTES:
                    continue
            else:
                if size > MAX_OTHER_BYTES or looks_binary(fpath):
                    continue
                lang = OTHER_LANG
            try:
                text = read_text(fpath)
            except OSError:
                continue
            lang_def = LANGS.get(lang)
            if lang_def is not None:
                total, code, comment, blank = classify(text, lang_def)
            else:
                total, code, comment, blank = classify_plain(text)
            rel = fpath.relative_to(target).as_posix()
            stats.append(FileStat(rel, lang, total, code, comment, blank))
    return stats


def aggregate(stats: list[FileStat], sort_key: str) -> list[dict]:
    langs: dict[str, dict] = {}
    for s in stats:
        agg = langs.setdefault(s.language, dict(language=s.language, files=0, total=0,
                                                code=0, comment=0, blank=0))
        agg["files"] += 1
        for field in ("total", "code", "comment", "blank"):
            agg[field] += getattr(s, field)
    return sorted(langs.values(), key=lambda a: a[sort_key], reverse=True)


# ---------------------------------------------------------------------------
# HTML レポート (html-create デザインシステムに従う)
# ---------------------------------------------------------------------------

PAGE_STYLE = """
    /* 数値列の右揃えとタブラー数字、構成比バーのみのページ固有スタイル */
    td.num, th.num { text-align: right; font-family: var(--mb-font-mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
    .mb-bar { display: flex; width: 100%; max-width: 320px; min-width: 160px; height: 10px; border-radius: 5px; overflow: hidden; border: 1px solid var(--mb-rule); }
    .mb-bar span { display: block; height: 100%; }
    .mb-bar .seg-code { background: var(--mb-ink); }
    .mb-bar .seg-comment { background: var(--mb-faint); }
    .mb-bar .seg-blank { background: var(--mb-rule); }
"""


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def n(x: int) -> str:
    return f"{x:,}"


def bar_svg(agg: dict) -> str:
    total = agg["total"] or 1
    def w(field):
        return round(agg[field] / total * 100, 2)
    return (f'<div class="mb-bar" role="img" aria-label="コード {w("code")}% コメント {w("comment")}% 空行 {w("blank")}%">'
            f'<span class="seg-code" style="width:{w("code")}%"></span>'
            f'<span class="seg-comment" style="width:{w("comment")}%"></span>'
            f'<span class="seg-blank" style="width:{w("blank")}%"></span>'
            f'</div>')


def render_html(target: Path, stats: list[FileStat], langs: list[dict], generated_at: str,
                design_css: str) -> str:
    total_files = len(stats)
    g_total = sum(a["total"] for a in langs)
    g_code = sum(a["code"] for a in langs)
    g_comment = sum(a["comment"] for a in langs)
    g_blank = sum(a["blank"] for a in langs)
    comment_rate = g_comment / g_total * 100 if g_total else 0.0
    code_rate = g_code / g_total * 100 if g_total else 0.0

    lang_rows = []
    for a in langs:
        lang_rows.append(
            f'<tr><td>{esc(a["language"])}</td>'
            f'<td class="num">{n(a["files"])}</td>'
            f'<td class="num">{n(a["code"])}</td>'
            f'<td class="num">{n(a["comment"])}</td>'
            f'<td class="num">{n(a["blank"])}</td>'
            f'<td class="num"><strong>{n(a["total"])}</strong></td>'
            f'<td>{bar_svg(a)}</td></tr>')

    file_sections = []
    for a in langs:
        files = sorted((s for s in stats if s.language == a["language"]),
                       key=lambda s: s.code, reverse=True)
        rows = []
        for s in files:
            rows.append(
                f'<tr><td><code>{esc(s.path)}</code></td>'
                f'<td class="num">{n(s.code)}</td>'
                f'<td class="num">{n(s.comment)}</td>'
                f'<td class="num">{n(s.blank)}</td>'
                f'<td class="num"><strong>{n(s.total)}</strong></td></tr>')
        file_sections.append(
            f'<h3>{esc(a["language"])}({a["files"]}ファイル・コード{n(a["code"])}行)</h3>\n'
            f'<table>\n<tr><th>ファイル</th><th class="num">コード行</th>'
            f'<th class="num">コメント行</th><th class="num">空行</th>'
            f'<th class="num">総行数</th></tr>\n' + "\n".join(rows) + '\n</table>')

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>コード規模レポート — {esc(target.name)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Ubuntu+Sans:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&family=Ubuntu+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
{design_css}
</style>
<style>{PAGE_STYLE}</style>
</head>
<body>
<div class="mb-page">

<header class="mb-header">
  <div>
    <h1>コード規模レポート</h1>
    <p class="mb-meta-line">target: {esc(str(target))} / generated by count_code.py</p>
  </div>
</header>

<p class="mb-lede">
<strong>{esc(str(target))}</strong> のソースコードをファイル別・言語別に集計した結果です。
総行数 {n(g_total)} 行のうち、コード行(コメントを除く)は {n(g_code)} 行、コメント行は {n(g_comment)} 行で、コメント率は {comment_rate:.1f}% です。
</p>

<div class="mb-wrap">
<div class="mb-main">

<nav class="mb-toc">
  <ol>
    <li><a href="#summary">要点</a></li>
    <li><a href="#languages">言語別サマリー</a></li>
    <li><a href="#files">ファイル別明細</a></li>
    <li><a href="#rules">集計ルールと限界</a></li>
  </ol>
</nav>

<div class="mb-summary" id="summary">
  <ul>
    <li>集計対象は <strong>{total_files} ファイル・{len(langs)} 言語</strong>、総行数 <strong>{n(g_total)} 行</strong></li>
    <li>コード行 {n(g_code)} 行({code_rate:.1f}%) / コメント行 {n(g_comment)} 行 / 空行 {n(g_blank)} 行</li>
    <li>コード行が多い言語は {", ".join(esc(a["language"]) for a in langs[:3])}</li>
  </ul>
</div>

<h2 id="languages">言語別サマリー</h2>

<p>構成比のバーは、左から黒(コード行)・グレー(コメント行)・薄グレー(空行)の比率を示します。</p>

<table>
<tr><th>言語</th><th class="num">ファイル数</th><th class="num">コード行</th><th class="num">コメント行</th><th class="num">空行</th><th class="num">総行数</th><th>構成比</th></tr>
{chr(10).join(lang_rows)}
<tr><td><strong>合計</strong></td><td class="num"><strong>{n(total_files)}</strong></td><td class="num"><strong>{n(g_code)}</strong></td><td class="num"><strong>{n(g_comment)}</strong></td><td class="num"><strong>{n(g_blank)}</strong></td><td class="num"><strong>{n(g_total)}</strong></td><td></td></tr>
</table>

<h2 id="files">ファイル別明細</h2>

<p>各言語内でコード行の降順に並べます。</p>

{chr(10).join(file_sections)}

<h2 id="rules">集計ルールと限界</h2>

<ul>
  <li><strong>コメント行</strong>は、行頭(空白を除く)がコメント記号で始まる行と、ブロックコメント内の行。行末にコメントが付く行はコード行として数える</li>
  <li><strong>Python の docstring</strong>(トリプルクォート)は文字列リテラルとしてコード行に数える</li>
  <li>文字列リテラル内のコメント記号(URL の <code>//</code> や <code>#</code> など)はコメントと誤判定しない</li>
  <li>既知の除外ディレクトリ(<code>.git</code>、<code>node_modules</code>、<code>venv</code>、<code>dist</code>、<code>build</code> など)は集計対象外</li>
  <li>拡張子が未知のテキストファイルは「{OTHER_LANG}」として総行数と空行のみ数える(コメント記法を判定できないため)</li>
  <li>.h は C、.m は Objective-C として判定する。ヒアドキュメントや C++ の生文字列リテラル内は判定しない</li>
</ul>

</div><!-- /.mb-main -->

<aside class="mb-glossary">
  <h2>用語リスト</h2>
  <table>
    <tr><th>用語</th><th>定義</th></tr>
    <tr><td class="mb-rowlabel">コード行</td><td>総行数からコメント行と空行を除いた行。docstring は含む。</td></tr>
    <tr><td class="mb-rowlabel">コメント行</td><td>行頭がコメント記号で始まる行。ブロックコメント内の行を含む。</td></tr>
    <tr><td class="mb-rowlabel">空行</td><td>空白のみの行。</td></tr>
    <tr><td class="mb-rowlabel">コメント率</td><td>コメント行数 ÷ 総行数 × 100(%)。</td></tr>
  </table>
</aside>

</div><!-- /.mb-wrap -->

<footer class="mb-footer">generated: {esc(generated_at)} / code-counter skill (design: html-create design system)</footer>

</div>
</body>
</html>
"""
    return html


# ---------------------------------------------------------------------------
# 各種出力
# ---------------------------------------------------------------------------

def render_text(target: Path, stats: list[FileStat], langs: list[dict], top: int | None) -> str:
    g_total = sum(a["total"] for a in langs)
    g_code = sum(a["code"] for a in langs)
    g_comment = sum(a["comment"] for a in langs)
    g_blank = sum(a["blank"] for a in langs)
    out = []
    out.append(f"対象: {target}  ({len(stats)} ファイル)")
    out.append("")
    header = f'{"言語":<14}{"ファイル":>8}{"コード行":>10}{"コメント行":>10}{"空行":>8}{"総行数":>10}'
    out.append(header)
    out.append("-" * len(header.expandtabs()))
    for a in langs:
        out.append(f'{a["language"]:<14}{a["files"]:>8,}{a["code"]:>10,}{a["comment"]:>10,}{a["blank"]:>8,}{a["total"]:>10,}')
    out.append("-" * len(header.expandtabs()))
    out.append(f'{"合計":<14}{len(stats):>8,}{g_code:>10,}{g_comment:>10,}{g_blank:>8,}{g_total:>10,}')
    out.append("")
    for a in langs:
        files = sorted((s for s in stats if s.language == a["language"]),
                       key=lambda s: s.code, reverse=True)
        shown = files if top is None else files[:top]
        out.append(f'== {a["language"]} ==')
        for s in shown:
            out.append(f'  {s.code:>8,} code {s.comment:>7,} cmt {s.blank:>7,} blank {s.total:>8,} total  {s.path}')
        if top is not None and len(files) > top:
            out.append(f'  ... ほか {len(files) - top} ファイル')
        out.append("")
    return "\n".join(out)


def write_csv(path: Path, stats: list[FileStat]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["language", "file", "total", "code", "comment", "blank"])
        for s in sorted(stats, key=lambda s: (s.language, -s.code)):
            writer.writerow([s.language, s.path, s.total, s.code, s.comment, s.blank])


def default_output(fmt: str, now: datetime) -> Path:
    day = now.strftime("%Y%m%d")
    return Path.cwd() / f"{day}-code-scale-report.{fmt}"


def load_design_css() -> str:
    """html-create デザインシステムの CSS を読み込み、HTML に埋め込む。"""
    css = Path(__file__).resolve().parent.parent / "assets" / "design-system" / "document.css"
    if not css.exists():
        print(f"警告: document.css が見つかりません(スタイルなしのレポートになります): {css}",
              file=sys.stderr)
        return ""
    return css.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# エントリポイント
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="指定フォルダのソースコード行数を言語別・ファイル別に集計する")
    parser.add_argument("target", help="集計対象のフォルダ")
    parser.add_argument("--format", choices=["html", "text", "csv", "json"],
                        default="html", help="出力形式(既定: html)")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="出力ファイル(text 以外で必須。省略時はカレントに日付付きファイル名)")
    parser.add_argument("--sort", choices=["code", "total", "files"], default="code",
                        help="言語サマリーの並び順(既定: code)")
    parser.add_argument("--top", type=int, default=None,
                        help="テキスト出力で言語ごとに表示するファイル数の上限")
    parser.add_argument("--no-ignore", action="store_true",
                        help="除外ディレクトリ(.git, node_modules など)も集計する")
    args = parser.parse_args(argv)

    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"エラー: フォルダが見つかりません: {target}", file=sys.stderr)
        return 2

    now = datetime.now()
    stats = collect_files(target, args.no_ignore)
    langs = aggregate(stats, args.sort)

    if args.format == "text":
        print(render_text(target, stats, langs, args.top))
        return 0

    output = args.output if args.output is not None else default_output(args.format, now)
    if output.parent != Path.cwd():
        output.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "html":
        generated_at = now.strftime("%Y-%m-%d %H:%M:%S")
        output.write_text(render_html(target, stats, langs, generated_at,
                                      load_design_css()), encoding="utf-8")
    elif args.format == "csv":
        write_csv(output, stats)
    elif args.format == "json":
        data = {
            "generated_at": now.isoformat(timespec="seconds"),
            "target": str(target),
            "languages": langs,
            "files": [asdict(s) for s in sorted(stats, key=lambda s: (s.language, -s.code))],
        }
        output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    g_code = sum(a["code"] for a in langs)
    g_total = sum(a["total"] for a in langs)
    print(f"{len(stats)} ファイル / 総行数 {g_total:,} / コード行 {g_code:,} を集計しました")
    print(f"レポート: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
