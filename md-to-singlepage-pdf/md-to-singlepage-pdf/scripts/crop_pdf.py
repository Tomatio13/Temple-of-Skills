#!/usr/bin/env python3
"""Trim bottom whitespace from PDF pages."""
from __future__ import annotations

import os
import sys

import fitz  # PyMuPDF


def crop_pdf_bottom(input_path: str) -> None:
    """Reduce bottom whitespace while keeping content."""
    if not os.path.exists(input_path):
        print(f"Not found: {input_path}")
        return

    doc = fitz.open(input_path)
    new_doc = fitz.open()

    for page in doc:
        drawings = page.get_drawings()
        text_dict = page.get_text("dict")

        max_y = 0.0

        for block in text_dict.get("blocks", []):
            if "bbox" in block:
                max_y = max(max_y, block["bbox"][3])

        for d in drawings:
            if "rect" in d:
                max_y = max(max_y, d["rect"][3])

        for img in page.get_images(full=True):
            try:
                img_rects = page.get_image_rects(img[0])
                for rect in img_rects:
                    max_y = max(max_y, rect.y1)
            except Exception:
                pass

        if max_y == 0:
            max_y = page.rect.height

        margin_bottom = 42.5  # ~15mm in points
        new_height = max_y + margin_bottom

        new_rect = fitz.Rect(0, 0, page.rect.width, new_height)
        new_page = new_doc.new_page(width=new_rect.width, height=new_rect.height)
        new_page.show_pdf_page(new_rect, doc, page.number, clip=new_rect)

    doc.close()

    temp_path = input_path + ".tmp"
    new_doc.save(temp_path, deflate=True)
    new_doc.close()

    os.replace(temp_path, input_path)
    print(f"Cropped: {input_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crop_pdf.py <pdf_file> [pdf_file2 ...]")
        sys.exit(1)

    for pdf_path in sys.argv[1:]:
        crop_pdf_bottom(pdf_path)
