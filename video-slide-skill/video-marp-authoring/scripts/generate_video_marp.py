#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def split_slides(body: str):
    body = body.strip("\n")
    if not body:
        return []
    return re.split(r"\n\s*---\s*\n", body)


def extract_style_block(frontmatter: str) -> str:
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        if re.match(r"^style\s*:\s*\|\s*$", lines[i]):
            i += 1
            buf = []
            while i < len(lines):
                ln = lines[i]
                if ln.startswith("  "):
                    buf.append(ln[2:])
                    i += 1
                    continue
                if ln.strip() == "":
                    buf.append("")
                    i += 1
                    continue
                break
            return "\n".join(buf).rstrip()
        i += 1
    return ""


def remove_style_block(frontmatter: str) -> str:
    if not frontmatter.strip():
        return ""
    out = []
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^style\s*:\s*\|\s*$", line):
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.startswith("  ") or nxt.strip() == "":
                    i += 1
                    continue
                break
            continue
        out.append(line)
        i += 1
    return "\n".join(out).strip("\n")


def parse_frontmatter_pairs(frontmatter: str):
    result = []
    for ln in frontmatter.splitlines():
        if not ln.strip() or ":" not in ln:
            continue
        key, value = ln.split(":", 1)
        result.append((key.strip(), value.strip()))
    return result


def ensure_core_frontmatter(src_frontmatter: str, css: str, overrides: dict | None) -> str:
    fm = remove_style_block(src_frontmatter)
    ordered = parse_frontmatter_pairs(fm)
    data = {k: v for k, v in ordered}

    if overrides:
        for k, v in overrides.items():
            data[str(k)] = str(v)

    if "marp" not in data:
        data["marp"] = "true"
    if "html" not in data:
        data["html"] = "true"
    if "theme" not in data:
        data["theme"] = "default"

    lines = [f"{k}: {v}" for k, v in data.items()]
    lines.append("style: |")
    lines.extend([f"  {ln}" if ln else "" for ln in css.splitlines()])
    return "---\n" + "\n".join(lines).rstrip() + "\n---\n\n"


def parse_template_layouts(template_md: str):
    t_frontmatter, t_body = split_frontmatter(template_md)
    style = extract_style_block(t_frontmatter)
    slides = split_slides(t_body)
    if not slides:
        raise SystemExit("テンプレートにスライドがありません。")

    layouts = {}
    for idx, slide in enumerate(slides, start=1):
        m = re.search(r"<!--\s*Layout\s*\d+\s*:\s*([^>]+?)\s*-->", slide)
        if m:
            raw_name = m.group(1).strip().lower()
            # "intro 3 columns" -> "intro", "grid cards" -> "grid"
            key = re.sub(r"[^a-z0-9_-]+", "-", raw_name).strip("-")
            if key.startswith("cover"):
                key = "cover"
            elif key.startswith("intro"):
                key = "intro"
            elif key.startswith("grid"):
                key = "grid"
            elif key.startswith("quote"):
                key = "quote"
            elif key.startswith("outro"):
                key = "outro"
        else:
            key = f"layout-{idx}"
        layouts[key] = slide.strip("\n")

    return style, layouts


def validate_blueprint(bp: dict):
    if not isinstance(bp, dict):
        raise SystemExit("blueprintはJSON objectである必要があります。")
    slides = bp.get("slides")
    if not isinstance(slides, list) or not slides:
        raise SystemExit("blueprint.slides は1件以上の配列である必要があります。")
    for i, s in enumerate(slides, start=1):
        if not isinstance(s, dict):
            raise SystemExit(f"blueprint.slides[{i}] がobjectではありません。")
        if "layout" not in s:
            raise SystemExit(f"blueprint.slides[{i}] に layout がありません。")
        if "video" not in s:
            raise SystemExit(f"blueprint.slides[{i}] に video がありません。")
        if "fields" in s and not isinstance(s["fields"], dict):
            raise SystemExit(f"blueprint.slides[{i}].fields はobjectである必要があります。")


def render_layout(layout_html: str, video_src: str, page_num: int, fields: dict):
    output = layout_html

    merged = {
        "VIDEO_SRC": video_src,
        "PAGE_NUM": str(page_num),
    }
    for k, v in fields.items():
        merged[str(k)] = str(v)

    for k, v in merged.items():
        output = output.replace("{{" + k + "}}", v)

    unresolved = re.findall(r"\{\{[A-Z0-9_]+\}\}", output)
    if unresolved:
        missing = ", ".join(sorted(set(unresolved)))
        raise SystemExit(f"layout置換後に未解決プレースホルダが残っています: {missing}")

    return output.strip("\n")


def build_from_blueprint(source_slides, blueprint: dict, layouts: dict, strict_count: bool):
    bp_slides = blueprint["slides"]
    if strict_count and len(bp_slides) != len(source_slides):
        raise SystemExit(
            f"blueprintのスライド数({len(bp_slides)})と入力Marpのスライド数({len(source_slides)})が一致しません。"
        )

    out = []
    for i, item in enumerate(bp_slides, start=1):
        layout_name = str(item["layout"]).strip().lower()
        if layout_name not in layouts:
            available = ", ".join(sorted(layouts.keys()))
            raise SystemExit(f"不明なlayout: {layout_name}. 利用可能: {available}")

        fields = dict(item.get("fields", {}))
        # デフォルト値を補完
        fields.setdefault("SLIDE_META", f"Slide {i:03d}")
        fields.setdefault("LOGO", "YOUR LOGO")
        fields.setdefault("CONTACT_1", "https://example.com")
        fields.setdefault("CONTACT_2", "https://facebook.com/example")
        fields.setdefault("CONTACT_3", "+1 (000) 000-0000")
        fields.setdefault("CONTACT_4", "contact@example.com")
        fields.setdefault("CONTACT_5", "Your City, Country")

        out.append(render_layout(layouts[layout_name], str(item["video"]), i, fields))
    return out


