#!/usr/bin/env python3
"""DK-02: synchronize the editable author record across the manuscript source.

The public PDF was amended to add a third author, but the LaTeX source was not:
its title page, its running header and its PDF metadata still name two. DK-03's
conversion sets a three-author `pdfauthorlist` for the named build, so today the
metadata and the visible page disagree with each other. This script makes the
source itself the single place the author record lives.

Three places carry it, and all three must agree:

    pdfauthor={...}          PDF metadata - leaks into the file even when the
                             title page is anonymised, so it is the one most
                             often missed
    \\fancyhead[R]{...}       the running header on every page after the first
    the title block           the visible author line and its affiliations

What this script does NOT do is decide the record. Author order, affiliations,
the corresponding author and consent are the authors' to settle; this only
applies a stated record consistently and reports what it changed, so the
proposal is reviewable as a diff rather than as prose.

Usage:
    python3 update_author_record.py --source <dir with main.tex> --outdir <dir>
    python3 update_author_record.py --source <dir> --outdir <dir> --check
"""

from __future__ import annotations

import argparse
import difflib
import re
import shutil
from pathlib import Path

# The record being applied. Every author-bearing string below is derived from
# this one structure, so the three places cannot drift apart again.
AUTHORS = [
    {"name": "Chengshuai Yang", "surname": "Yang", "affiliation": 1,
     "corresponding": True, "email": "spiritai@platformai.org"},
    {"name": "Ting Xue", "surname": "Xue", "affiliation": 1,
     "corresponding": False, "email": None},          # not on record; left unfilled
    {"name": "Dingyi Kang", "surname": "Kang", "affiliation": 2,
     "corresponding": False, "email": "dingyi.kang@utdallas.edu"},
]
AFFILIATIONS = {
    1: "NextGen PlatformAI C Corp, USA",
    2: "University of Texas at Dallas, USA",
}


def author_line() -> str:
    """The visible author line, with affiliation and corresponding markers."""
    parts = []
    for author in AUTHORS:
        marks = str(author["affiliation"])
        if author["corresponding"]:
            marks += ",*"
        parts.append(f"{author['name']}$^{{{marks}}}$")
    return "{\\large " + "\\quad ".join(parts) + "}\\\\[5pt]"


def affiliation_lines() -> list[str]:
    used = sorted({a["affiliation"] for a in AUTHORS})
    return [
        f"{{\\normalsize $^{{{n}}}${AFFILIATIONS[n]}}}\\\\[4pt]"
        for n in used
    ]


def contact_lines() -> list[str]:
    """The correspondence line, then any other author address on record.

    Ting Xue's address is not on record and is left out rather than guessed.
    """
    out = []
    for author in AUTHORS:
        if not author["email"]:
            continue
        mark = "*" if author["corresponding"] else str(author["affiliation"])
        label = "Correspondence: " if author["corresponding"] else ""
        out.append(
            f"{{\\normalsize $^{{{mark}}}${label}"
            f"\\href{{mailto:{author['email']}}}{{{author['email']}}}}}\\\\[4pt]"
        )
    return out


def tmlr_author_block() -> str:
    """The same record in TMLR's \\author format.

    DK-03's conversion replaces the centred title block with this macro, so a
    record applied only to the source never reaches the rendered page. It is
    generated here, from the same structure, rather than written out twice.
    """
    entries = []
    for author in AUTHORS:
        email = f" \\email {author['email']}" if author["email"] else ""
        entries.append(
            f"      \\name {author['name']}{email} \\\\\n"
            f"      \\addr {AFFILIATIONS[author['affiliation']]}"
        )
    return "\\author{\n" + "\n      \\AND\n".join(entries) + "}"


def running_header() -> str:
    """TMLR headers are short: surnames only, serial comma-free."""
    surnames = [a["surname"] for a in AUTHORS]
    if len(surnames) > 2:
        joined = ", ".join(surnames[:-1]) + " and " + surnames[-1]
    else:
        joined = " and ".join(surnames)
    return f"\\fancyhead[R]{{\\small {joined}}}"


