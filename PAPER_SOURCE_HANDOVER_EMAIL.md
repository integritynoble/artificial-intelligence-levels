# Handover note to Dingyi Kang — 2026-09-17

_The message sent with the source handover, in English. The detailed version, with
hashes and evidence, is [`PAPER_SOURCE_HANDOVER.md`](PAPER_SOURCE_HANDOVER.md)._

**Subject: Paper source, dataset and figure code are uploaded (with answers to your three questions)**

Hi Dingyi,

Everything you asked for is now in this public repository — clone it or download
from the web interface; no separate access grant is needed:

https://github.com/integritynoble/artificial-intelligence-levels

## 1. LaTeX source (bibliography, figures, appendix)

`paper-sources/unified-theory/`

- `main.tex` — the whole manuscript, one file
- `references.bib` and the pre-built `main.bbl` (arXiv does not run BibTeX, so the
  `.bbl` is included)
- `fig_hsc.pdf`, `fig_regime.pdf` — the two figures used in the text
- `build_arxiv.sh`, `ARXIV.md`, `abstract_arxiv.txt`
- `addenda_v2_5_v2_6.tex` — the last four appendix pages of the v2.6 PDF, in LaTeX

To build: run `pdflatex main.tex` twice (the second pass resolves cross-references
and the table of contents). Verified in an empty directory: **64 pages, no
undefined references, no overfull boxes, no BibTeX run needed.**

Two things to know first, or the files will not line up with the PDF:

- **The v2.6 PDF is not one LaTeX build; it is a merge.** Pages 1–65 are the
  pdfTeX-typeset manuscript, and pages 66–69 (the two addenda) were typeset
  outside LaTeX and appended with pypdf. So no `.tex` file anywhere produces that
  69-page PDF — that is why the earlier record said the source could not be
  found. The original editable file for those four pages was not kept; I
  transcribed the published text into LaTeX sentence by sentence as
  `addenda_v2_5_v2_6.tex`, and the file header says it is a transcription and
  that the PDF is authoritative.
- **The source you are getting is newer than v2.6, not older.** Comparing the
  tables of contents section by section: it has every section v2.6 has, plus
  §11.7 "Cumulative structure is typed, not universal" (that is the appended v2.6
  addendum, now written into the body), plus §11.9, and §15.2 has been renamed.
  So **do not re-append the two addenda when you reformat for TMLR** — the body
  already says it.

The full mapping, the version-numbering explanation and what is still missing are
in `paper-sources/README.md`.

## 2. The dataset

`downloads/Unified_Intelligence_Paper_Dataset.zip` — the ancillary archive the
paper's data statement names. It contains the harness-scaling-curve and
regime-switch evidence, the schemas, `docs/LIMITATIONS.md`, and `tools/analyze.py`
(which recomputes the statistics reported in the paper, including the
continuity-corrected Wald interval).

About access to the `sarsi-intelligence-level` repository: it is private, and it
also holds implementation plans, internal benchmark material and the other six
papers, so it stays closed for now. Everything the paper work needs is in the
public repository above, which should be enough. If you find a specific file
missing, tell me and I will add that file to the public repository.

## 3. Figure code and data

`paper-sources/figures/`. One command redraws both figures:

```bash
cd paper-sources/figures && python3 make_figures.py --outdir ../unified-theory
```

matplotlib is the only dependency. The two regime-switch CSVs in `data/` are
byte-copies from the dataset — their SHA-256 sums match the `source_hashes`
recorded in the study manifest. The harness-scaling CSV transcribes the paper's
two tables, and the one curve that has per-episode evidence released is included
alongside it. One caveat: the original plotting script was not kept, so
`make_figures.py` is a rewrite against the published figures and the released
data. Its output is visually equivalent but not bit-identical, which is why the
repository still ships the original figure PDFs.

## Your three questions

1. **Which version to submit.** Use the source above and reformat it into the
   TMLR template. All of v2.6's scientific content is in it, plus the later
   revisions; and TMLR requires a build from source in any case, so a merged PDF
   could not be submitted.
2. **The website still shows v2.4.** There are two independent numbering lines:
   `build_arxiv.sh` has always named its output `..._v2_4.pdf` (that is the file
   on the website), while the packaging counted the two addenda as revisions 2.5
   and 2.6. **The lower number is the newer text** — nothing was rolled back on
   the website. My suggestion: once the submission version number is decided,
   change the title page, the output filename, the website and the release label
   together.
3. **Which frontier model was used.** Two experiments, two different answers.
   - **The regime-switch comparison (frontier vs. Haiku in the two figures): the
     frontier side's model ID was never archived.** The manifest states it
     plainly: `"frontier": {"model_id": null, "executor_version": null,
     "evidence_status": "not_archived"}`, while the Haiku side is
     `claude-haiku-4-5`. The paper's data statement already says it will not
     infer it. **Please keep it that way — do not fill in a model name after the
     fact.** If a reviewer asks, the honest answer is that this compares two
     archived configurations on these instances with one of them unidentified,
     and that is already recorded as a limitation.
   - **The harness scaling curve (the three-curve figure): this one is on
     record.** The executor is **Claude Code 2.1.234**, the model field is
     `default`, and `claude-opus-5` was reconstructed from local transcripts (the
     manifest marks it `reconstructed_from_local_transcripts`). When you write it
     up, carry the "reconstructed" qualifier with it; it is not an archived fact.
     Family B is a different vendor's CLI and is deliberately unnamed in the
     paper.

The complete answers with their evidence are in `PAPER_SOURCE_HANDOVER.md` in the
repository root, if you need something to cite.

## Still undecided

Author order, each author's contribution statement and consent to submit, and the
anonymous edition (the source now makes it possible; it is DK-03 on your task
list). These need the authors' confirmation first, so please do not submit
anything on anyone's behalf yet.

If anything fails to compile or does not match, send it to me and I will look
into it.

Best regards,
Chengshuai
