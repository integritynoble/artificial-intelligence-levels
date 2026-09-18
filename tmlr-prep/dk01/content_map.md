# DK-01 content map — recovered source vs. published v2.6 PDF

_Prepared 2026-09-17. Source: `paper-sources/unified-theory/main.tex` (SHA-256 `f6565616…ba60c`, commit `de19f09`). Reference: `papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf` (SHA-256 `eda9c513…a94aef`). Comparison is between the **three-pass build of the source** (64 pp.) and the **published PDF** (69 pp.)._

## 1. Document structure

| | Published v2.6 PDF | Recovered source build |
|---|---|---|
| Composition | Three documents merged with pypdf: LaTeX body pp. 1–65, "v2.5 Revision Addendum" pp. 66–67, "v2.6 Cumulative-Structure Clarification" pp. 68–69 | One `pdflatex` build, 64 pp. |
| Producer | pypdf (after the author-only amendment) | pdfTeX-1.40.27 |
| Author line | Chengshuai Yang, Ting Xue, Dingyi Kang (amended) | Chengshuai Yang, Ting Xue — **Dingyi Kang missing** (DK-02) |
| Running header | "Yang, Xue and Kang" | "Yang and Xue" (DK-02) |
| PDF metadata | Author: all three | `pdfauthor={Chengshuai Yang and Ting Xue}` (DK-02) |
| Title-page date | September 3, 2026 | September 3, 2026 |

**No `.tex` file produces the 69-page PDF.** The source is a *superset of the body* plus the v2.6 addendum content written into the text; pagination therefore differs by design.

## 2. Accounting for the two addenda

All 13 numbered addendum sections are traced, not only the ones named in the handover.

**v2.5 Revision Addendum (published pp. 66–67)**

| Section | Where it is in the source | Status |
|---|---|---|
| §1 Authority and current naming | The body's own "Naming" note, which instead explains the earlier HIL name | **Reworded** (difference 4) |
| §2 One experimental grammar for every ladder (10-field record) + "Generic certification form" | **§11.9** "The harmonized grammar, and the grid"; the certification law is item 5 of the §11 schema box | Accounted for |
| §3 Ladder-specific interpretation (per-object table) | §11.1–§11.6 with their per-ladder tables (C, SA, O, the (T,H) surface, HG, U) | Accounted for |
| §4 Operational Self-Awareness is fully grounded | §7 (SA levels) and §11.2 (SA factors with control arms) | Accounted for |
| §5 GUI cognition remains inside Cognitive Intelligence | §4.1 (C^GUI witnesses, GP subscale, oracle-screen / perfect-actuator arms) | Accounted for |
| §6 Dataset binding + the v0.2 identifiers | **Not present** | **Dropped** (difference 5) |

**v2.6 Cumulative-Structure Clarification (published pp. 68–69)**

| Section | Where it is in the source | Status |
|---|---|---|
| §1 Cumulative structure is typed, not universal | **§11.7** + the new **Table 17** "Cumulative structure by object" | Accounted for |
| §2 Revised general cumulative law (`K_X,<k = ∏ K_X,j`, `q*_X,k = min_{j≤k} q_X,j`) | §11.7, one paragraph, including the T/H exception and the measurement-contract refusals | Accounted for |
| §3 Cognitive Intelligence C remains cumulative | **Partly.** The qualitative half is in §11.7 ("a domain-specific C, including C^GUI, inherits the ordinary C retention gate rather than creating a second ladder") and §11.1 ("the same gate is instantiated once per domain of D_C"). The **continuous per-domain rule is missing**: the addendum states `q*_{C,k,d} = min_{j≤k} q_{C,j,d}` with domain aggregation performed *after* within-domain retention; nothing in the source says this, and Eq. (14) is scoped to `d ∈ {I,O,SA}`. | **Gap** (difference 9) |
| §4 GP becomes a cumulative diagnostic sub-ladder | Table 17 (GP0–GP5 row) and §11.7 | Accounted for |
| §5 Delegation is cumulative as a frontier, not a T ladder | Table 17 (DI row, with the cumulative `DF` formula) and §11.4 | Accounted for, though §11.4's own formula omits the retention (DK-06 proposal P2) |
| §6 HG is cumulative engineering; U is cumulative integration | Table 17 (HG and U rows), §11.5, §11.6 | Accounted for |
| §7 Consequence for measurement and datasets | §11.7's closing sentences on what the measurement contract records and refuses | Accounted for |

