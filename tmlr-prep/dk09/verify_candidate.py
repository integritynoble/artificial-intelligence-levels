#!/usr/bin/env python3
"""DK-09: verify a built submission candidate.

Five checks that a clean build log does not make. Each was chosen because a
defect of that shape actually reached a candidate at some point in this work:

  1. equivalence   the anonymous and named builds carry the same science, and
                   differ only in the author block
  2. geometry      no page has text running into the paper's edge
  3. fonts         every font is embedded, and no glyph is missing
  4. figures       no figure caption or panel label cites an equation number -
                   the figure source hard-codes them and they go stale silently
                   when the manuscript renumbers
  5. anonymity     the submission build names no author, affiliation or address
  6. references    every hand-typed "§N", "Table N", "Figure N" and "Equation (N)"
                   resolves. LaTeX checks \\ref and reports 0 undefined; it never
                   sees a number typed directly into the prose, and this paper
                   types a great many of them

Usage:
    python3 verify_candidate.py --named tmlr_named.pdf --anonymous tmlr_submission.pdf

Exit status is 0 when every check passes and 1 when any reports a finding.
"""

from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import subprocess
import sys

IDENTITY = ["Chengshuai", "Ting Xue", "Dingyi", "Kang", "utdallas",
            "platformai", "NextGen", "Texas at Dallas", "spiritai"]

# The running header of the named build, which is an expected difference.
NAMED_HEADER = re.compile(r"^(Yang|Yang, Xue and Kang)")


def pdftotext(path: pathlib.Path, *extra: str) -> str:
    return subprocess.run(["pdftotext", *extra, str(path), "-"],
                          capture_output=True, text=True).stdout


def normalise(path: pathlib.Path) -> list[str]:
    """Body text, with the parts that legitimately differ removed."""
    out = []
    for line in pdftotext(path, "-layout").splitlines():
        s = line.strip()
        if not s or s.startswith("Under review as submission to TMLR"):
            continue
        if re.fullmatch(r"\d+", s) or NAMED_HEADER.match(s):
            continue
        out.append(re.sub(r"\s+", " ", s))
    return out


def check_equivalence(named: pathlib.Path, anon: pathlib.Path) -> list[str]:
    a, n = normalise(anon), normalise(named)
    diff = [l for l in difflib.unified_diff(a, n, lineterm="", n=0)
            if l[:1] in "+-" and l[:3] not in ("---", "+++")]
    # Every difference must be part of the author block.
    unexplained = [l for l in diff
                   if not any(t.lower() in l.lower() for t in IDENTITY + ["Anonymous authors",
                                                                          "double-blind review"])]
    print(f"1. equivalence: {len(a)} vs {len(n)} lines, {len(diff)} differing, "
          f"{len(unexplained)} not explained by the author block")
    for l in diff:
        print(f"     {l[:100]}")
    return [f"{len(unexplained)} content difference(s) beyond the author block"] if unexplained else []


def check_geometry(pdf: pathlib.Path, margin: float = 18.0) -> list[str]:
    xml = pdftotext(pdf, "-bbox")
    pages = re.findall(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', xml, re.S)
    findings = []
    for i, (w, h, body) in enumerate(pages, 1):
        w, h = float(w), float(h)
        words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">',
                           body)
        if not words:
            findings.append(f"page {i}: no extractable text")
            continue
        if max(float(x2) for _, _, x2, _ in words) > w - margin:
            findings.append(f"page {i}: text within {margin}pt of the right edge")
        if min(float(x1) for x1, _, _, _ in words) < margin:
            findings.append(f"page {i}: text within {margin}pt of the left edge")
    print(f"2. geometry: {len(pages)} pages, {len(findings)} finding(s)")
    for f in findings:
        print(f"     {f}")
    return findings


