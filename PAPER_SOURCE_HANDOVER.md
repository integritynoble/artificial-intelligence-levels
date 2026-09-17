# Source handover and answers — 2026-09-17

Answers to the four requests about the theory paper: the LaTeX source, the data
package, the figure code, and the three questions about versions and the frontier
model. Everything claimed below was checked against the files on this date; where
something could not be established, it says so instead of guessing.

## 1. LaTeX source, bibliography, figures, appendix

Delivered in [`paper-sources/`](paper-sources/README.md).

- `paper-sources/unified-theory/main.tex` — the whole manuscript in one file
  (SHA-256 `f6565616…`).
- `references.bib` and a pre-built `main.bbl`, so two `pdflatex` passes suffice
  and no BibTeX run is needed.
- `fig_hsc.pdf` and `fig_regime.pdf` — the two figures as published.
- `addenda_v2_5_v2_6.tex` — the last four pages of the v2.6 PDF, transcribed into
  LaTeX.
- `build_arxiv.sh`, `ARXIV.md`, `abstract_arxiv.txt`.

Build check run on 2026-09-17 in an empty directory: **64 pages, 0 undefined
references, 0 overfull boxes**, pdfTeX-1.40.25.

Two things to know before reformatting, both explained in detail in
[`paper-sources/README.md`](paper-sources/README.md):

1. **The v2.6 PDF is a merge, not a build.** Pages 1–65 are a pdfTeX build of
   this manuscript; pages 66–69 are two addenda typeset outside LaTeX and
   appended with `pypdf`. That is why no single `.tex` file reproduces the
   69-page PDF, and why the earlier inventory recorded the source as missing.
2. **This source is ahead of v2.6, not behind it.** Its section list contains
   every section of the v2.6 PDF plus §11.7 "Cumulative structure is typed, not
   universal" — which is the appended v2.6 addendum folded into the body — plus
   §11.9 and a renamed §15.2. Nothing in the v2.6 PDF is absent from it.

The exact working-tree `.tex` that produced pages 1–65 was never committed (it
sits between two commits made on 2026-09-06, 26 minutes apart). It is superseded
rather than lost, and the addenda file preserves the appended pages.

## 2. The data package

`Unified_Intelligence_Paper_Dataset.zip` is now in
[`downloads/`](downloads/Unified_Intelligence_Paper_Dataset.zip) (SHA-256
`decc0d4a…`). This is the archive the paper's data statement names — the same
file shipped as the arXiv ancillary archive. It contains:

- `evidence/harness_scaling_curve/` — 48 episode rows, rung results, resource
  summary, canonical report and the study manifest for the Family A stronger
  curve.
- `evidence/regime_switch/` — the frontier and Haiku per-seed CSVs, the paired
  results and the study manifest.
- `schemas/`, `docs/DATA_DICTIONARY.md`, `docs/PROTOCOL.md`,
  `docs/LIMITATIONS.md`, `checksums.sha256`.
- `tools/analyze.py`, `tools/validate.py`, `tools/build_release.py` — the
  analysis code that recomputes the reported statistics, including the
  continuity-corrected Wald interval quoted in the paper.
- `dependencies/HIL_Coordinate_Benchmark_Datasets_v1_2.zip`.

What it deliberately does not contain, as the paper's data statement says: the
Family B curve, the weaker Family A curve, the paired HG0/HG1 rerun, and the
item generators.

**On repository access:** the manuscript repository
`integritynoble/sarsi-intelligence-level` is **private**, so it cannot be read
without an invitation — granting that is the owner's decision, not something this
handover settles. The material needed for the paper work is published here
instead, which is the narrower and safer route: source, figures, figure data and
the dataset are all in this repository now.

## 3. Figure code and data

Delivered in [`paper-sources/figures/`](paper-sources/figures/README.md):
`make_figures.py` plus `data/` (four CSVs).

```bash
cd paper-sources/figures && python3 make_figures.py --outdir ../unified-theory
```

