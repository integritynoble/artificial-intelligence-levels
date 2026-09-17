# DK-03 section-by-section map: TMLR edition ↔ published v2.6

_Prepared 2026-09-17. TMLR builds: `build/tmlr_submission.pdf` (anonymous, 63 pp.) and `build/tmlr_named.pdf` (named, 63 pp.), generated from `paper-sources/unified-theory` by `convert_to_tmlr.py`. Reference: `papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf` (69 pp.)._

## How to read this map

The conversion happens in two hops, and the second one changes nothing in the body:

```
v2.6 PDF (69 pp.)  --[the owner's newer source]-->  source build (64 pp.)  --[DK-03]-->  TMLR build (63 pp.)
```

- **v2.6 → source** is where the content differences are. All twelve are listed in `tmlr-prep/dk01/content_map.md`; the substantive ones are §11.7 with a new Table 17, §11.9, the §15.2 rename, a sentence added to the abstract, the dropped v2.5 dataset-binding block and the reworded naming note.
- **source → TMLR** changes only the preamble, the title block, the citation style and one equation's line breaking. Body text, section order, table order, figure content, equation numbering and reference count are untouched.

## Section map

Every numbered section and appendix of v2.6 is present in the TMLR build, in the same order and with the same number. The only section-level differences are the ones introduced by the source, not by this conversion:

| v2.6 | TMLR edition | Note |
|---|---|---|
| §1–§11.6 | same numbers | unchanged |
| — | **§11.7 Cumulative structure is typed, not universal** | from the source (the v2.6 addendum, written into the body) |
| §11.7 What the uniform style buys | §11.8 | shifted by the insertion |
| — | **§11.9 The harmonized grammar, and the grid** | from the source |
| §12–§15.1 | same numbers | unchanged |
| §15.2 AIL-Level, AIL-AUC, AIL-Ceiling and Harness Gain | §15.2 The Components of the AI-Level Score: Level, AUC, Ceiling and Harness Gain | renamed in the source; Eq. (19) and §15.4 follow the rename |
| §15.3–§24 | same numbers | unchanged |
| Appendices A–D | Appendices A–D | same titles |
| v2.5 addendum (pp. 66–67), v2.6 addendum (pp. 68–69) | not appended | their content is in the body (§11.7, §11.9 and Table 17); per the handover they are not re-appended. One rule is lost in the process — see DK-01 difference 10 and decision A8 |

## Tables, figures, equations, references

| Item | v2.6 | TMLR edition | Note |
|---|---|---|---|
| Tables | 45 | 46 | +1 from the source (Table 17, "Cumulative structure by object"); **v2.6 Table N ≥ 17 is TMLR Table N+1** |
| Figures | 2 | 2 | same data; Figure 2's panel titles no longer carry stale equation numbers (see below) |
| Numbered equations | 19 | 19 | same numbering; the success-only primitive is (15), the net primitive (16)–(17), the U gates (9)–(10) |
| References | 30 | 30 | same works; **rendered author-year** rather than numeric, because TMLR's style requires it |
| Pages | 69 (incl. 4 addendum pages) | 63 | pagination is not preserved by any reformatting |

## What this conversion changed, and why

| # | Change | Kind | Reason |
|---|---|---|---|
| 1 | `\documentclass[11pt]` + `geometry` → `\documentclass[10pt]` + `\usepackage{tmlr}` | required | the official TMLR template sets its own class options and page geometry |
| 2 | Dropped `mathptmx`, `helvet`, `courier` | required | TMLR uses its own fonts; loading Times fights the template |
| 3 | Dropped the source's `natbib` load and `fancyhdr` running head | required | `tmlr.sty` loads both itself and sets the "Under review as submission to TMLR" head |
| 4 | Centred title block → `\title`/`\author`/`\maketitle`, with hand-set line breaks | required | the TMLR title block is narrower; unbroken lines wrapped badly |
| 5 | `\bibliographystyle{plainnat}` → `{tmlr}` | required | TMLR's citation and reference style. This is why the text now reads "(Amershi et al., 2019)" instead of "[1]" |
| 6 | `pdfauthor` now expands a macro the wrapper defines: empty in the anonymous build | required | otherwise the PDF metadata names the authors, which is a desk-reject risk |
| 7 | The U-gate display (§11.6) set on two aligned lines | layout | it overflowed the narrower TMLR text block by 14.9pt. Same symbols, same values |
| 8 | Figure 2's panel titles: "Success-only primitive, Eq. (9)" → "Success-only primitive"; "Delivered-outcome primitive, Eq. (10), ρ=1" → "Delivered-outcome primitive, ρ=1" | cross-reference repair | (9) and (10) are the U-level gates; the primitives are (15) and (17). The numbers are dropped rather than corrected so they cannot go stale again |
| 9 | Float placement parameters retuned (`topfraction`, `bottomfraction`, `textfraction`, `floatpagefraction`, `topnumber`, `bottomnumber`, `totalnumber`) | layout | LaTeX's defaults left a table-only page and several half-empty ones in the narrower block. Standard parameters; no content moves. Sparse pages 12 → 11, page count 61 → 60 |
| 10 | The title-page date (September 3, 2026) is not carried over | **content dropped** | It lived in the centred title block that `\maketitle` replaces, and the TMLR template has no date field for submissions. Decision **B4** |
| 11 | The correspondence `mailto:` link is gone with that block | consequence of 10 | The anonymous build now has no external links at all, which suits a review copy |
| 12 | The two indicator functions in the U gate: `\mathbb 1` → `\mathds{1}` (loading `dsfont`) | **defect repair** | The AMS blackboard font has no digits, so both printed as a wrong symbol — in the published v2.6 PDF as well. This corrects a defect of the paper, not of the conversion |
| 13 | Floats confined to their own section, subsection and subsubsection (`placeins` plus two barriers) | layout | Without it, tables drifted above their own heading: §6.1, §11.2 and §15.2 each showed a heading with the next heading directly under it. The cost is roughly three pages and a few half-filled ones |

The anonymous and named builds are both 63 pages. **No section, table, figure, equation or reference was cut, relocated or shortened.** The one piece of content that does not survive is the title-page date (change 10), which needs decision B4. No 12-page cap was imposed: the main text plus appendices run to 63 pages, which TMLR permits when the length is justified, though it may lengthen review.

Nothing here is a substantive scientific change. The substantive proposals (DK-01 A8, and DK-04/DK-06 P1–P8) are **not applied**; they wait for the owner's decisions and will be made in one pass.

## Still to do in this edition

| Item | Task |
|---|---|
| Author line, contribution statement, consent | DK-02 — the named build currently lists the three authors in the amended public PDF's order, awaiting confirmation |
| The words `hilbench` and `ailevel` in the naming note | DK-02/DK-07 — searchable project identifiers in an anonymous submission |
| The approved wording changes | applied after the owner decides (DK-04, DK-06) |
| Remaining sparse pages (two wide-table pages) | cosmetic; revisit in DK-09 once the text stops changing |
