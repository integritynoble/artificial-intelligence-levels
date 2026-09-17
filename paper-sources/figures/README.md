# Figure code and data

```bash
python3 make_figures.py --outdir ../unified-theory     # writes fig_hsc.pdf and fig_regime.pdf
```

Requires `matplotlib` (verified with 3.10.8) and nothing else.

## fig_regime.pdf — held-out RMSE per seed

`data/regime_switch_frontier.csv` and `data/regime_switch_haiku.csv` are copied
**verbatim** from `evidence/regime_switch/` inside
`../../downloads/Unified_Intelligence_Paper_Dataset.zip`. Their SHA-256 sums
match the `source_hashes` recorded in that study's `study_manifest.json`:

| File | SHA-256 |
|---|---|
| `regime_switch_frontier.csv` | `97ac14a02b6ac666f527b3dab1a7ab2d6badba965f4e52c8c8156d15c9ab6c54` |
| `regime_switch_haiku.csv` | `ca95e0f1008280ef49cefad0930bd51185a7669121c37a214467b3d622c7bde8` |

Each row is one seed: the held-out extrapolation RMSE, the pass bar (one quarter
of the nearest-neighbour baseline RMSE), the baseline itself, whether a mechanism
was stated, the exit code and the wall time where it was recorded. A seed passes
when `extrapolation_rmse <= bar` and a mechanism was stated. The plot orders
seeds by the pass bar, draws the baseline and the bar as lines, and marks passes
filled and failures open — 5/12 filled for the frontier executor, 1/12 for
Haiku, which are the counts the paper reports.

Six frontier rows have no wall time, and neither file has a separate
termination-reason field. Those gaps are in the released data and are disclosed
in the paper, not repaired here.

## fig_hsc.pdf — the three harness scaling curves

`data/hsc_curves.csv` holds the twelve (executor, rung) points plotted, with the
raw `HLIS_DI` (success-only primitive, left panel) and the net `HLIS_DI`
(delivered-outcome primitive at ρ=1, right panel). The values are the paper's
own tables — "Three Harness Scaling Curves on ladder dli-ladder/HG0–HG3" and
"Raw and net HLIS_DI per rung" — transcribed to CSV.

Only one of the three curves has released per-episode evidence:
`data/hsc_family_a_stronger_rungs.csv` is the Family A stronger curve's rung
aggregate from `evidence/harness_scaling_curve/rung_results.csv` in the
ancillary archive, and its `hlis_di` column reproduces that curve's raw panel
(93.33, 93.33, 96.67, 96.67). The Family B and Family A weaker curves are
reported in the paper's tables only; their episode rows were not released, so
the plot for those two series is driven by the transcribed table values.

## Provenance of the code

The scripts that produced the published `fig_hsc.pdf` and `fig_regime.pdf` (dated
2026-09-02) were not archived. `make_figures.py` was written on 2026-09-17
against the published figures and the released data: the plotted numbers come
from `data/`, and the styling was matched by eye. Regenerated output is visually
equivalent to the published figures but not byte-identical to them, so the
committed `../unified-theory/fig_*.pdf` are still the published files. Overwrite
them only deliberately — for example when moving to a TMLR template that wants a
different figure width or font.
