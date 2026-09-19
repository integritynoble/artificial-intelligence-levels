# Handoff — TMLR submission preparation

One place to find everything produced for this submission, what state each piece is in, and what is needed to move it.

**Nothing here is submitted, and nothing is approved.** Submission requires separate authorization that has not been given, and is not assumed by this handoff existing.

| Field | Value |
|---|---|
| Prepared | 2026-09-18 |
| Prepared by | Dingyi Kang |
| Overall state | `awaiting-author-approval` |
| Day-5 target | **Not met.** Reason: every remaining task needs an owner or coauthor decision, and none has been given |

## Task status

Using the assignment's vocabulary. `ready-for-review` is technical completion; only an owner decision makes anything `accepted`.

| Task | Status | Where | Items awaiting the owner |
|---|---|---|---|
| DK-01 recover and freeze the inputs | `ready-for-review` | PR #2 | **9** — proposals A1–A9 |
| DK-02 synchronize the author record | `blocked` | PR #8 | **6** decisions, plus 5 revision proposals |
| DK-03 convert to TMLR format | `ready-for-review` | PR #3 | **6** — A5 carried from DK-01, plus B1–B5 |
| DK-04 audit theory, wording, references | `ready-for-review` | PR #5 | **17** corrections in the change log, of which **6** are substantive |
| DK-05 check the empirical results | `ready-for-review` | PR #4 | **5** — numerical proposals C1–C5 |
| DK-06 resolve supporting-code issues | `ready-for-review` | PR #6 | **12** — P1–P8, S1, N1 and related |
| DK-07 build the reproducibility supplement | `blocked` | PR #7 | **7** decisions |
| DK-08 authorship, rights, submission info | `blocked` | PR #9 | **11** decisions, plus 6 revision proposals |
| DK-09 verify the candidate, review packet | `ready-for-review` | PR #10 | **6** revision proposals |
| DK-10 owner and coauthor approval | `blocked` | this file | all of the above, plus each coauthor's own consent |
| DK-11 deliver; submit only if authorized | `ready-for-review` for the handoff; **submission not authorized** | this file | **1** decision, plus 2 revision proposals |

Counted in each record's own scheme, because the records use different ones — lettered proposals in DK-01, DK-03, DK-05 and DK-06, numbered decision tables in DK-02, DK-07, DK-08 and DK-11, and a change log in DK-04. DK-04's six substantive items are drawn from its seventeen, not additional to them.

**An earlier version of this table gave a single "decisions waiting" number per task, and almost every one was wrong** — DK-01 read 6 against 9 real items, DK-06 read 5 against 12, DK-05 read "0 — findings only" when it has five numerical proposals, and DK-07 read 6 after a seventh had been added. The counts had been written once and never re-derived while the records kept moving.

**`not-applicable` items, with evidence rather than silence:**

| Item | Why not applicable |
|---|---|
| Human-subjects / IRB declaration | Both studies measure model–harness pairs. No participant data appears anywhere in the released evidence. An author should still confirm rather than leave it inferred |
| Survey-paper exclusion | TMLR stopped accepting surveys on 2026-09-01. This paper defines a framework and reports two measurement studies of its own |
| Paid model reruns | None performed; none authorized. No result here depends on a new run |
| Repository licence change | Not made. Note that no licence exists to change — see blocker 1 |

## The candidate

| Artifact | SHA-256 |
|---|---|
| `tmlr_submission.pdf` (anonymous, 63 pp) | `335ac583991413214070995a734f876235c0ab93ffbd1df9e2dcc8db86da5589` |
| `tmlr_named.pdf` (named, 63 pp) | `eee49b58f95a6face7f191fbba4a006acfd3c822a9212d5f93de3906dac321c7` |
| `review_packet.md` | `a59d3c893e13f0c4d04579c8ec71ee2746c16967160df0e26b137b0b731e3bae` |

Both live in PR #10 under `tmlr-prep/dk09/build/`. The source is `paper-sources/unified-theory/main.tex`, SHA-256 `f6565616…cdba60c`, hash-matched to DK-01's frozen inventory.

**These hashes are provisional.** Any approved correction changes them, and the checks and hashes must be regenerated — `tmlr-prep/dk09/verify_candidate.py` does that in one command.

## What is in the handoff, and where

| Piece | Location |
|---|---|
| Final named manuscript | PR #10, `tmlr-prep/dk09/build/tmlr_named.pdf` |
| Anonymous submission PDF | PR #10, `tmlr-prep/dk09/build/tmlr_submission.pdf` |
| Source, bibliography, figures | `paper-sources/`, already public; converter in PR #3 |
| Anonymous supplement | PR #7, both variants — **cannot ship**, see blockers 1 and 5 |
| Reproduction instructions | Inside each supplement variant's README; build steps in PR #10's `build_log.txt` |
| Review evidence | Task records in `tmlr-prep/tasks/`, one per task, across PRs #2–#10 |
| Private records — consent, declarations, contact details | Held outside this repository, never committed |