| Also | |
|---|---|
| Standalone transcription of published pp. 66–69 | `addenda_v2_5_v2_6.tex` (builds on its own to 6 pp.; not `\input` by `main.tex`). Reference copy only; the published PDF stays authoritative |

**Per the handover, do not re-append the addenda in the TMLR edition** — the body carries all of the above except v2.5 §6 (deliberately dropped) and the one rule noted in v2.6 §3.

## 2b. Abstract and front matter

| Item | Result |
|---|---|
| Abstract | **Changed**: one sentence added, nothing removed (word-level similarity 0.912, insertions only). The new sentence is "Cumulative structure is typed rather than universal: retention for the capability ladders C, I, M, O, SA_{1:Ω}, U and the GP diagnostic, a frontier for delegation across T at fixed H and p, nesting for the harness generations, and none for the T and H axes." — the §11.7 material summarized for the abstract. |
| "Naming" note under the abstract | Changed (see difference 4) |
| Keywords, title, subtitle, affiliation, correspondence address, date | Identical to v2.6 |
| Author line, running header, PDF metadata | Two authors (DK-02) |
| Appendices | A–D present in both, same titles |

## 3. Sections

80 contents entries in the source build vs 78 in v2.6. **Every v2.6 section, subsection and appendix is present.**

| Change | Detail |
|---|---|
| New | **§11.7** "Cumulative structure is typed, not universal" (the v2.6 addendum, in the body) |
| New | **§11.9** "The harmonized grammar, and the grid" |
| Renamed | v2.6 §15.2 "AIL-Level, AIL-AUC, AIL-Ceiling and Harness Gain" → **§15.2** "The Components of the AI-Level Score: Level, AUC, Ceiling and Harness Gain" |
| Removed | none |

## 4. Tables

46 in the source build vs 45 in v2.6. **All 45 v2.6 tables are present.**

- **New:** Table 17, "Cumulative structure by object" (belongs to §11.7).
- **Renumbering:** v2.6 Tables 1–16 keep their numbers; **v2.6 Table N (N ≥ 17) is now Table N+1**, through v2.6 Table 45 → Table 46.
- **Section renumbering:** inserting §11.7 pushes the old §11.7 down, so **v2.6 §11.7 "What the uniform style buys" is now §11.8**. Comparing all 108 headings in v2.6 against the 109 in the build, **§11.7 is the only section number that means something different in the two documents**; §11.8 and §11.9 are new, §15.2 is renamed, and every other number keeps its meaning. A reference to "§11.7" is therefore ambiguous unless it says which document it follows, and nothing else is.
- No table was removed, and no caption changed materially (matched caption by caption).

> Consequence for other tasks: every table reference in the DK-04 change log and the DK-06 record was written against v2.6 numbering. Re-anchor them with the +1 rule before applying (DK-03).

## 5. Figures and equations

