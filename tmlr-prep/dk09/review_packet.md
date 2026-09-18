# Review packet — submission candidate

| Field | Value |
|---|---|
| Built | 2026-09-18, in a clean directory from the inputs DK-01 froze |
| Source | `paper-sources/unified-theory/main.tex`, SHA-256 `f6565616…cdba60c`, hash-matched to DK-01 |
| Anonymous PDF | `build/tmlr_submission.pdf`, 63 pages |
| Named PDF | `build/tmlr_named.pdf`, 63 pages |
| Supplement | Built under DK-07; **not shippable** — see blockers |

## READY FOR SUBMISSION: **NO**

DK-09 forbids marking a candidate ready while a central blocker is unresolved. Six are.

| # | Blocker | Owner | Task |
|---|---|---|---|
| 1 | No licence exists anywhere in the repository, so everything defaults to all rights reserved | Owner | DK-08 |
| 2 | CC BY 4.0 from submission onward not approved | Owner | DK-08 |
| 3 | Author order, consent and the final author set unconfirmed; TMLR permits no change after submission | All authors | DK-02 |
| 4 | Ting Xue has no contact address on record, and has confirmed nothing | Owner | DK-02 |
| 5 | The supplement cannot ship: rights, plus 824 certification-ready items that carry their answers | Owner | DK-07 |
| 6 | The first-page LLM-assistance disclosure is drafted but not in the manuscript, and speaks for one author only | All authors | DK-08 |

## What was verified

| Check | Result |
|---|---|
| Inputs match DK-01's frozen hashes | 5 of 5 |
| Both builds | 63 pages, 0 undefined references, 0 overfull boxes |
| Anonymous vs named scientific content | **Identical** — 8 differing lines out of ~2,520, all the author block |
| Every page inspected for clipping, broken mathematics, unreadable figures, missing content | 63 of 63, by rendering and reading them |
| Fonts | 35, all embedded; 0 missing glyphs |
| Anonymity of the submission build | 0 identifying terms in text or metadata |
| Published snapshot integrity | `verify_public_snapshot.py` passes: 159 payload hashes, 155 dataset files |
| Numerical claims | 52 of 53 reproduce; 132 of 132 per-seed cells agree (DK-05) |

## Substantive-change log

Nothing below is applied to the manuscript. Every item is a proposal awaiting approval.

| Source | Proposals | Substantive |
|---|---|---|
| DK-04 | 17 corrections | 6 |
| DK-02 | 5, covering the author record and the published PDF's wrong affiliation | 2 |
| DK-06 | Corrected delegation-frontier scorer, with tests | 1 |
| DK-08 | 6, including the first-page disclosure and citing the omitted prior work | 3 |
| DK-09 | 2, below | 2 |

## Claim-to-evidence summary

This is a summary. The claim-level tables the submission plan's Step 3 asks for already exist and are more specific than anything restated here:

| Table | Granularity | Where |
|---|---|---|
| `claim_to_evidence.md` | Every reported **number**, with its study, executor or model, episode and seed counts, source artifact, and whether it reproduces | DK-05, PR #4 |
| `claim_status.md` | Every central **claim**, classified as definition, argued, proved, measured or proposed test, with whether the paper labels it correctly | DK-04, PR #5 |

Read those for per-claim detail. The table below is only the shape of the result.

| Claim class | Evidence status |
|---|---|
| Reported numerical values | 52 of 53 reproduce from the released archive; one prose figure (§18.4.7 "+3.4") contradicts the paper's own tables, which read 3.3 |
| Per-seed tables 34 and 35 | 132 of 132 cells agree |
| Protocol claims | 17 of 17 hold |
| Harness-scaling curves | Only one executor's episode rows were released; two of three curves are table-only |
| Item-family accuracies | Not reproducible by anyone — generators, reference solvers and specification-key tests are unreleased |
| "The memory ladder is measured at M1" | **No method, data or result anywhere in the paper.** Mislabelled (DK-04) |
| §14.2 retention claim | False for A_DI (DK-04) |

## Verification and limitations, in one page

**What this candidate is.** A 63-page TMLR-format build from the frozen inputs, in anonymous and named forms whose scientific content is identical. It builds clean, renders clean on every page, and carries no identity in the anonymous form.

**What it is not.** It is not approved, not licensed, and not complete as a submission. None of the proposed corrections from DK-02, DK-04, DK-06, DK-08 or DK-09 are applied, because none is approved. So this candidate still contains the two mislabelled claims DK-04 found and the prose/table discrepancy DK-05 found.

**The most significant limitation is evidential, not editorial.** Of the paper's empirical content, one curve of three has released episode rows; the item-family accuracies cannot be reproduced by anyone, including the authors, because the generators and keys were never released; and one headline claim about the memory ladder has no method or data behind it anywhere. A reviewer who asks for the evidence behind those will not find it, and no amount of build verification changes that.

**On reproducibility of this build.** The figure step needs matplotlib, which is undeclared and was absent from every interpreter on the build machine; the figures had to be regenerated with matplotlib 3.11.2, which is not the version that produced the released ones, so the figures are not byte-reproducible.
