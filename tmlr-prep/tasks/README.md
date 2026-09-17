# TMLR preparation — task records

One file per task from `DINGYI_KANG_PAPER_TASKS.md`. Status values: `assigned`, `in-progress`, `ready-for-review`, `accepted`, `blocked`, `not-applicable`. Only an owner decision sets `accepted`.

Private items (author contacts, consent, declarations, conflicts) are kept outside this repository and are never recorded here.

**The live status view is `tmlr-prep/dk11/HANDOFF.md`**, which also carries the candidate hashes, the blockers in priority order and the approval record. This table is the index; the handoff is what to act on.

| Task | Title | Status | Record | Main blocker / note |
|---|---|---|---|---|
| DK-01 | Recover and freeze the inputs | `ready-for-review` | [DK-01.md](DK-01.md) | Source received 2026-09-17; builds clean and reconciles against v2.6. Decisions A4–A9 pending |
| DK-02 | Synchronize and confirm the editable author record | `blocked` | [DK-02.md](DK-02.md) | Record applied from one structure; Yang and Xue have confirmed nothing, and Xue has no contact on record |
| DK-03 | Convert to TMLR format without automatic cuts | `ready-for-review` | [DK-03.md](DK-03.md) | Both editions build clean at 63 pp. Decisions B1–B5 pending |
| DK-04 | Audit the theory, wording and references | `ready-for-review` | [DK-04.md](DK-04.md) | 17 proposed corrections, 6 substantive; 2 claims mislabelled; 29 of 30 references exact |
| DK-05 | Check the empirical results | `ready-for-review` | [DK-05.md](DK-05.md) | 52 of 53 values, 132 of 132 cells, 17 of 17 protocol claims reproduce; one prose/table discrepancy |
| DK-06 | Resolve supporting-code issues that affect this paper | `ready-for-review` | [DK-06.md](DK-06.md) | Scorer defect confirmed and fixed in a separate module with tests; no measured result affected |
| DK-07 | Build the reproducibility supplement | `blocked` | [DK-07.md](DK-07.md) | Both variants built and verified anonymous; **neither may ship** until rights and the certification-item question are answered |
| DK-08 | Coordinate authorship, rights and submission information | `blocked` | [DK-08.md](DK-08.md) | 24 requirements, 14 unresolved; no repository licence exists |
| DK-09 | Verify the exact candidate and prepare the review packet | `ready-for-review` | [DK-09.md](DK-09.md) | Candidate verified on all 63 pages; packet marked **not ready**, six blockers |
| DK-10 | Obtain final owner and coauthor approval | `blocked` | — | Needs the owner and each coauthor; Dingyi cannot supply another author's approval |
| DK-11 | Deliver; submit only when separately authorized | `ready-for-review` for the handoff | [DK-11.md](DK-11.md) | Handoff delivered; **submission not authorized and not performed** |

`not-applicable`, with evidence rather than silence: human-subjects reporting (both studies measure model–harness pairs; no participant data in the released evidence), the survey exclusion (this is original research), paid model reruns (none performed or authorized), and a repository licence change (not made — and none exists to change).
