# Editable sources for the theory paper

_Added 2026-09-17 to close the DK-01 blocker: "Matching editable v2.6 source was not found in the inspected release."_

This directory holds the LaTeX source, bibliography, figures, figure data and
figure code behind **Unified Intelligence Theory and the Artificial Intelligence
Level**, plus a LaTeX reconstruction of the four appended pages at the end of the
published v2.6 PDF.

| Path | What it is |
|---|---|
| `unified-theory/main.tex` | The manuscript. 208 KB, one file, no `\input` of other bodies. |
| `unified-theory/references.bib` | BibTeX database. |
| `unified-theory/main.bbl` | Pre-built bibliography, so no BibTeX run is needed (arXiv does not run BibTeX). |
| `unified-theory/fig_hsc.pdf`, `unified-theory/fig_regime.pdf` | The two figures, as included by `main.tex`. |
| `unified-theory/addenda_v2_5_v2_6.tex` | **Reconstruction** of pages 66–69 of the v2.6 PDF. See "The last four pages" below. |
| `unified-theory/build_arxiv.sh`, `ARXIV.md`, `abstract_arxiv.txt` | The build script and the arXiv metadata written for this manuscript. |
| `figures/make_figures.py`, `figures/data/` | Code and data that regenerate both figures. |
| `../downloads/Unified_Intelligence_Paper_Dataset.zip` | The ancillary dataset the paper's data statement names. |

## Building

```bash
cd unified-theory
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex      # second pass resolves refs/ToC
```

Verified on 2026-09-17 in an empty directory containing only `main.tex`,
`main.bbl`, `references.bib` and the two figure PDFs: **64 pages, zero undefined
references or citations, zero overfull boxes**, pdfTeX-1.40.25, no BibTeX run.
`build_arxiv.sh` does the same through `latexmk` and then writes the arXiv
tarball and `SHA256SUMS`.

The addenda file builds on its own: `pdflatex addenda_v2_5_v2_6.tex` → 6 pages.

## How this source relates to the published v2.6 PDF

`papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf` is **not** a single
LaTeX build. It is a merge:

- **Pages 1–65** are a pdfTeX-1.40.25 build of this manuscript (fonts:
  NimbusRomNo9L; running header "Yang and Xue").
- **Pages 66–69** are two addenda — "v2.5 Revision Addendum" and "v2.6
  Cumulative-Structure Clarification" — typeset outside LaTeX (fonts: Noto Sans
  and Helvetica) and appended.
- The merged file was written by `pypdf`, which is why the PDF's Producer is
  `pypdf` rather than pdfTeX. (The September 13 author-line amendment used
  `pypdf` again on the same file.)

The `.tex` state that produced pages 1–65 was never committed: it is a working
copy from between two commits of the manuscript repository on 2026-09-06 —
`7800d43` (14:25) and `14a2428` (14:51); the release package
`AI_Level_Research_Package_v2_6_v0_3.zip` was assembled at 14:39. Two sentences
prove it was an intermediate state rather than any committed revision:

- v2.6 page 1 reads "Naming. AI-Level is the current name of this framework and
  its base-model characterization." That sentence appears in no commit of the
  manuscript.
- The abstract sentence "Cumulative structure is typed rather than universal…",
  present in the source shipped here, is absent from v2.6.

**The source shipped here is ahead of the v2.6 PDF, not behind it**, and it is a
superset at section level. Comparing the two tables of contents:

| Section | v2.6 PDF | This source |
|---|---|---|
| 11.7 | — | **Cumulative structure is typed, not universal** (this is the appended v2.6 addendum, folded into the body with its typed-cumulative table, the revised cumulative law, the GP retention rule and `DF(h,p)`) |
| 11.8 | 11.7 What the uniform style buys | What the uniform style buys |
| 11.9 | — | The harmonized grammar, and the grid |
| 15.2 | AIL-Level, AIL-AUC, AIL-Ceiling and Harness Gain | The Components of the AI-Level Score: Level, AUC, Ceiling and Harness Gain (renamed; "AI-Level" is now written in full) |

Every other numbered section and subsection is present in both, in the same
order. No section of the v2.6 PDF is missing here.

Consequences for a TMLR edition:

- Reformatting **this source** preserves the v2.6 scientific content and adds the
  later corrections; it does not lose anything the v2.6 PDF had.
- The appended addenda should **not** simply be re-appended, because §11.7 now
  says the same things in the manuscript's own voice. `addenda_v2_5_v2_6.tex`
  exists so the appended text survives the move and can be compared line by line.

## The last four pages

No editable source for pages 66–69 was found in the manuscript repository, the
release bundles, or the ChatGPT-side working folders that were searched — those
pages were generated outside LaTeX. `unified-theory/addenda_v2_5_v2_6.tex` is a
**faithful transcription of the published text of those pages into LaTeX**: the
wording is the PDF's own, the tables keep their rows and columns, and the plain
ASCII symbol spellings (`=>`, `subset`, `Omega`, `Theta`, `Psi`, `Phi`, `mu`) are
restored to math. It is a reconstruction, and the file says so in its header
comment; treat the published PDF as the authority if the two ever disagree.

## Naming: why the website says v2.4 and the release says v2.6

Two numbering lines have been running in parallel:

- The manuscript's own build writes `Unified_Intelligence_Theory_and_AI_Level_v2_4.pdf`
  (`build_arxiv.sh`), and that file is what ai-level.platformai.org publishes.
- The release packaging that produced `AI_Level_Research_Package_v2_6_v0_3.zip`
  labelled the merged artifact v2.6, counting the two addenda as revisions 2.5
  and 2.6.

So the lower number is the newer text. The website PDF is byte-identical
(SHA-256 `99e786ef…`) to the build of the source in this directory, dated
2026-09-07; the v2.6 body is a 2026-09-06 state of the same manuscript.
Whatever version number the submission edition carries, it should be decided
once and applied to the title page, the filename and the repository at the same
time.

## What is still missing

- The exact working-tree `.tex` of the v2.6 body. It is superseded, not lost:
  every section of it is in this source.
- Original per-episode records behind the two curves that are not in the
  ancillary archive (Family B, the weaker Family A curve, the paired HG0/HG1
  rerun). The paper already states this in its data statement.
- The frontier executor's model ID for the regime-switch study. It was never
  archived; see `../PAPER_SOURCE_HANDOVER.md`.
