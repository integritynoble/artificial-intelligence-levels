"""Reproduce and verify the owner-requested v2.6 author-only PDF amendment.

Requires PyMuPDF and Pillow (verified with PyMuPDF 1.27.1). The source is the
pinned, original PDF in Git, not an editable LaTeX source. No scientific claim,
contribution statement, or journal-readiness status is changed by this script.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess

import fitz
from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "12331315048e1cbf35a706f80ba572be81dcdd78"
PAPER = "papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf"
ORIGINAL_SHA256 = "c2a8738f25d0b98cf840b4fa55c4837c8f558bb29a4c00ce674797e684e2e9c3"
AUTHORS = "Chengshuai Yang; Ting Xue; Dingyi Kang"
HEADER_OLD = b"-15706(Y)100(ang)-250(and)-250(Xue)]TJ"
HEADER_AREA = fitz.Rect(440, 36, 542, 49)
AUTHOR_AREA = fitz.Rect(175, 160, 435, 181)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def once(data, old, new):
    require(data.count(old) == 1, "Expected exactly one source text operator")
    return data.replace(old, new, 1)


def words_outside(page, areas):
    return Counter(
        (word[4], *(round(value, 2) for value in word[:4]))
        for word in page.get_text("words")
        if not any(fitz.Rect(word[:4]).intersects(area) for area in areas)
    )


def verify(original, revised):
    require(len(original) == len(revised) == 69, "Page count changed")
    require(revised.metadata["author"] == AUTHORS, "Incorrect author metadata")
    expected_metadata = dict(original.metadata, author=AUTHORS)
    require(revised.metadata == expected_metadata, "Non-author PDF metadata changed")
    first = revised[0].get_text()
    for name in AUTHORS.split("; "):
        require(first.count(name) == 1, "Missing or duplicate author: " + name)
    require("NextGen PlatformAI C Corp, USA" in first, "Affiliation missing")
    changed_pages = []
    total_links = 0
    for index, (before, after) in enumerate(zip(original, revised)):
        require(before.rect == after.rect, "Page geometry changed")
        require(before.get_links() == after.get_links(), "PDF links changed")
        total_links += len(after.get_links())
        areas = [HEADER_AREA] if index < 65 else []
        if index == 0:
            areas.append(AUTHOR_AREA)
        require(words_outside(before, areas) == words_outside(after, areas),
                f"Non-author text or positions changed on page {index + 1}")
        require("Yang and Xue" not in after.get_text(), "Old author header remains")
        if index < 65:
            require(len(after.search_for("Yang, Xue and Kang")) == 1,
                    f"New author header missing on page {index + 1}")
        images = []
        for page in (before, after):
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2),
                                  colorspace=fitz.csRGB, alpha=False)
            images.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        difference = ImageChops.difference(*images)
        if difference.getbbox():
            changed_pages.append(index + 1)
        mask = ImageDraw.Draw(difference)
        for area in areas:
            mask.rectangle((math.floor(area.x0 * 2), math.floor(area.y0 * 2),
                            math.ceil(area.x1 * 2), math.ceil(area.y1 * 2)), fill=0)
        require(difference.getbbox() is None,
                f"Pixels changed outside author areas on page {index + 1}")
    require(changed_pages == list(range(1, 66)), "Unexpected visually changed pages")
    return {"pages_checked": 69, "headers_updated": 65,
            "unchanged_links": total_links, "pixel_comparison_dpi": 144,
            "pixels_outside_author_areas": "identical",
            "words_and_positions_outside_author_areas": "identical",
            "addendum_pages_66_to_69": "visually unchanged"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="Output PDF path; defaults to refusing existing files")
    parser.add_argument("--replace-original", action="store_true",
                        help="Replace only the repository PDF with the pinned original hash")
    args = parser.parse_args()
    if args.replace_original:
        require(args.output.resolve() == (ROOT / PAPER).resolve()
                and not args.output.is_symlink(), "Replacement is limited to the release PDF")
        require(hashlib.sha256(args.output.read_bytes()).hexdigest() == ORIGINAL_SHA256,
                "Release PDF changed; refusing to overwrite")
    else:
        require(not args.output.exists(), "Output already exists; refusing to overwrite")
    source = subprocess.run(["git", "show", BASELINE + ":" + PAPER], cwd=ROOT,
                            check=True, capture_output=True).stdout
    require(hashlib.sha256(source).hexdigest() == ORIGINAL_SHA256,
            "Original PDF does not match the pinned source hash")
    original = fitz.open(stream=source, filetype="pdf")
    revised = fitz.open(stream=source, filetype="pdf")

    # Reuse existing embedded font/resources and PDF text operators. Changing
    # only these narrowly matched byte sequences preserves all other operators.
    regular = fitz.Font(fontbuffer=original.extract_font(8)[3])
    name_size, superscript_size, gap = 11.9552, 8.9664, 14.0
    name_width = (regular.text_length("Dingyi", fontsize=name_size)
                  + name_size * 0.25
                  + regular.text_length("Kang", fontsize=name_size))
    one_width = regular.text_length("1", fontsize=superscript_size)
    shift = (gap + name_width + one_width) / 2
    header_size = 9.9626
    header_growth = (regular.text_length("Yang, Xue and Kang", fontsize=header_size)
                     - regular.text_length("Yang and Xue", fontsize=header_size))
    header_gap = 15706 - 1000 * header_growth / header_size
    new_header = (f"-{header_gap:.6f}(Y)100(ang,)-250(Xue)-250(and)-250(Kang)]TJ"
                  .encode("ascii"))
    header_count = author_count = 0
    seen_streams = set()
    for page in revised:
        for xref in page.get_contents():
            require(xref not in seen_streams, "Unexpected shared page content stream")
            seen_streams.add(xref)
            old = revised.xref_stream(xref)
            data = old
            if HEADER_OLD in data:
                data = once(data, HEADER_OLD, new_header)
                header_count += 1
            if b"(Chengshuai)" in data:
                require(page.number == 0, "Unexpected author line outside title page")
                data = once(data, b"123.374 -29.49 Td",
                            f"{123.374 - shift:.6f} -29.49 Td".encode("ascii"))
                # Insert after Ting Xue's affiliation marker. Compensate the
                # following relative move to keep the affiliation/body fixed.
                new_name = (
                    f"0 G/F183 11.9552 Tf {one_width + gap:.6f} -4.34 Td "
                    "[(Dingyi)-250(Kang)]TJ "
                    f"0 G/F183 8.9664 Tf {name_width:.6f} 4.34 Td [(1)]TJ "
                    f"0 G/F183 7.9701 Tf {-153.051 - shift:.6f} -18.91 Td"
                ).encode("ascii")
                data = once(data, b"0 G/F183 7.9701 Tf -153.051 -18.91 Td", new_name)
                author_count += 1
            if data != old:
                revised.update_stream(xref, data)
    require(header_count == 65 and author_count == 1, "Wrong number of author edits")
    metadata = revised.metadata
    metadata["author"] = AUTHORS
    revised.set_metadata(metadata)
    output = revised.tobytes(garbage=0, no_new_id=True)
    reopened = fitz.open(stream=output, filetype="pdf")
    checks = verify(original, reopened)
    if args.replace_original:
        require(hashlib.sha256(args.output.read_bytes()).hexdigest() == ORIGINAL_SHA256,
                "Release PDF changed during validation; refusing to overwrite")
        args.output.write_bytes(output)
    else:
        with args.output.open("xb") as target:
            target.write(output)
    print(json.dumps({"baseline_commit": BASELINE, "original_sha256": ORIGINAL_SHA256,
                      "output_sha256": hashlib.sha256(output).hexdigest(),
                      "output_bytes": len(output), "authors": AUTHORS.split("; "),
                      "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
