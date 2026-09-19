# Approval pack — what each person is being asked to approve

One page per reviewer, so nobody has to reconstruct their own list from eleven task records. **Nothing here is approved.** Overall state: `awaiting-author-approval`.

Candidate under review:

| Artifact | SHA-256 |
|---|---|
| `tmlr_submission.pdf` (anonymous, 63 pp) | `335ac583991413214070995a734f876235c0ab93ffbd1df9e2dcc8db86da5589` |
| `tmlr_named.pdf` (named, 63 pp) | `eee49b58f95a6face7f191fbba4a006acfd3c822a9212d5f93de3906dac321c7` |

**These hashes are provisional.** Approving any correction changes the PDF and therefore its hash. Regenerating the checks after a change is one command — `python3 tmlr-prep/dk09/verify_candidate.py --named … --anonymous …` — so an approved change costs a rebuild, not a re-audit.

---

## Chengshuai Yang — owner and corresponding author

You are the only person who can answer most of this.

**Rights and licensing**
1. The repository carries **no licence at all**, so everything in it defaults to all rights reserved. This single answer also decides items 2 and 3.
2. CC BY 4.0 applies from submission onward, not from acceptance. Approve?
3. May the evidence archive, and the inherited third-party benchmark archive inside it, go into a CC BY supplement?
4. The supplement would publish answers and verifier identities for 824 items the corpus marks certification-ready. Your own publication notes already state that public forms are specifications rather than protected instances, so this is a licensing choice, not a leak: ship as is, strip the answer fields, or ship the code-only variant?

**Authorship**

5. Is the order final — Yang, Xue, Kang? It cannot change after submission.
6. Do you remain corresponding author?
7. Ting Xue's contact address, and Xue's agreement to submit. No address is on record anywhere.
8. Your own contribution statement. Page 59 currently names only C.Y. and T.X. while the paper will carry three authors.

**Declarations**

9. Funding, per author. Page 59 says "no funding specific to this work"; confirm it is accurate and complete.
10. Competing interests. Page 59 says "no competing interest" — but NextGen PlatformAI is both your affiliation and the operator of the site hosting this work and its benchmark. That needs a deliberate answer, not a default.
11. Did you or Ting Xue use LLM tools in preparing the manuscript? The first-page disclosure currently speaks for Dingyi only.
12. Is a Statement of Broader Impact wanted?
13. Confirm there is no human-subjects component.
14. Does every author hold an active OpenReview profile, and is anyone at their submission quota?
15. Any concurrent submission of this work elsewhere? Note the repository contains a complete but unused arXiv submission package for v2.4.

**Scientific corrections** — 17 in DK-04's change log, of which 6 are substantive. The two that change what the paper asserts:

16. §23 and Appendix D state the memory ladder "is measured at M1". No method, data or result for M1 appears anywhere in the paper. Withdraw the claim, or supply the evidence?
17. §14.2 claims every achievement variable already enforces lower-level retention. That is false for `A_DI`. Correct the sentence, or make `A_DI` cumulative — which would change every measured number?

**Edition and identity**

18. The version number disagrees across the website (v2.4), the release package (v2.6) and the build script's output filename. Pick one for the submission edition.
19. The TMLR template has no date field, so the candidate carries no date. Leave it out, or restore one in the named build?
20. The published v2.6 PDF lists Dingyi Kang at NextGen PlatformAI C Corp. The correct affiliation is University of Texas at Dallas. Correct the public PDF?
21. `ladder_py_sha256` in the harness-curve study manifest is 65 characters and cannot be a valid SHA-256. Correct in a future release, or record as a known issue?

---

## Ting Xue

Nothing has been received from you, and no contact address is on record.

1. Name spelling as it should print.
2. Affiliation.
3. Contact address.
4. Author order: Yang, Xue, Kang.
5. Your own contribution statement.
6. Did you use LLM tools in preparing the manuscript?
7. Conflicts of interest for action-editor assignment.
8. OpenReview profile active, and submission quota not exhausted?
9. Agreement to submit.

---

## Dingyi Kang

| Item | State |
|---|---|
| Name, affiliation, contact | Confirmed 2026-09-18 — University of Texas at Dallas, dingyi.kang@utdallas.edu |
| Contribution statement | Drafted, evidenced by PRs #2–#11 |
| LLM tool use | Disclosed in the drafted first-page footnote |
| Author order | Pending — cannot be settled alone |
| Conflicts, OpenReview profile, quota | To be supplied |
| Approval of the candidate | Prepared it; does not self-approve |

---

## Approval record

Both templates are reproduced, because the assignment and the submission plan each specify one and they ask for different things.

**From the assignment:**

> Task IDs: ____ · exact evidence / candidate version: ____ · decision: accept / changes requested / blocked · reviewer / date: ____

**From the submission plan:**

> Candidate commit / PDF SHA-256: ____ · scientific changes approved: ____ · coauthor consent confirmed: ____ · submission terms confirmed: ____ · authorized submitter: ____ · owner / date: ____

| Reviewer | Decision | Date |
|---|---|---|
| Chengshuai Yang | pending | |
| Ting Xue | pending | |
| Dingyi Kang | prepared, not self-approved | 2026-09-18 |

Completed records go to `private-notes/`, never to this repository.

## Authorization to submit is separate

Approving the candidate is not authorization to submit. The assignment requires that to be given explicitly and separately, and it has not been given. Until it is, the state is `awaiting-author-approval` — not `submitted`, not `complete`.