def check_fonts(pdf: pathlib.Path) -> list[str]:
    rows = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
    not_embedded = [r.split()[0] for r in rows if r.strip() and " no " in r[37:]]
    type3 = [r for r in rows if "Type 3" in r]
    missing = pdftotext(pdf).count("�")
    print(f"3. fonts: {len(rows)} fonts, {len(not_embedded)} not embedded, "
          f"{len(type3)} Type 3, {missing} replacement characters")
    findings = []
    if not_embedded:
        findings.append(f"fonts not embedded: {not_embedded}")
    if missing:
        findings.append(f"{missing} replacement character(s) in the text")
    if type3:
        print("     note: Type 3 fonts come from the matplotlib figures; not fatal, but "
              "they rasterise poorly and some venues discourage them")
    return findings


def check_figure_labels(pdf: pathlib.Path) -> list[str]:
    """Figure panel labels must not cite equation numbers.

    `make_figures.py` hard-codes "Eq. (9)" and "Eq. (10)". Those numbers are
    wrong in every build, and they go stale silently whenever the manuscript
    renumbers, because nothing ties the figure to the equation counter.
    """
    stale = re.findall(r"(?:primitive|curve|panel)[^.\n]{0,40}Eq\.?\s*\(\d+\)",
                       pdftotext(pdf), re.I)
    print(f"4. figure labels: {len(stale)} label(s) citing an equation number")
    for s in stale:
        print(f"     {s}")
    return [f"figure label cites an equation number: {s}" for s in stale]


def check_cross_references(pdf: pathlib.Path) -> list[str]:
    """Hand-typed cross-references, which LaTeX never validates.

    "0 undefined references" covers \\ref only. A prose "§17.3" or "Table 38"
    is just text, and stays wrong silently when the manuscript renumbers - which
    is exactly how the figure's equation numbers went stale.
    """
    text = pdftotext(pdf, "-layout")
    targets = {
        "section": set(re.findall(r"^\s*(\d+(?:\.\d+)*)\s+[A-Z]", text, re.M)),
        "Table": set(re.findall(r"Table (\d+):", text)),
        "Figure": set(re.findall(r"Figure (\d+):", text)),
        "Equation": {n for n in re.findall(r"\((\d+)\)\s*$", text, re.M)},
    }
    cited = {
        "section": set(re.findall(r"§\s?(\d+(?:\.\d+)*)", text)),
        "Table": set(re.findall(r"Tables? (\d+)", text)),
        "Figure": set(re.findall(r"Figures? (\d+)", text)),
        "Equation": set(re.findall(r"(?:Equations?|Eqs?\.?)\s*\((\d+)\)", text)),
    }
    findings = []
    for kind in targets:
        missing = sorted(cited[kind] - targets[kind])
        print(f"   {kind}: {len(cited[kind])} cited, {len(missing)} unresolved")
        for m in missing:
            findings.append(f"{kind} {m} is cited but does not exist")
    return findings


def check_anonymity(pdf: pathlib.Path) -> list[str]:
    text = pdftotext(pdf) + subprocess.run(["pdfinfo", str(pdf)],
                                           capture_output=True, text=True).stdout
    hits = [t for t in IDENTITY if re.search(rf"\b{re.escape(t)}\b", text, re.I)]
    print(f"5. anonymity: {len(hits)} identifying term(s) in text or metadata")
    for h in hits:
        print(f"     {h}")
    return [f"identifying term in the anonymous build: {h}" for h in hits]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--named", required=True, type=pathlib.Path)
    ap.add_argument("--anonymous", required=True, type=pathlib.Path)
    args = ap.parse_args()

    findings: list[str] = []
    findings += check_equivalence(args.named, args.anonymous)
    findings += check_geometry(args.anonymous)
    findings += check_fonts(args.anonymous)
    findings += check_figure_labels(args.anonymous)
    findings += check_anonymity(args.anonymous)
    print("\n6. hand-typed cross-references")
    findings += check_cross_references(args.anonymous)

    print(f"\n{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