def metadata_line() -> str:
    return "  pdfauthor={" + " and ".join(a["name"] for a in AUTHORS) + "},"


def rewrite(text: str) -> tuple[str, list[str]]:
    log: list[str] = []
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    seen_author_line = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("pdfauthor={"):
            out.append(metadata_line())
            log.append("PDF metadata: pdfauthor now lists all three authors")
            i += 1
            continue

        if stripped.startswith("\\fancyhead[R]"):
            out.append(running_header())
            log.append("running header: 'Yang and Xue' -> 'Yang, Xue and Kang'")
            i += 1
            continue

        # The visible author line: a \large block naming the first author.
        if not seen_author_line and "Chengshuai Yang$^" in line:
            seen_author_line = True
            out.append(author_line())
            log.append(
                "title page: added Dingyi Kang as third author, appended to preserve "
                "the existing order"
            )
            i += 1
            # Consume the affiliation and correspondence lines that follow, then
            # re-emit both from the record. Stopping at the affiliations would
            # leave the old correspondence block and drop the contact lines.
            consumed = 0
            while i < len(lines) and re.match(r"\{\\normalsize \$\^", lines[i].strip()):
                consumed += 1
                i += 1
            for affiliation in affiliation_lines():
                out.append(affiliation)
            contacts = contact_lines()
            # The released block left 10pt before the date; keep that gap on
            # whichever line is now last, so the title page spacing is unchanged.
            contacts[-1] = contacts[-1].replace("\\\\[4pt]", "\\\\[10pt]")
            out.extend(contacts)
            on_record = [a["name"] for a in AUTHORS if a["email"]]
            log.append(
                f"title page: {consumed} affiliation/contact line(s) -> "
                f"{len(AFFILIATIONS)} affiliation(s) plus {len(on_record)} contact(s), "
                f"adding {AFFILIATIONS[2]}"
            )
            continue

        out.append(line)
        i += 1

    return "\n".join(out) + "\n", log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", required=True, type=Path, help="directory holding main.tex")
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--check", action="store_true", help="report the diff, write nothing")
    ap.add_argument("--emit-tmlr-author", type=Path,
                    help="also write the record as a TMLR \\author block, for the conversion to read")
    args = ap.parse_args()

    main_tex = args.source / "main.tex"
    original = main_tex.read_text(encoding="utf-8")
    updated, log = rewrite(original)

    print("== author record applied")
    for author in AUTHORS:
        mark = "  (corresponding)" if author["corresponding"] else ""
        email = author["email"] or "no address on record"
        print(f"   {author['name']:<18} {AFFILIATIONS[author['affiliation']]:<34} {email}{mark}")

    print("\n== changes")
    for entry in log:
        print(f"   {entry}")
    if len(log) < 4:
        print("   WARNING: expected four changes; the source may have moved")

    print("\n== diff")
    diff = list(
        difflib.unified_diff(
            original.splitlines(), updated.splitlines(),
            fromfile="main.tex (released)", tofile="main.tex (author record applied)",
            lineterm="", n=1,
        )
    )
    for line in diff:
        print(f"   {line}")

    if args.check:
        return 0

    args.outdir.mkdir(parents=True, exist_ok=True)
    for item in sorted(args.source.iterdir()):
        if item.is_file():
            shutil.copy2(item, args.outdir / item.name)
        elif item.is_dir():
            shutil.copytree(item, args.outdir / item.name, dirs_exist_ok=True)
    (args.outdir / "main.tex").write_text(updated, encoding="utf-8")
    print(f"\n== wrote {args.outdir / 'main.tex'}")

    if args.emit_tmlr_author:
        args.emit_tmlr_author.write_text(tmlr_author_block() + "\n", encoding="utf-8")
        print(f"== wrote {args.emit_tmlr_author}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
