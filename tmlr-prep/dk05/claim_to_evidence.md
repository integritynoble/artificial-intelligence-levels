# DK-05 claim-to-evidence table

_Prepared 2026-09-17. Every reported number in the theory paper, its source, and whether it reproduces. Table and section numbers follow the TMLR build (`tmlr-prep/dk03/build/`); v2.6's table numbers are one lower from Table 17 on._

Recomputation: `python3 -B tmlr-prep/dk05/recompute.py --dataset <unpacked archive>`, output in `recompute_log.txt`. The script **reimplements the paper's definitions from the raw rows**; it does not call the archive's own `analyze.py`, because a shared implementation would agree with the paper even if both were wrong. The two agree.

## Summary

| | Count |
|---|---|
| Reported values recomputed from released evidence | **53** |
| Of those, reproducing the printed value | **52** |
| **Individual table cells** checked against the archived CSVs (Tables 34 and 35) | **132**, all agreeing |
| Protocol, run-log and resource claims checked against the manifests and rows | **17**, all agreeing |
| Genuine discrepancies | **1** (§18.4.7's "+3.4") |
| Reported results with no released artifact | 12 groups (listed in §4) |

A second review pass added the 132 cell-level and 13 protocol checks; the first pass had checked only aggregates and headline figures.

## 1. Regime-switch study (§17.10) — archived evidence

Source: `evidence/regime_switch/frontier.csv` and `haiku.csv`, 24 episodes, 12 matched seeds. Both files are **original archived observations**: their hashes match `study_manifest.json`, and a byte comparison against the copies in `paper-sources/figures/data/` shows no difference. Executors: Haiku is `claude-haiku-4-5`; the frontier side's model ID is recorded as `not_archived` and is **not** inferred here.

| Reported | Paper | Recomputed | Status |
|---|---|---|---|
| Frontier passes | 5/12 | 5 | reproduces |
| Haiku passes | 1/12 | 1 | reproduces |
| Paired outcomes | 4 frontier-only, 0 Haiku-only, 1 both-pass, 7 both-fail | same | reproduces |
| Frontier lower RMSE | 11/12 | 11 | reproduces |
| Exact two-sided sign test | p = 0.00635 | 0.0063477 | reproduces |
| Exact two-sided McNemar | p = 0.125 | 0.125 | reproduces |
| Paired pass-rate difference | 33.3 points | 33.333 | reproduces |
| 95% CI (continuity-corrected Wald) | −1.7 to +68.3 | −1.672 to +68.339 | reproduces |
| Median RMSE | 0.639 / 5.112 | 0.6385 / 5.1115 | reproduces |
| Median normalized RMSE | 0.359 / 2.142 | 0.35933 / 2.14205 | reproduces |
| Failures worse than nearest neighbour | 3 frontier, 11 Haiku | 3 / 11 | reproduces |
| Seed 11 after the retraction | passes at 0.021 | 0.021 | reproduces |
| Seed 27 rerun with time to finish | 0.060 | 0.060 | reproduces |

### Cell-level check of the two per-seed tables

Every printed cell of **Table 34** (12 seeds × NN baseline, bar, achieved RMSE, "vs. bar", outcome) and **Table 35** (12 seeds × two verdicts, three RMSE columns, reading) was checked against the archived CSVs: **132 of 132 agree**. The pass rule was applied independently from the manifest (`rmse ≤ 0.25 × nearest-neighbour baseline and mechanism stated`), and it reproduces every verdict, every "vs. bar" ratio, and every outcome label including the three-way split between pass, capability failure and worse-than-baseline.

### Protocol and resource claims

| Claim | Paper | Archive |
|---|---|---|
| Timeout | 7200 s | 7200 |
| Held-out points | 120 | 120 |
| Observed noise | 2% | 0.02 |
| Frontier wall times recorded | six seeds, 1350–4983 s | 6 seeds, 1350–4983 |
| Haiku wall times | 90–376 s | 90–376 |
| All 24 episodes exited 0 with a stated mechanism | yes | yes |
| Seed 12 excluded | yes | `excluded_seed: 12` |
| Harness curve: six task classes, two seeds each, all at H1, twelve episodes per rung | yes | yes |
| No false rejections in any episode | implied by §14.9.2 and Table 41 | all 48 rows are 0 |
| `harness_accepted` null at HG0, where there is no acceptance step | §14.12's required run-log field | all HG0 rows empty |
| Termination reason not archived | disclosed on pp. 60–61 | all 48 rows `not_archived` |
| Table 38's "Attempts" column is harness iterations, not model calls | HG2 prints 15 | 15 iterations against 14 model calls |

All seventeen agree. The last one matters because the two counts differ only at HG2: the paper prints the iteration count, and the archive's `LIMITATIONS.md` explains the gap as one criteria-provider failure before model launch.

## 2. Harness-scaling curve (§18.4) — reconstructed rows, one executor

Source: `evidence/harness_scaling_curve/episodes.csv`, 48 rows. The archive and the paper both state these rows are **reconstructed from the runner's aggregate log**, not archived per episode; the HG0 acceptance verdict and the termination reason were never archived per row. The released curve is **Family A, stronger** only.

| Reported | Paper | Recomputed | Status |
|---|---|---|---|
| A_DI raw per rung | 0.933, 0.933, 0.967, 0.967 | same | reproduces |
| HLIS_DI per rung | 93.3, 93.3, 96.7, 96.7 | same | reproduces |
| Net HLIS_DI at ρ=1 | 86.7, 93.3, 96.7, 96.7 | same | reproduces |
| False completions per rung | 2, 0, 0, 0 | same | reproduces |
| Held back per rung | 0, 2, 1, 1 | same | reproduces |
| Attempts per rung | 12, 12, 15, 14 | same | reproduces |
| Harness Gain, gross / net | 3.3 / 10.0 | 3.333 / 10.0 | reproduces |
| AIL-Ceiling, AIL-AUC | 96.7, 95.0 | same | reproduces |
| Headroom | 6.7 points | 6.667 | reproduces |
| Episodes | 48 | 48 | reproduces |
| **HG1→HG2 rise (§18.4.7)** | **+3.4** | **+3.333** | **differs** |

**The one discrepancy.** §18.4.7 says "two executors rose +3.4 there", while Tables 39 and 40 print the same quantity as 3.3. The rise comes from subtracting the *rounded* rungs (96.7 − 93.3 = 3.4); the unrounded values give 96.667 − 93.333 = 3.333, which correctly prints as 3.3. The tables are right and the sentence is wrong. Proposed correction in the DK-04 change log (item 8).

## 3. Checks possible from the published tables only

Family B and the weaker Family A curve have **no released rows**. Their summaries can still be checked for internal arithmetic consistency against the paper's own tables. This tests arithmetic, not data: it cannot detect a wrong measurement, only a summary inconsistent with its table.

| Curve | Check | Result |
|---|---|---|
| Family B | AUC = mean of rungs (95.0), ceiling (96.7), net gain (10.0) | consistent |
| Family A weaker | AUC (88.8), gain (15.0), ceiling (93.3), net gain (36.6) | consistent |
| Family B | Harness Gain printed 3.3, derived from the rounded rungs 3.4 | the same rounding effect as §18.4.7 |
| Family A weaker | §18.4.5's claim that the HG0→HG1 rise "is a single episode at T2": one T2 episode of two, weighted 4 of 15, moves A_DI by 13.33 points; the printed rise is 13.4 | consistent (same rounding) |

## 4. Reported results with no released artifact

Not reproduced, and none of them can be with what exists today:

| Result | Why not |
|---|---|
| Table 38, Family B curve | no episode rows released; the figure-code CSV transcribes the paper's own table |
| Table 38, Family A weaker curve | same |
| Tables 39, 40: Family B and weaker net figures, gain, AUC, ceiling | same |
| Table 41: paired HG0/HG1 rerun, both executors | §18.4.6; the archive holds the unpaired run only |
| Tables 27, 28, 29, 31, 32: item-family accuracies | generators, reference solvers and specification–key tests not released; the paper says so |
| §17.7: the 1.000 / 0.700 / 0.472 strategy scores | same |
| Table 36: the two library audits | the 45-error run **is** evidenced by `docs/AUDIT_v1_1.md` inside the inherited dependency archive; the 5-error harness-level v1.0 record is not released |
| §16.1: 34 of 224 bound, 30 band-only, 160 specification | the reference library is not released, and these counts appear in no released inventory |
| Table 33: sealed-discovery instance families (6/12 and 0/4) | a different experiment from the regime-switch CSVs; its instances are not released |
| §17.10 intro: the frontier executor passed 7 of 8 delivered seeds | same; these are the earlier single-form families, not the 12 common-protocol seeds |
| §18.4.4: Family B took two to three times the wall-clock per episode | no rows released for Family B |
| §15.3: a class moved 0/2 to 2/2 | no source stated in the paper |
| §1.3, §23, App. D: "the memory ladder is measured at M1" | no M1 method, data or result appears anywhere in the paper |

## 5. Findings for the manuscript

| # | Finding | Proposal |
|---|---|---|
| 1 | §18.4.7's "+3.4" contradicts Tables 39 and 40, which print 3.3. It comes from subtracting rounded values. | Correct the sentence to +3.3 (DK-04 item 8), or report the unrounded 3.33 |
| 2 | The data-availability section claims "per-band success rates … are reported in-line so the reported A_DI can be recomputed by hand from the tables". **No table in the paper carries per-band rates.** They exist only in the released episode rows, and only for one of the three curves. | DK-04 item 6. The per-band surface is now recomputed (§6 below) and could be added as a table, which would make the claim true for the released curve |
| 3 | The same section says "the released episode rows reproduce every entry of Table 38". Table 38 has three executors; the released rows cover one. | Narrow the sentence to the Family A stronger curve |
| 4 | §17.10's statistics reproduce exactly, including the retracted seed 11 and the corrected seed 27. The retraction is honestly reported and checkable. | No change |
| 5 | The frontier executor's identity is `not_archived` in the manifest and is not inferred in the paper. | No change; keep it that way |
| 6 | **The archive carries a resource envelope the paper never prints.** `resource_summary.csv` gives per-rung input, cache and output tokens, tool calls, harness iterations, model calls and runner seconds (4,867 s and 281 tool calls in total), all marked reconstructed from local transcripts. §14.13 requires resource conditions to accompany the score, and §23 lists an incomplete resource envelope as a limitation — yet for this curve the data exists. | Report the envelope for the released curve, or say why not (proposal C5) |

## 6. Per-band surface for the released curve

Recovered from the episode rows. This is the table the paper's reproducibility sentence implies exists.

| Rung | T0 | T1 | T2 | T3 |
|---|---|---|---|---|
| HG0 | 4 ep, 1.000 | 4 ep, 0.500 (2 false-done) | 2 ep, 1.000 | 2 ep, 1.000 |
| HG1 | 4 ep, 1.000 | 4 ep, 0.500 (2 held back) | 2 ep, 1.000 | 2 ep, 1.000 |
| HG2 | 4 ep, 1.000 | 4 ep, 0.750 (1 held back) | 2 ep, 1.000 | 2 ep, 1.000 |
| HG3 | 4 ep, 1.000 | 4 ep, 0.750 (1 held back) | 2 ep, 1.000 | 2 ep, 1.000 |

Weighted by the predeclared schedule (1, 2, 4, 8), these give exactly the A_DI values in Table 38.

**The whole curve turns on one task class.** Of the six classes, only `t1.clean_dataset` ever fails — six failing episodes in 48. Everything else passes at every rung. This also confirms two statements in §18.4.3 that could not be checked before the archive arrived: that the executors "both fail only one class, the T1 data-cleaning task", and that at HG2 and HG3 "A fails seed 0". The released rows show exactly that: `t1.clean_dataset` seed 0 failing at HG2 and HG3, and both seeds failing at HG0 (as false completions) and HG1 (held back).

It also shows how narrow the measurement is: the difference between 93.3 and 96.7 across the whole curve is one episode of one task class.