| Item | Result |
|---|---|
| Figures | 2 in both, on the same pages (44 and 50). Verified by rendering both documents' figure regions and reading them side by side: Figure 1 has the same 12 seed positions, markers and baselines; Figure 2 has the same two panels and three curves, and the neighbouring Tables 35/38 (v2.6 Tables 34/37) carry identical numbers. The shipped `fig_hsc.pdf` / `fig_regime.pdf` are the PDFs the build uses. |
| Figure regeneration | `make_figures.py` reproduces both: **visually equivalent, not byte-identical** (the script is a rewrite; layout and legend placement differ slightly). Verified by rendering both versions side by side. |
| Figure defect carried over | Both the shipped figures and the script label the panels "Success-only primitive, Eq. (9)" and "Delivered-outcome primitive, Eq. (10)". In this build those equations are (15) and (16)/(17), so the labels are wrong in the source too (`make_figures.py` lines 99–100). Now fixable, since the script exists. |
| Equations | (1)–(19) present in both, with matching content. Equations (12), (15) and (17) were checked individually by locating them in the built PDF, because the automated extraction skips multi-line fractions. |
| Equation wording change | Eq. (19): v2.6 "AIL-Score = 0.55 × AIL-AUC + 0.35 × AIL-Ceiling + …" → source "AI-Level Score = 0.55 × AUC + 0.35 × Ceiling + …" (consistent with the §15.2 rename). |
| References | 30 in both, identical; `references.bib` holds exactly 30 entries; `main.bbl` is shipped so no BibTeX run is needed. |

## 6. Complete list of content differences (source vs v2.6)

| # | Difference | Kind | Action |
|---|---|---|---|
| 1 | §11.7 + Table 17 added (v2.6 addendum written into the body) | Addition | Record as an approved difference (owner instruction: submit from this source) |
| 2 | §11.9 added | Addition | Same |
| 3 | §15.2 renamed; Eq. (19) terms renamed to match | Rename | Same |
| 4 | The "Naming" note differs: v2.6 announces AI-Level as the current name; the source explains the earlier HIL name | Changed text | Confirm which note the submission should carry |
| 5 | The v2.5 "Dataset binding" block (dataset/bench v0.2 identifiers) is absent from the source | Removal | Confirm it stays out; this retires DK-06 proposal P7 |
| 6 | Author line, running header and PDF metadata list two authors | Omission | DK-02 |
| 7 | Table numbers shift by +1 from v2.6 Table 17 onward | Renumbering | Re-anchor references in DK-04/DK-06 |
| 8 | 64 pages vs 69 | Pagination | Expected; reformatting changes it again |
| 9 | The abstract gains one sentence on typed cumulative structure | Addition | Include in the A5 acceptance; it is the abstract, so reviewers see it first |
| 10 | The v2.6 addendum's continuous per-domain C retention rule (`q*_{C,k,d} = min_{j≤k} q_{C,j,d}`, aggregation after retention) is in **neither** the body nor Eq. (14) | **Content gap** | Add one sentence to §11.7 or §14.8, or accept the loss on the record (proposal A8) |
| 11 | The data-availability sentence names a specific ancillary archive, `HIL_Benchmark_Library_v1_1.zip`, where v2.6 said only "the ancillary zip". **No file of that name was delivered**; the delivered dependency is `HIL_Coordinate_Benchmark_Datasets_v1_2.zip`, whose tooling looks like that material one version on | Changed text + dangling reference | Correct the name, or supply the named archive (proposal A9) |
| 12 | §15.4: "The three components and **AIL-Level** must always be published beside the composite" → "the three components and **the rung reached**" | Rename follow-through | Include in A5; consistent with the §15.2 and Eq. (19) renames |

**Body prose.** A sentence-level comparison of the whole body (v2.6 pp. 1–65 against the 64-page build, headers, page numbers and the contents pages removed) found no textual change beyond the differences listed above: 1,105 sentences in v2.6 against 1,089 in the build, and every unmatched sentence on either side traces either to one of these differences or to a table reflowing differently in text extraction. The keywords line, present in both, was confirmed directly after the extraction merged it with neighbouring text.

No v2.6 section, table, figure, equation or reference is missing from the recovered source. The only content that the published PDF carries and the source does not is (a) the v2.5 dataset-binding block, dropped deliberately, and (b) the one continuous rule in item 10.
