#!/usr/bin/env python3
"""DK-05: recompute the paper's reported numbers from the released archive.

Everything here is computed from the archive's raw rows with a fresh
implementation of the definitions printed in the paper. The archive ships its
own `tools/analyze.py`; this script deliberately does not use it, because a
shared implementation would agree with the paper even if both were wrong. Where
the two disagree, that is itself a finding.

Each comparison names the paper value, the recomputed value and the evidence
class of the underlying rows:

    archived      original archived observations
    reconstructed rows rebuilt from an aggregate log (the paper says so)
    table-only    no artifact released; the paper's own table is the only source

Usage:
    python3 recompute.py --dataset <unpacked Unified_Intelligence_v2_0_Paper_Dataset>
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

# Definitions as printed in the paper (TMLR build numbering).
# Section 18.4: "the predeclared band weights w_T0=1, w_T1=2, w_T2=4, w_T3=8;
# with one intervention budget the v_h term drops out".
T_WEIGHTS = {"T0": 1.0, "T1": 2.0, "T2": 4.0, "T3": 8.0}
RUNGS = ("HG0", "HG1", "HG2", "HG3")
RHO = 1.0  # section 18.4: "at rho = 1"

# Values as printed in the paper, transcribed by hand with their location.
# TMLR build = the source build; v2.6 table numbers are one lower from 17 on.
PAPER = {
    # Table 38 (v2.6 Table 37), Family A stronger - the only curve with released rows
    "hsc.gross.HG0": (0.933, "Table 38, A stronger, A_DI raw"),
    "hsc.gross.HG1": (0.933, "Table 38, A stronger, A_DI raw"),
    "hsc.gross.HG2": (0.967, "Table 38, A stronger, A_DI raw"),
    "hsc.gross.HG3": (0.967, "Table 38, A stronger, A_DI raw"),
    "hsc.hlis.HG0": (93.3, "Table 38, HLIS_DI"),
    "hsc.hlis.HG1": (93.3, "Table 38, HLIS_DI"),
    "hsc.hlis.HG2": (96.7, "Table 38, HLIS_DI"),
    "hsc.hlis.HG3": (96.7, "Table 38, HLIS_DI"),
    "hsc.false_done.HG0": (2, "Table 38, False-done"),
    "hsc.false_done.HG1": (0, "Table 38, False-done"),
    "hsc.false_done.HG2": (0, "Table 38, False-done"),
    "hsc.false_done.HG3": (0, "Table 38, False-done"),
    "hsc.held_back.HG0": (0, "Table 38, Held back"),
    "hsc.held_back.HG1": (2, "Table 38, Held back"),
    "hsc.held_back.HG2": (1, "Table 38, Held back"),
    "hsc.held_back.HG3": (1, "Table 38, Held back"),
    "hsc.attempts.HG0": (12, "Table 38, Attempts"),
    "hsc.attempts.HG1": (12, "Table 38, Attempts"),
    "hsc.attempts.HG2": (15, "Table 38, Attempts"),
    "hsc.attempts.HG3": (14, "Table 38, Attempts"),
    "hsc.episodes": (48, "Table 38 caption, 48 episodes per executor"),
    # Table 39 (v2.6 Table 38), net figures and gain, A stronger
    "hsc.net.HG0": (86.7, "Table 39, A stronger net"),
    "hsc.net.HG1": (93.3, "Table 39, A stronger net"),
    "hsc.net.HG2": (96.7, "Table 39, A stronger net"),
    "hsc.net.HG3": (96.7, "Table 39, A stronger net"),
    "hsc.gain.gross": (3.3, "Table 39/40, Harness Gain, A stronger"),
    "hsc.gain.net": (10.0, "Table 39, Gain, A stronger net"),
    # Table 40 (v2.6 Table 39), curve summaries
    "hsc.ceiling": (96.7, "Table 40, AIL-Ceiling, A stronger"),
    "hsc.auc": (95.0, "Table 40, AIL-AUC, A stronger"),
    "hsc.headroom": (6.7, "section 18.4.2 text: 6.7 points of headroom"),
    # section 18.4.7 text
    "hsc.hg1_hg2_rise": (3.4, "section 18.4.7: 'two executors rose +3.4 there'"),
    # Table 35 (v2.6 Table 34) and section 17.10.2
    "regime.frontier_passes": (5, "section 17.10.2: frontier passed 5/12"),
    "regime.haiku_passes": (1, "section 17.10.2: Haiku passed 1/12"),
    "regime.frontier_lower_rmse": (11, "section 17.10.2: lower RMSE on 11/12"),
    "regime.sign_p": (0.00635, "section 17.10.2 and the abstract"),
    "regime.mcnemar_p": (0.125, "section 17.10.2, abstract, section 23"),
    "regime.diff_points": (33.3, "section 17.10.2: 33.3 percentage points"),
    "regime.ci_lower": (-1.7, "section 17.10.2 and section 23: -1.7 to +68.3"),
    "regime.ci_upper": (68.3, "section 17.10.2 and section 23"),
    "regime.median_rmse_frontier": (0.639, "section 17.10.2"),
    "regime.median_rmse_haiku": (5.112, "section 17.10.2"),
    "regime.median_norm_frontier": (0.359, "section 17.10.2"),
    "regime.median_norm_haiku": (2.142, "section 17.10.2"),
    "regime.frontier_worse_than_nn": (3, "section 17.10.2: three of them extrapolated worse"),
    "regime.haiku_worse_than_nn": (11, "section 17.10.2: all 11 Haiku failures"),
    "regime.both_pass": (1, "section 17.10.2: one both-pass seed (27)"),
    "regime.both_fail": (7, "section 17.10.2: seven both-fail seeds"),
    "regime.frontier_only": (4, "section 17.10.2: four frontier-only passes"),
    "regime.haiku_only": (0, "section 17.10.2: no Haiku-only pass"),
    "regime.episodes": (24, "section 17.10.1: all 24 episodes exited 0"),
    "regime.seed11_rmse": (0.021, "section 17.10 box: 'Seed 11 passes at 0.021'"),
    "regime.seed27_frontier_rmse": (0.060, "section 17.10 box: 'Rerun with time to finish, it passes at 0.060'"),
    # section 14.10 worked example, computed from the printed inputs
    "hlis.example": (74.3, "section 14.10: HLIS = 100 x (0.90 x 0.70 x 0.60 x 0.80 x 0.75)^(1/5)"),
}

EVIDENCE = {
    "hsc": "reconstructed (48 episode rows rebuilt from the runner's aggregate log)",
    "regime": "archived (the two CSVs; hashes match the study manifest)",
    "hlis": "worked example, no measurement",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def exact_two_sided_binomial(successes: int, trials: int) -> float:
    """Exact two-sided binomial test at p = 0.5, summing outcomes no more likely."""
    if trials == 0:
        return 1.0
    observed = math.comb(trials, successes)
    return min(1.0, sum(math.comb(trials, k) for k in range(trials + 1)
                        if math.comb(trials, k) <= observed) / 2 ** trials)


def hsc(dataset: Path) -> dict[str, float]:
    rows = read_csv(dataset / "evidence/harness_scaling_curve/episodes.csv")
    out: dict[str, float] = {"hsc.episodes": len(rows)}
    gross, net = {}, {}
    for rung in RUNGS:
        rung_rows = [r for r in rows if r["rung"] == rung]
        bands: dict[str, list[dict[str, str]]] = defaultdict(list)
        for r in rung_rows:
            bands[r["T_band"]].append(r)

        # A_DI raw: weighted mean over bands of the verifier pass rate
        num = den = 0.0
        for band, brows in bands.items():
            w = T_WEIGHTS[band]
            num += w * sum(int(r["verifier_pass"]) for r in brows) / len(brows)
            den += w
        gross[rung] = num / den

        # A_DI net at rho = 1: delivered-and-correct minus rho x false completions,
        # floored at zero per band (section 14.9.2: "S_net is clamped at zero")
        num = den = 0.0
        for band, brows in bands.items():
            w = T_WEIGHTS[band]
            delivered = sum(1 for r in brows
                            if int(r["verifier_pass"]) and not int(r["held_back"])) / len(brows)
            false_done = sum(int(r["false_completion"]) for r in brows) / len(brows)
            num += w * max(0.0, delivered - RHO * false_done)
            den += w
        net[rung] = num / den

        out[f"hsc.gross.{rung}"] = gross[rung]
        out[f"hsc.hlis.{rung}"] = 100 * gross[rung]
        out[f"hsc.net.{rung}"] = 100 * net[rung]
        out[f"hsc.false_done.{rung}"] = sum(int(r["false_completion"]) for r in rung_rows)
        out[f"hsc.held_back.{rung}"] = sum(int(r["held_back"]) for r in rung_rows)
        out[f"hsc.attempts.{rung}"] = sum(int(r["harness_iterations"]) for r in rung_rows)

    curve = [100 * gross[r] for r in RUNGS]
    net_curve = [100 * net[r] for r in RUNGS]
    out["hsc.gain.gross"] = max(curve) - curve[0]
    out["hsc.gain.net"] = max(net_curve) - net_curve[0]
    out["hsc.ceiling"] = max(curve)
    out["hsc.auc"] = sum(curve) / len(curve)
    out["hsc.headroom"] = 100 - curve[0]
    out["hsc.hg1_hg2_rise"] = curve[2] - curve[1]
    return out


def regime(dataset: Path) -> dict[str, float]:
    base = dataset / "evidence/regime_switch"
    frontier = {int(r["seed"]): r for r in read_csv(base / "frontier.csv")}
    haiku = {int(r["seed"]): r for r in read_csv(base / "haiku.csv")}
    seeds = sorted(set(frontier) & set(haiku))
    out: dict[str, float] = {"regime.episodes": len(frontier) + len(haiku)}

    def passed(row: dict[str, str]) -> bool:
        # study_manifest.json pass_rule: rmse <= 0.25 x nn baseline and mechanism stated
        return (float(row["extrapolation_rmse"]) <= 0.25 * float(row["nn_baseline_rmse"])
                and int(row["mechanism_stated"]) == 1)

    fp = [s for s in seeds if passed(frontier[s])]
    hp = [s for s in seeds if passed(haiku[s])]
    out["regime.frontier_passes"] = len(fp)
    out["regime.haiku_passes"] = len(hp)
    out["regime.frontier_only"] = len([s for s in seeds if s in fp and s not in hp])
    out["regime.haiku_only"] = len([s for s in seeds if s in hp and s not in fp])
    out["regime.both_pass"] = len([s for s in seeds if s in fp and s in hp])
    out["regime.both_fail"] = len([s for s in seeds if s not in fp and s not in hp])

    f_rmse = [float(frontier[s]["extrapolation_rmse"]) for s in seeds]
    h_rmse = [float(haiku[s]["extrapolation_rmse"]) for s in seeds]
    nn = [float(frontier[s]["nn_baseline_rmse"]) for s in seeds]
    lower = sum(1 for a, b in zip(f_rmse, h_rmse) if a < b)
    out["regime.frontier_lower_rmse"] = lower
    out["regime.sign_p"] = exact_two_sided_binomial(lower, sum(1 for a, b in zip(f_rmse, h_rmse) if a != b))

    b = out["regime.frontier_only"]
    c = out["regime.haiku_only"]
    out["regime.mcnemar_p"] = exact_two_sided_binomial(int(b), int(b + c))
    n = len(seeds)
    diff = (b - c) / n
    se = math.sqrt((b + c) - (b - c) ** 2 / n) / n
    out["regime.diff_points"] = 100 * diff
    out["regime.ci_lower"] = 100 * (diff - 1.96 * se - 1 / n)
    out["regime.ci_upper"] = 100 * (diff + 1.96 * se + 1 / n)

    out["regime.median_rmse_frontier"] = statistics.median(f_rmse)
    out["regime.median_rmse_haiku"] = statistics.median(h_rmse)
    out["regime.median_norm_frontier"] = statistics.median([a / b for a, b in zip(f_rmse, nn)])
    out["regime.median_norm_haiku"] = statistics.median([a / b for a, b in zip(h_rmse, nn)])
    out["regime.frontier_worse_than_nn"] = sum(
        1 for s in seeds if s not in fp and float(frontier[s]["extrapolation_rmse"]) > float(frontier[s]["nn_baseline_rmse"]))
    out["regime.haiku_worse_than_nn"] = sum(
        1 for s in seeds if s not in hp and float(haiku[s]["extrapolation_rmse"]) > float(haiku[s]["nn_baseline_rmse"]))
    out["regime.seed11_rmse"] = float(frontier[11]["extrapolation_rmse"])
    out["regime.seed27_frontier_rmse"] = float(frontier[27]["extrapolation_rmse"])
    return out


def per_band_surface(dataset: Path) -> dict[str, dict[str, dict[str, float]]]:
    """Per-band pass rates for the released curve.

    The data-availability section claims per-band success rates are "reported
    in-line so the reported A_DI can be recomputed by hand from the tables".
    No table in the paper carries them; they are recoverable only from these
    episode rows, and only for this one executor.
    """
    rows = read_csv(dataset / "evidence/harness_scaling_curve/episodes.csv")
    surface: dict[str, dict[str, dict[str, float]]] = {}
    for rung in RUNGS:
        rung_rows = [r for r in rows if r["rung"] == rung]
        bands: dict[str, list[dict[str, str]]] = defaultdict(list)
        for r in rung_rows:
            bands[r["T_band"]].append(r)
        surface[rung] = {
            band: {
                "episodes": len(brows),
                "pass_rate": sum(int(r["verifier_pass"]) for r in brows) / len(brows),
                "false_completions": sum(int(r["false_completion"]) for r in brows),
                "held_back": sum(int(r["held_back"]) for r in brows),
            }
            for band, brows in sorted(bands.items())
        }
    return surface


# Reported results with no released artifact. Listed so that "not reproduced" is
# explicit rather than an omission.
NOT_REPRODUCIBLE = [
    ("Table 38, Family B curve (all four rungs)", "no episode rows released; the figure CSV transcribes the paper's own table"),
    ("Table 38, Family A weaker curve (all four rungs)", "same"),
    ("Table 39/40, Family B and weaker net figures, gain, AUC, ceiling", "same"),
    ("Table 41, paired HG0/HG1 rerun (both executors)", "section 18.4.6; the archive holds the unpaired run only"),
    ("Tables 27, 28, 29, 31, 32: item-family accuracies", "generators, reference solvers and specification-key tests not released (the paper says so)"),
    ("Section 17.7: 1.000 / 0.700 / 0.472 strategy scores", "same"),
    ("Table 33: sealed-discovery instance families against a single-form fit (6/12 and 0/4)",
     "a different experiment from the regime-switch CSVs; its instances are not released"),
    ("Section 17.10 intro: the frontier executor passed 7 of 8 seeds it delivered",
     "same; these are the earlier single-form families, not the 12 common-protocol seeds"),
    ("Table 36: the two library audits (5 and 45 errors)", "the 45-error run is evidenced by docs/AUDIT_v1_1.md in the inherited dependency; the 5-error harness-level v1.0 record is not released"),
    ("Section 16.1: 34 of 224 bound, 30 band-only, 160 specification", "the reference library is not released; these counts appear in no released inventory"),
    ("Section 15.3: a class moved 0/2 to 2/2", "no source stated in the paper"),
    ("Sections 1.3, 23, appendix D: 'the memory ladder is measured at M1'", "no M1 method, data or result appears anywhere in the paper"),
    ("Section 18.4.4: Family B took two to three times the wall-clock per episode", "no rows released for Family B"),
]


# Internal-consistency checks computed only from the paper's own printed tables,
# for the two curves with no released rows. These test arithmetic, not data: they
# cannot detect a wrong measurement, only a summary inconsistent with its table.
TABLE_ONLY = {
    "Family B": {"curve": [93.3, 93.3, 96.7, 96.7], "net": [86.7, 93.3, 96.7, 96.7],
                 "auc": 95.0, "gain": 3.3, "net_gain": 10.0, "ceiling": 96.7},
    "Family A weaker": {"curve": [78.3, 91.7, 91.7, 93.3], "net": [56.7, 91.7, 91.7, 93.3],
                        "auc": 88.8, "gain": 15.0, "net_gain": 36.6, "ceiling": 93.3},
}


def table_only_checks() -> list[tuple[str, str, float, float, bool]]:
    results = []
    for name, t in TABLE_ONLY.items():
        checks = [
            ("AIL-AUC = mean of the four rungs", t["auc"], sum(t["curve"]) / 4),
            ("Harness Gain = ceiling - HG0", t["gain"], max(t["curve"]) - t["curve"][0]),
            ("AIL-Ceiling = max rung", t["ceiling"], max(t["curve"])),
            ("net gain = net ceiling - net HG0", t["net_gain"], max(t["net"]) - t["net"][0]),
        ]
        for label, printed, derived in checks:
            results.append((name, label, printed, derived, abs(printed - derived) <= 0.05 + 1e-9))
    # section 18.4.5: the weaker executor's HG0 -> HG1 rise is "a single episode at T2"
    printed = 91.7 - 78.3
    one_t2_episode = 100 * (T_WEIGHTS["T2"] * 0.5) / sum(T_WEIGHTS.values())
    results.append(("Family A weaker", "HG0->HG1 rise equals one T2 episode flipping",
                    printed, one_t2_episode, abs(printed - one_t2_episode) <= 0.05 + 1e-9))
    return results


# Table 34 as printed: seed, NN baseline, bar (25%), achieved RMSE, "vs. bar", outcome.
TABLE_34 = [
    (11, 0.174, 0.043, 0.021, 0.5, "pass"),
    (40, 1.271, 0.318, 0.003, 0.01, "pass"),
    (27, 3.737, 0.934, 0.060, 0.06, "pass"),
    (50, 1.573, 0.393, 0.093, 0.24, "pass"),
    (9, 1.210, 0.303, 0.276, 0.9, "pass"),
    (38, 0.689, 0.172, 0.455, 2.6, "capability failure"),
    (44, 2.521, 0.630, 0.822, 1.3, "capability failure"),
    (25, 1.543, 0.386, 0.874, 2.3, "capability failure"),
    (17, 2.705, 0.676, 1.062, 1.6, "capability failure"),
    (0, 1.030, 0.258, 1.087, 4.2, "worse than the baseline"),
    (41, 1.579, 0.395, 1.743, 4.4, "worse than the baseline"),
    (24, 2.321, 0.580, 2.453, 4.2, "worse than the baseline"),
]

# Table 35 as printed: seed, frontier verdict, haiku verdict, frontier RMSE, haiku RMSE, NN RMSE, reading.
TABLE_35 = [
    (0, "fail", "fail", 1.087, 1.045, 1.030, "both fail"),
    (9, "pass", "fail", 0.276, 2.586, 1.210, "frontier-only"),
    (11, "pass", "fail", 0.021, 5.240, 0.174, "frontier-only"),
    (17, "fail", "fail", 1.062, 5.698, 2.705, "both fail"),
    (24, "fail", "fail", 2.453, 4.983, 2.321, "both fail"),
    (25, "fail", "fail", 0.874, 10.600, 1.543, "both fail"),
    (27, "pass", "pass", 0.060, 0.758, 3.737, "both pass"),
    (38, "fail", "fail", 0.455, 1.234, 0.689, "both fail"),
    (40, "pass", "fail", 0.003, 1187.885, 1.271, "frontier-only"),
    (41, "fail", "fail", 1.743, 6.287, 1.579, "both fail"),
    (44, "fail", "fail", 0.822, 4.109, 2.521, "both fail"),
    (50, "pass", "fail", 0.093, 6.192, 1.573, "frontier-only"),
]

# Protocol and resource claims stated in prose.
PROSE_CLAIMS = [
    ("timeout is 7200 seconds", "timeout_seconds", 7200),
    ("120 held-out points", "held_out_points", 120),
    ("noise fraction 0.02", "observed_noise_fraction", 0.02),
]


def per_seed_tables(dataset: Path) -> list[tuple[str, int, str, object, object, bool]]:
    """Check every printed cell of Tables 34 and 35 against the archived CSVs."""
    base = dataset / "evidence/regime_switch"
    frontier = {int(r["seed"]): r for r in read_csv(base / "frontier.csv")}
    haiku = {int(r["seed"]): r for r in read_csv(base / "haiku.csv")}
    close = lambda a, b, d=3: abs(float(a) - float(b)) <= 0.5 * 10 ** -d + 1e-9
    rows = []

    for seed, nn, bar, achieved, vs_bar, outcome in TABLE_34:
        f = frontier[seed]
        rows.append(("T34 NN baseline", seed, "nn_baseline_rmse", nn, float(f["nn_baseline_rmse"]),
                     close(nn, f["nn_baseline_rmse"])))
        rows.append(("T34 bar = 25% of baseline", seed, "0.25 x nn", bar, 0.25 * float(f["nn_baseline_rmse"]),
                     close(bar, 0.25 * float(f["nn_baseline_rmse"]), 3)))
        rows.append(("T34 achieved RMSE", seed, "extrapolation_rmse", achieved, float(f["extrapolation_rmse"]),
                     close(achieved, f["extrapolation_rmse"])))
        ratio = float(f["extrapolation_rmse"]) / (0.25 * float(f["nn_baseline_rmse"]))
        decimals = len(str(vs_bar).split(".")[1])
        rows.append(("T34 vs. bar", seed, "achieved / bar", vs_bar, ratio,
                     abs(ratio - vs_bar) <= 0.5 * 10 ** -decimals + 1e-9))
        passed = (float(f["extrapolation_rmse"]) <= 0.25 * float(f["nn_baseline_rmse"])
                  and int(f["mechanism_stated"]) == 1)
        worse = float(f["extrapolation_rmse"]) > float(f["nn_baseline_rmse"])
        derived = "pass" if passed else ("worse than the baseline" if worse else "capability failure")
        rows.append(("T34 outcome", seed, "pass rule + baseline comparison", outcome, derived, derived == outcome))

    for seed, fv, hv, frmse, hrmse, nn, reading in TABLE_35:
        f, h = frontier[seed], haiku[seed]
        fp = (float(f["extrapolation_rmse"]) <= 0.25 * float(f["nn_baseline_rmse"])
              and int(f["mechanism_stated"]) == 1)
        hp = (float(h["extrapolation_rmse"]) <= 0.25 * float(h["nn_baseline_rmse"])
              and int(h["mechanism_stated"]) == 1)
        rows.append(("T35 frontier verdict", seed, "pass rule", fv, "pass" if fp else "fail", (fv == "pass") == fp))
        rows.append(("T35 haiku verdict", seed, "pass rule", hv, "pass" if hp else "fail", (hv == "pass") == hp))
        rows.append(("T35 frontier RMSE", seed, "extrapolation_rmse", frmse, float(f["extrapolation_rmse"]),
                     close(frmse, f["extrapolation_rmse"])))
        rows.append(("T35 haiku RMSE", seed, "extrapolation_rmse", hrmse, float(h["extrapolation_rmse"]),
                     close(hrmse, h["extrapolation_rmse"])))
        rows.append(("T35 NN RMSE", seed, "nn_baseline_rmse", nn, float(f["nn_baseline_rmse"]),
                     close(nn, f["nn_baseline_rmse"])))
        derived_reading = ("both pass" if fp and hp else "frontier-only" if fp
                           else "haiku-only" if hp else "both fail")
        rows.append(("T35 reading", seed, "from the two verdicts", reading, derived_reading,
                     derived_reading == reading))
    return rows


def prose_claims(dataset: Path) -> list[tuple[str, object, object, bool]]:
    manifest = json.loads((dataset / "evidence/regime_switch/study_manifest.json").read_text())
    out = []
    for label, key, printed in PROSE_CLAIMS:
        out.append((label, printed, manifest[key], manifest[key] == printed))

    base = dataset / "evidence/regime_switch"
    frontier = read_csv(base / "frontier.csv")
    haiku = read_csv(base / "haiku.csv")
    f_times = [float(r["seconds"]) for r in frontier if r["seconds"].strip()]
    h_times = [float(r["seconds"]) for r in haiku if r["seconds"].strip()]
    out.append(("frontier wall times recorded on six seeds", 6, len(f_times), len(f_times) == 6))
    out.append(("frontier wall-time range 1350-4983 s", (1350.0, 4983.0), (min(f_times), max(f_times)),
                (min(f_times), max(f_times)) == (1350.0, 4983.0)))
    out.append(("Haiku wall-time range 90-376 s", (90.0, 376.0), (min(h_times), max(h_times)),
                (min(h_times), max(h_times)) == (90.0, 376.0)))
    # harness-curve protocol claims (section 18.4)
    rows = read_csv(dataset / "evidence/harness_scaling_curve/episodes.csv")
    classes = sorted({r["task_class"] for r in rows})
    seeds = sorted({int(r["seed"]) for r in rows})
    budgets = {r["H_budget"] for r in rows}
    out.append(("six task classes", 6, len(classes), len(classes) == 6))
    out.append(("two seeds per class", [0, 1], seeds, seeds == [0, 1]))
    out.append(("all runs at H1", {"H1"}, budgets, budgets == {"H1"}))
    out.append(("twelve episodes per rung", {12}, {sum(1 for r in rows if r["rung"] == g) for g in RUNGS},
                {sum(1 for r in rows if r["rung"] == g) for g in RUNGS} == {12}))
    out.append(("seed 12 excluded from the regime study",
                12, json.loads((dataset / "evidence/regime_switch/study_manifest.json").read_text())["excluded_seed"]["seed"],
                json.loads((dataset / "evidence/regime_switch/study_manifest.json").read_text())["excluded_seed"]["seed"] == 12))

    # run-log fields the paper's own reporting standard requires (sections 14.12, 17.11)
    out.append(("no false rejections in any episode", {0}, {int(r["false_rejection"]) for r in rows},
                {int(r["false_rejection"]) for r in rows} == {0}))
    accepted = {r["harness_accepted"] for r in rows if r["rung"] == "HG0"}
    out.append(("harness_accepted null at HG0 (no acceptance step)", {""}, accepted, accepted == {""}))
    reasons = {r["termination_reason"] for r in rows}
    out.append(("termination reason not archived, as disclosed", {"not_archived"}, reasons,
                reasons == {"not_archived"}))
    # Table 38's "Attempts" column: harness iterations, not model calls. They differ at HG2.
    iters = {g: sum(int(r["harness_iterations"]) for r in rows if r["rung"] == g) for g in RUNGS}
    calls = {g: sum(int(r["model_calls"]) for r in rows if r["rung"] == g) for g in RUNGS}
    out.append(("Attempts column = harness iterations (HG2: 15, not the 14 model calls)",
                (15, 14), (iters["HG2"], calls["HG2"]), (iters["HG2"], calls["HG2"]) == (15, 14)))

    codes = {int(r["exit_code"]) for r in frontier + haiku}
    out.append(("all 24 episodes exited 0", {0}, codes, codes == {0}))
    stated = {int(r["mechanism_stated"]) for r in frontier + haiku}
    out.append(("all 24 stated a mechanism", {1}, stated, stated == {1}))
    return out


def worked_example() -> dict[str, float]:
    values = [0.90, 0.70, 0.60, 0.80, 0.75]
    return {"hlis.example": 100 * math.prod(values) ** (1 / len(values))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, type=Path)
    ap.add_argument("--json", type=Path, help="also write the recomputed values here")
    args = ap.parse_args()

    got = {**hsc(args.dataset), **regime(args.dataset), **worked_example()}

    width = max(len(k) for k in PAPER)
    print(f"{'quantity'.ljust(width)}  {'paper':>10}  {'recomputed':>12}  verdict   evidence / source")
    print("-" * (width + 78))
    agree = differ = 0
    for key, (paper_value, where) in PAPER.items():
        value = got.get(key)
        if value is None:
            print(f"{key.ljust(width)}  {paper_value:>10}  {'not computed':>12}  -")
            continue
        # Agreement means the recomputed value rounds to what the paper prints, at
        # the precision the paper prints. Half-way cases count as agreement: 0.6385
        # printed as 0.639 is correct rounding, and binary floats put such values a
        # hair either side of the boundary.
        decimals = len(str(paper_value).split(".")[1]) if "." in str(paper_value) else 0
        ok = abs(value - float(paper_value)) <= 0.5 * 10 ** -decimals + 1e-9
        agree += ok
        differ += not ok
        klass = EVIDENCE[key.split(".")[0]]
        print(f"{key.ljust(width)}  {paper_value:>10}  {value:>12.5g}  {'match' if ok else 'DIFFERS':<8}  {klass.split(' (')[0]}  [{where}]")
    print("-" * (width + 78))
    print(f"{agree} of {agree + differ} reported values reproduce from the archive.")

    print("\n== per-band surface for the released curve (Family A, stronger)")
    print("   the paper claims these rates are reported in-line; no table carries them")
    surface = per_band_surface(args.dataset)
    print(f"   {'rung':<6} {'band':<5} {'episodes':>9} {'pass rate':>10} {'false-done':>11} {'held back':>10}")
    for rung, bands in surface.items():
        for band, stats in bands.items():
            print(f"   {rung:<6} {band:<5} {stats['episodes']:>9} {stats['pass_rate']:>10.3f}"
                  f" {stats['false_completions']:>11} {stats['held_back']:>10}")

    print("\n== every printed cell of the two per-seed tables, against the archived CSVs")
    cells = per_seed_tables(args.dataset)
    bad_cells = [c for c in cells if not c[-1]]
    print(f"   {len(cells) - len(bad_cells)} of {len(cells)} cells agree")
    for what, seed, how, printed, derived, ok in bad_cells:
        print(f"   MISMATCH {what} seed {seed}: printed {printed}, from {how} {derived}")

    print("\n== protocol and resource claims stated in prose")
    for label, printed, found, ok in prose_claims(args.dataset):
        print(f"   {'ok ' if ok else 'BAD'} {label:<44} paper {printed}  archive {found}")

    print("\n== internal consistency of the two curves with no released rows")
    print("   computed from the paper's printed tables only; this checks arithmetic, not data")
    for name, label, printed, derived, ok in table_only_checks():
        # a gap of about 0.07 is the signature of subtracting two values that were
        # already rounded to one decimal, not of a wrong figure
        tag = "ok " if ok else ("rnd" if abs(printed - derived) <= 0.1 + 1e-9 else "BAD")
        print(f"   {tag} {name:<16} {label:<44} printed {printed:>6.1f} derived {derived:>7.3f}")
    print("   ok = agrees; rnd = differs only because the printed inputs are already rounded")
    print("   (this is the source of the '+3.4' in section 18.4.7: 96.7 - 93.3 = 3.4, but the")
    print("   unrounded rungs give 96.667 - 93.333 = 3.333, which the tables print as 3.3)")

    print("\n== reported results with no released artifact (not reproduced)")
    for what, why in NOT_REPRODUCIBLE:
        print(f"   - {what}\n       {why}")
    if args.json:
        args.json.write_text(json.dumps(got, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
