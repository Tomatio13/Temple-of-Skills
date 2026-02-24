#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import subprocess
import tarfile
from pathlib import Path


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{res.stderr}")
    return res.stdout


def sanitize_name(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9_-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "deck"


def inject_click_nav(html_text: str) -> str:
    html_text = re.sub(r'<script id="marp-click-nav">.*?</script>', "", html_text, flags=re.S)
    injection = '''<script id="marp-click-nav">(function(){
  var isMainView = !document.body.dataset.bespokeView || document.body.dataset.bespokeView === '';
  if (!isMainView) return;

  var getNavButtons = function() {
    var prev = document.querySelector('.bespoke-marp-osc button[data-bespoke-marp-osc="prev"]');
    var next = document.querySelector('.bespoke-marp-osc button[data-bespoke-marp-osc="next"]');
    return { prev: prev, next: next };
  };

  var isInteractiveTarget = function(el) {
    return !!el.closest('button,a,input,textarea,select,[role="button"],.bespoke-marp-osc');
  };

  document.addEventListener('click', function(e) {
    var target = e.target;
    if (!(target instanceof Element)) return;
    if (isInteractiveTarget(target)) return;

    var nav = getNavButtons();
    if (!nav.prev || !nav.next) return;

    var width = window.innerWidth || document.documentElement.clientWidth;
    var leftThreshold = width * 0.35;
    if (e.clientX < leftThreshold) {
      nav.prev.click();
    } else {
      nav.next.click();
    }
  }, true);
})();</script>'''
    if "</body>" not in html_text:
        raise RuntimeError("HTMLに</body>が見つかりません。")
    return html_text.replace("</body>", injection + "</body>", 1)


def extract_video_srcs(html_text: str):
    return re.findall(r"<video[^>]*class=\"[^\"]*bg-video[^\"]*\"[^>]*src=\"([^\"]+)\"", html_text)


def resolve_video_source(src: str, input_md: Path, video_base: Path | None):
    if re.match(r"^(https?:)?//", src):
        return None

    src_path = Path(src)
    candidates = [
        (input_md.parent / src_path),
        (Path.cwd() / src_path),
    ]

    if video_base is not None:
        candidates.append(video_base / src_path)
        candidates.append(video_base / src_path.name)

    for c in candidates:
        if c.exists() and c.is_file():
            return c.resolve()
    return None


def remove_google_font_imports(html_text: str) -> str:
    return re.sub(r"@import\s+url\([^)]*fonts\.googleapis\.com[^)]*\);", "", html_text)


def inject_local_font_face(html_text: str, font_files):
    if not font_files:
        return html_text

    font_face = []
    for ff in font_files:
        low = ff.name.lower()
        if "bold" in low or "700" in low:
            weight = "700"
        elif "medium" in low or "500" in low:
            weight = "500"
        else:
            weight = "400"
        font_face.append(
            "@font-face { font-family: 'Plus Jakarta Sans'; "
            f"src: url('../fonts/{ff.name}') format('woff2'); font-style: normal; font-weight: {weight}; font-display: swap; }}"
        )

    inject = "\n".join(font_face)
    if "<style>" in html_text:
        return html_text.replace("<style>", f"<style>\n{inject}\n", 1)
    return html_text


def ensure_font_family_fallback(html_text: str) -> str:
    return html_text.replace(
        "font-family: 'Plus Jakarta Sans', sans-serif;",
        "font-family: 'Plus Jakarta Sans', 'Noto Sans JP', sans-serif;",
    )


def main():
    parser = argparse.ArgumentParser(description="Build portable Marp HTML bundle and tar.gz")
    parser.add_argument("input_md", help="Video-enabled Marp markdown")
    parser.add_argument("--output-root", default="portable", help="Output root directory")
    parser.add_argument("--video-base", default=None, help="Base directory for video resolution")
    parser.add_argument("--font-dir", default=None, help="Directory containing .woff2 files")
    parser.add_argument("--font-license", default=None, help="Font license text file path")
    args = parser.parse_args()

    input_md = Path(args.input_md).resolve()
    if not input_md.exists():
        raise SystemExit(f"入力ファイルが見つかりません: {input_md}")

    if shutil.which("marp") is None:
        raise SystemExit("marp コマンドが見つかりません")

    deck_name = sanitize_name(input_md.stem)
    output_root = Path(args.output_root).resolve()
    bundle_dir = output_root / deck_name
    html_dir = bundle_dir / "marp"
    video_dir = bundle_dir / "public" / "videos"
    fonts_dir = bundle_dir / "fonts"
    licenses_dir = bundle_dir / "LICENSES"

    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    html_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    html_out = html_dir / f"{deck_name}.html"
    run(["marp", str(input_md), "--html", "--bespoke", "-o", str(html_out)])

    html = html_out.read_text(encoding="utf-8")
    html = inject_click_nav(html)
    html = remove_google_font_imports(html)

    font_files = []
    if args.font_dir:
        src_font_dir = Path(args.font_dir).resolve()
        if not src_font_dir.exists() or not src_font_dir.is_dir():
            raise SystemExit(f"font-dir が不正です: {src_font_dir}")
        fonts_dir.mkdir(parents=True, exist_ok=True)
        for ff in sorted(src_font_dir.glob("*.woff2")):
            dst = fonts_dir / ff.name
            shutil.copy2(ff, dst)
            font_files.append(dst)

    html = inject_local_font_face(html, font_files)
    html = ensure_font_family_fallback(html)

    srcs = extract_video_srcs(html)
    if not srcs:
        raise SystemExit("bg-video src が見つかりません")

    video_base = Path(args.video_base).resolve() if args.video_base else None

    replace_map = {}
    for src in srcs:
        if src in replace_map:
            continue
        resolved = resolve_video_source(src, input_md, video_base)
        if resolved is None:
            raise SystemExit(f"動画ファイルを解決できません: {src}")
        dst_name = resolved.name
        shutil.copy2(resolved, video_dir / dst_name)
        replace_map[src] = f"../public/videos/{dst_name}"

    for old, new in replace_map.items():
        html = html.replace(f'src="{old}"', f'src="{new}"')

    html_out.write_text(html, encoding="utf-8")

    if args.font_license:
        lic = Path(args.font_license).resolve()
        if not lic.exists() or not lic.is_file():
            raise SystemExit(f"font-license が見つかりません: {lic}")
        licenses_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(lic, licenses_dir / lic.name)

    tar_path = output_root / f"{deck_name}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(bundle_dir, arcname=deck_name)

    print(f"HTML: {html_out}")
    print(f"Bundle: {bundle_dir}")
    print(f"Archive: {tar_path}")


if __name__ == "__main__":
    main()
