#!/usr/bin/env python3
"""Regenerate the two figures of the theory paper from their source data.

    python3 make_figures.py [--outdir ../unified-theory]

Writes fig_hsc.pdf and fig_regime.pdf.

fig_hsc.pdf  (Figure "Harness Scaling Curves")
    Source: data/hsc_curves.csv -- the raw and net HLIS_DI values of the paper's
    tables "Three Harness Scaling Curves" (raw, success-only primitive) and
    "Raw and net HLIS_DI per rung" (net, delivered-outcome primitive at rho=1).
    Only the Family A stronger curve is backed by released per-episode rows
    (data/hsc_family_a_stronger_rungs.csv, from the arXiv ancillary archive);
    the Family B and Family A weaker curves are reported in the paper's tables
    only and their episode rows are not part of the public release.

fig_regime.pdf  (Figure "Held-out RMSE per seed")
    Source: data/regime_switch_frontier.csv and data/regime_switch_haiku.csv,
    copied verbatim from evidence/regime_switch/ in
    Unified_Intelligence_Paper_Dataset.zip. A seed passes when its held-out
    extrapolation RMSE is at or below the bar (one quarter of the
    nearest-neighbour baseline RMSE) and the run stated a mechanism.

This script is a reconstruction: the plots that produced the published PDFs were
not archived, so it was written against the published figures and the released
data. The plotted numbers come from the files in data/; the styling is matched
by eye.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

RUNGS = ["HG0", "HG1", "HG2", "HG3"]

# One style per executor, in the order the legend lists them.
SERIES = [
    ("Family A, stronger", "#1f3757", "o", "-"),
    ("Family B", "#4a7c4e", "s", "--"),
    ("Family A, weaker", "#d4622a", "^", "-"),
]

NAVY = "#1f3757"
ORANGE = "#d4622a"


def _grid(ax):
    ax.set_axisbelow(True)
    ax.grid(True, color="#d9d9d9", linewidth=0.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#4d4d4d")


def read_hsc():
    curves = {name: {} for name, *_ in SERIES}
    with (DATA / "hsc_curves.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            curves[row["executor"]][row["rung"]] = (
                float(row["raw_hlis_di"]),
                float(row["net_hlis_di"]),
            )
    return curves


def read_regime(name):
    rows = []
    with (DATA / name).open(newline="") as fh:
        for row in csv.DictReader(fh):
            rows.append(
                {
                    "seed": int(row["seed"]),
                    "rmse": float(row["extrapolation_rmse"]),
                    "bar": float(row["bar"]),
                    "baseline": float(row["nn_baseline_rmse"]),
                    "passed": row["result"] == "pass",
                }
            )
    return {row["seed"]: row for row in rows}


def fig_hsc(outdir: Path) -> Path:
    curves = read_hsc()
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
    x = range(len(RUNGS))

    for ax, idx, title in (
        (axes[0], 0, "Success-only primitive, Eq. (9)"),
        (axes[1], 1, r"Delivered-outcome primitive, Eq. (10), $\rho=1$"),
    ):
        for name, colour, marker, linestyle in SERIES:
            ys = [curves[name][rung][idx] for rung in RUNGS]
            ax.plot(
                x,
                ys,
                color=colour,
                marker=marker,
                linestyle=linestyle,
                markersize=5,
                linewidth=1.4,
                label=name,
            )
        ax.set_title(title, fontsize=9)
        ax.set_xticks(list(x))
        ax.set_xticklabels(RUNGS, fontsize=8)
        ax.set_xlabel("Harness generation", fontsize=9)
        ax.set_ylim(50, 100)
        ax.tick_params(labelsize=8)
        _grid(ax)

    axes[0].set_ylabel(r"$HLIS_{DI}$", fontsize=9)
    axes[0].legend(loc="lower center", fontsize=8, frameon=False)
    fig.tight_layout()
    out = outdir / "fig_hsc.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def fig_regime(outdir: Path) -> Path:
    frontier = read_regime("regime_switch_frontier.csv")
    haiku = read_regime("regime_switch_haiku.csv")
    seeds = sorted(frontier, key=lambda s: frontier[s]["bar"])
    x = range(len(seeds))

    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    ax.plot(
        x,
        [frontier[s]["baseline"] for s in seeds],
        color="#8c8c8c",
        linestyle=":",
        linewidth=1.2,
        label="Nearest-neighbour baseline",
    )
    ax.plot(
        x,
        [frontier[s]["bar"] for s in seeds],
        color="#1a1a1a",
        linestyle="--",
        linewidth=1.4,
        label="Pass bar (25% of baseline)",
    )

    for rows, colour, marker, label in (
        (frontier, NAVY, "o", "Frontier executor"),
        (haiku, ORANGE, "^", "Haiku executor"),
    ):
        for passed, suffix in ((True, "pass"), (False, "fail")):
            xs = [i for i, s in enumerate(seeds) if rows[s]["passed"] is passed]
            ys = [rows[s]["rmse"] for s in seeds if rows[s]["passed"] is passed]
            ax.scatter(
                xs,
                ys,
                marker=marker,
                s=42,
                linewidths=1.3,
                facecolors=colour if passed else "none",
                edgecolors=colour,
                label=f"{label} ({suffix})",
            )

    ax.set_yscale("log")
    ax.set_ylim(1e-3, 3e3)
    ax.set_xticks(list(x))
    ax.set_xticklabels([str(s) for s in seeds], fontsize=8)
    ax.set_xlabel("Seed (ordered by pass bar)", fontsize=9)
    ax.set_ylabel("Held-out RMSE (log)", fontsize=9)
    ax.tick_params(labelsize=8)
    _grid(ax)
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=3,
        fontsize=7.5,
        frameon=False,
        handletextpad=0.4,
        columnspacing=1.2,
    )
    fig.tight_layout()
    out = outdir / "fig_regime.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--outdir",
        type=Path,
        default=HERE.parent / "unified-theory",
        help="where to write the two PDFs (default: the LaTeX source directory)",
    )
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    for path in (fig_hsc(args.outdir), fig_regime(args.outdir)):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