def wrap_slide_with_video(slide: str, src: str) -> str:
    if 'class="bg-video"' in slide:
        return slide.strip("\n")
    content = slide.strip("\n")
    return (
        f'<video class="bg-video" src="{src}" autoplay muted loop playsinline></video>\n'
        f'<div class="layer">\n{content}\n</div>'
    )


def parse_mapping_lines(lines):
    mapping = {}
    patterns = [
        re.compile(r"^\s*(\d+)\s*[:：]\s*(\S.+?)\s*$"),
        re.compile(r"^\s*(\d+)\s+(.+?)\s*$"),
        re.compile(r"^\s*(\d+)\s*ページ目\s*は\s*(\S.+?)\s*$"),
        re.compile(r"^\s*[Pp]age\s*(\d+)\s*[:：]?\s*(\S.+?)\s*$"),
    ]

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        ok = False
        for pat in patterns:
            m = pat.match(line)
            if m:
                mapping[int(m.group(1))] = m.group(2).strip()
                ok = True
                break
        if not ok:
            raise SystemExit(f"動画割当の形式が不正です: {raw}")
    return mapping


def main():
    parser = argparse.ArgumentParser(description="Generate video-enabled Marp markdown")
    parser.add_argument("input_md")
    parser.add_argument("output_md")
    parser.add_argument(
        "--mode",
        choices=["blueprint", "preserve"],
        default="blueprint",
        help="blueprint: LLM設計図(JSON)を使ってテンプレート組み立て, preserve: 元構造にvideo/layerを注入",
    )
    parser.add_argument(
        "--blueprint-file",
        default=None,
        help="JSON blueprint file for blueprint mode",
    )
    parser.add_argument(
        "--template-md",
        default=str(Path(__file__).resolve().parents[1] / "references" / "video-pitch-deck-template.md"),
        help="Template markdown that contains style and layout slides",
    )
    parser.add_argument(
        "--strict-count",
        action="store_true",
        help="Require blueprint slide count == source slide count",
    )
    parser.add_argument("--map-file", default=None, help="Mapping file for preserve mode")
    parser.add_argument("--map-line", action="append", default=[], help="Mapping line for preserve mode")

    args = parser.parse_args()

    input_path = Path(args.input_md)
    output_path = Path(args.output_md)
    template_path = Path(args.template_md)

    if not input_path.exists():
        raise SystemExit(f"入力Marpが見つかりません: {input_path}")
    if output_path.exists():
        raise SystemExit(f"出力先が既に存在します: {output_path}")
    if not template_path.exists():
        raise SystemExit(f"テンプレートMarkdownが見つかりません: {template_path}")

    src_raw = input_path.read_text(encoding="utf-8")
    src_frontmatter, src_body = split_frontmatter(src_raw)
    source_slides = split_slides(src_body)
    if not source_slides:
        raise SystemExit("入力Marpにスライドがありません。")

    template_raw = template_path.read_text(encoding="utf-8")
    template_style, layouts = parse_template_layouts(template_raw)
    if not template_style:
        raise SystemExit("テンプレートのstyleブロックが見つかりません。")

    if args.mode == "blueprint":
        if not args.blueprint_file:
            raise SystemExit("blueprintモードでは --blueprint-file が必要です。")
        bp_path = Path(args.blueprint_file)
        if not bp_path.exists():
            raise SystemExit(f"blueprintファイルが見つかりません: {bp_path}")
        blueprint = json.loads(bp_path.read_text(encoding="utf-8"))
        validate_blueprint(blueprint)

        new_frontmatter = ensure_core_frontmatter(
            src_frontmatter,
            template_style,
            blueprint.get("frontmatter_overrides", {}),
        )
        out_slides = build_from_blueprint(source_slides, blueprint, layouts, args.strict_count)

    else:
        map_lines = list(args.map_line)
        if args.map_file:
            mf = Path(args.map_file)
            if not mf.exists():
                raise SystemExit(f"map-fileが見つかりません: {mf}")
            map_lines.extend(mf.read_text(encoding="utf-8").splitlines())

        mapping = parse_mapping_lines(map_lines)
        expected = set(range(1, len(source_slides) + 1))
        actual = set(mapping.keys())
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing or extra:
            msg = []
            if missing:
                msg.append(f"未指定ページ: {missing}")
            if extra:
                msg.append(f"範囲外ページ: {extra}")
            raise SystemExit("動画割当が不正です: " + ", ".join(msg))

        new_frontmatter = ensure_core_frontmatter(src_frontmatter, template_style, None)
        out_slides = [wrap_slide_with_video(s, mapping[i]) for i, s in enumerate(source_slides, start=1)]

    output_text = new_frontmatter + "\n\n---\n\n".join(out_slides).rstrip() + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")

    print(f"Generated: {output_path}")
    print(f"Slides: {len(out_slides)}")
    print(f"Mode: {args.mode}")


if __name__ == "__main__":
    main()