The regime-switch CSVs are byte-copies of the released evidence files — their
SHA-256 sums match the `source_hashes` recorded in the study manifest. The
harness-scaling CSV transcribes the paper's own two tables, and the one curve
with released per-episode evidence is included beside it for cross-checking.

The original plotting scripts were not archived; `make_figures.py` was written
against the published figures and the released data, so its output is visually
equivalent but not byte-identical. The published figure PDFs remain the
committed ones.

## Question A — is v2.6 the version to submit?

**This is the owner's call; it has not been decided here.** The factual input:

- The scientific content of v2.6 is fully contained in the source now published
  in `paper-sources/`, which additionally carries the typed-cumulative section
  and later corrections.
- Submitting a merged PDF is not possible for TMLR anyway: the submission has to
  be built from source in the TMLR template, and that build will come from this
  manuscript.

So the practical answer is: **prepare the submission from `paper-sources/`, and
treat "v2.6" as the content baseline it already contains.** The version number
printed on the submission is a separate decision — see Question B.

## Question B — the website still shows v2.4

Both numbers are real, and the lower one is the newer text:

| | Number | Date | What it is |
|---|---|---|---|
| Website PDF | v2.4 | 2026-09-07 | The manuscript's own LaTeX build. `build_arxiv.sh` writes the filename `..._v2_4.pdf`. Byte-identical (SHA-256 `99e786ef…`) to a build of the source published here. |
| Release package | v2.6 | 2026-09-06 | A 2026-09-06 build of the same manuscript with two addenda appended. |

The manuscript's build script and the release packaging were numbering
independently: the packaging counted the two addenda as revisions 2.5 and 2.6,
while the build kept writing v2\_4. Nothing was rolled back, and the website is
not showing an older text — it is showing a newer one under a lower number.

Recommended, pending the owner's decision: pick one version number for the
submission edition, and change the title page, the build script's output
filename, the website and the release label together, so the three stop
disagreeing.

## Question C — which frontier model, exactly?

There are two experiments, and the answer differs.

**Regime-switch comparison (the frontier vs. Haiku figure and table): the
frontier executor's model ID was never archived.** `study_manifest.json` in the
released dataset records it explicitly:

```json
"executors": {
  "frontier": { "model_id": null, "executor_version": null,
                "evidence_status": "not_archived" },
  "haiku":    { "model_id": "claude-haiku-4-5", "executor_version": null,
                "evidence_status": "model_archived_executor_version_not_archived" }
}
```

The paper's data statement says the same thing in words: "The frontier executor
label/version is missing from the archived frontier CSV and is not inferred
here." Please keep it that way — do not fill it in from memory or inference. If
a reviewer asks, the honest answer is that the comparison is between two archived
configurations on these instances, with one of them unidentified, which is
already stated as a limitation.

**Harness scaling curve (the three-curve figure): identified, with one part
reconstructed.** From that study's manifest:

- `reported_executor`: **Claude Code 2.1.234**
- `reported_model`: `default`
- `reconstructed_model`: `claude-opus-5`, with
  `reconstructed_model_evidence_status: reconstructed_from_local_transcripts`
- ladder `dli-ladder/HG0-HG3@2026-08-25`, 48 episodes, seeds 0 and 1,
  intervention budget H1, executor timeout 420 s, runtime commit
  `0be289f3668eb9367bdf952367d44d48f7ac3843`.

So "Claude Code 2.1.234 running its default model" is what was recorded;
"claude-opus-5" is a reconstruction from local transcripts, and should be
reported with that qualifier rather than as an archived fact. The Family B
executor is a different vendor's CLI and is deliberately unnamed in the paper,
which states that absolute values are not a claim about any product.

## Not settled by this handover

- Authorship, author order and each author's consent to submit.
- The anonymous TMLR edition (the source is now available to build one; producing
  it is DK-03).
- Any licence grant, journal submission, or publication of material beyond what
  is already in this repository.
