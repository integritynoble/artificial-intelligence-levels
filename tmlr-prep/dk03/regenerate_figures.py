#!/usr/bin/env python3
"""DK-03 figure repair: rebuild the harness-curve figure without stale equation numbers.

`paper-sources/figures/make_figures.py` hard-codes the panel titles
"Success-only primitive, Eq. (9)" and "Delivered-outcome primitive, Eq. (10)".
Those numbers are wrong in every build we have: in the published v2.6 PDF and in
the TMLR build alike, the success-only achievement variable is Equation (15) and
the delivered-outcome one is Equation (17), while (9) and (10) are the U-level
gates. The repair drops the numbers instead of correcting them, so the labels
cannot go stale again when the manuscript is renumbered; the surrounding caption
and text already point at the equations.

The upstream script is not modified. A patched copy is written to a temporary
directory and run from there.

Usage:
    python3 regenerate_figures.py --figures <paper-sources/figures> --outdir <build dir>
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPLACEMENTS = [
    ('"Success-only primitive, Eq. (9)"', '"Success-only primitive"'),
    (
        'r"Delivered-outcome primitive, Eq. (10), $\\rho=1$"',
        'r"Delivered-outcome primitive, $\\rho=1$"',
    ),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--figures", required=True, type=Path, help="paper-sources/figures")
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--python", default=sys.executable, help="interpreter that has matplotlib")
    args = ap.parse_args()

    script = (args.figures / "make_figures.py").read_text()
    for old, new in REPLACEMENTS:
        if old not in script:
            raise SystemExit(f"panel title not found, upstream script changed: {old}")
        script = script.replace(old, new)
        print(f"patched panel title: {old} -> {new}")

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(args.figures / "data", work / "data")
        (work / "make_figures.py").write_text(script)
        subprocess.run(
            [args.python, str(work / "make_figures.py"), "--outdir", str(args.outdir)],
            check=True,
            cwd=work,
        )
    print(f"regenerated fig_hsc.pdf and fig_regime.pdf in {args.outdir}")


if __name__ == "__main__":
    main()