## Blockers, in the order they should be answered

| # | Blocker | Who | Why it is first |
|---|---|---|---|
| 1 | **No licence exists anywhere in this repository** | Owner | Everything defaults to all rights reserved, which is why rights cannot be verified for the supplement or anything else. One decision unblocks the most |
| 2 | CC BY 4.0 from submission onward | Owner | Applies from submission, not acceptance |
| 3 | Author order, consent, final author set | All three | TMLR permits no change after submission |
| 4 | Ting Xue's contact and agreement | Owner to relay | No address is on record at all |
| 5 | Supplement: 824 certification-ready items ship with their answers | Owner | Publishing them under CC BY affects the benchmark's future use |
| 6 | First-page LLM disclosure, accurate for all three authors | All three | Required by TMLR; the draft speaks for one author |
| 7 | Version number for the submission edition, and whether to restore a date (DK-03 B4) | Owner | Not a blocker. The version number genuinely disagrees in three places; the date is simply absent by design — see above |

## Approval record

To be completed by the owner and each coauthor, in the assignment's template. Dingyi coordinates this and cannot supply another author's approval.

> Task IDs: ____ · exact evidence / candidate version: ____ · decision: accept / changes requested / blocked · reviewer / date: ____

| Reviewer | Task IDs | Candidate version | Decision | Date |
|---|---|---|---|---|
| Chengshuai Yang | | | pending | |
| Ting Xue | | | pending | |
| Dingyi Kang | DK-01 … DK-11 | the hashes above | prepared, not self-approved | 2026-09-18 |

## Two decisions about the submission edition's identity

Neither blocks submission, but both should be settled before the title page is final, and neither appears in any task record until now. Both come from the owner's own source handover, which recommends a decision and does not make one.

**Version number.** Three places disagree, and the lower number is the newer text:

| | Number | Date | What it is |
|---|---|---|---|
| Website PDF | v2.4 | 2026-09-07 | The manuscript's own LaTeX build; `build_arxiv.sh` writes `..._v2_4.pdf` |
| Release package | v2.6 | 2026-09-06 | The same manuscript with two addenda appended |

The handover's recommendation is to pick one number for the submission edition and change the title page, the build script's output filename, the website and the release label together. Nothing here does that, because it is the owner's call.

**Title-page date.** The candidate carries **no date at all** — the string appears nowhere in either TMLR edition. The date lived in the centred title block that `\maketitle` replaces, and the template has no date field for submissions, so it survives only in the source and any arXiv build. DK-03 records this as a deliberate drop, decision **B4**: leave it out, which is what the template expects, or restore it in the named build.

## The submission plan's own final checklist

`TMLR_SUBMISSION_PLAN.md` carries an eight-item checklist to be re-checked against current journal instructions immediately before submitting. Where each is handled:

| Plan checklist item | State | Where |
|---|---|---|
| Manuscript and supplement anonymized, incl. metadata and links; not linked to a named version | Anonymity verified; the archive still describes itself by the v2.0 title | DK-02, DK-07, DK-09 |
| OpenReview profiles for every author; supplement within PDF/ZIP and 100 MB | Size and format verified; profiles unchecked | DK-07, DK-08 |
| CC BY 4.0 understood from submission onward; rights confirmed | **Unresolved** — no licence exists to confirm rights under | DK-08 |
| All authors consent; list final; sufficient quota; no conflicting or concurrent archival submission | **Unresolved**; not on arXiv, but an unused arXiv package and an uncited overlapping paper were found | DK-02, DK-08 |
| LLM assistance disclosed in a first-page footnote; original research, not a survey; submissions stay public | Footnote drafted, not inserted; originality confirmed | DK-08 |
| Funding, competing interests, ethics, broader impact complete | Declared on page 59; the competing-interest sentence needs revisiting | DK-08, DK-09 |
| Central claims supported, missing evidence disclosed, substantive changes approved; no blocker hidden behind a passing integrity check | Evidence gaps disclosed; **no change is approved**; snapshot integrity reported separately from scientific validation, as the plan requires | DK-04, DK-05, DK-09 |
| Exact final PDF, supplement and source pass technical checks; owner separately authorizes submission | Checks pass on the current candidate; **no authorization** | DK-09, DK-11 |

## Approval record — the submission plan's template

`TMLR_SUBMISSION_PLAN.md` specifies its own record, with fields the assignment's template does not carry. Both are reproduced so neither is lost.

> Candidate commit / PDF SHA-256: ____ · scientific changes approved: ____ · coauthor consent confirmed: ____ · submission terms confirmed: ____ · authorized submitter: ____ · owner / date: ____

## If submission is later authorized

Not authorized today. If it is, in this order: recheck TMLR's current instructions, enter the approved metadata and the full author list in OpenReview, upload the exact approved anonymous files by the hashes recorded above, and verify the receipt. Report journal review as pending, never as accepted, and keep receipt details private.
