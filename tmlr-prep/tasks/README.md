# TMLR preparation — task records

One file per task from `DINGYI_KANG_PAPER_TASKS.md`. Status values: `assigned`, `in-progress`, `ready-for-review`, `accepted`, `blocked`, `not-applicable`. Only an owner decision sets `accepted`.

Private items (author contacts, consent, declarations, conflicts) are kept outside this repository and are never recorded here.

| Task | Title | Status | Record | Main blocker / note |
|---|---|---|---|---|
| DK-01 | Recover and freeze the inputs | `ready-for-review` | [DK-01.md](DK-01.md) | Source received 2026-09-17, builds clean in 64 pp., complete against v2.6. Owner decisions A4–A6 pending |
| DK-02 | Synchronize and confirm the editable author record | `in-progress` | not yet written | Source lists 2 authors; author order, contributions and consent await the authors |
| DK-03 | Convert to TMLR format without automatic cuts | `ready-for-review` | [DK-03.md](DK-03.md) | Both editions build clean in 61 pp. (0 errors, 0 undefined, 0 overfull). Decisions B1–B3 pending |
| DK-04 | Audit the theory, wording and references | `in-progress` | not yet written | 10 proposed corrections logged locally (from the DK-06 full reading); reference check not started; both land with the DK-04/DK-06 commit |
| DK-05 | Check the empirical results | `in-progress` | not yet written | §17.10 statistics match Table 34; the archive has arrived and its `analyze.py` runs, so the §18.4 recomputation can start |
| DK-06 | Resolve supporting-code issues that affect this paper | `ready-for-review` | follows in the next commit | Scorer defect confirmed, fixed in a separate module with tests; no measured result affected. Record being restructured by sub-task before review |
| DK-07 | Build the reproducibility supplement | `assigned` | not yet written | Needs archive and rights decision |
| DK-08 | Coordinate authorship, rights and submission information | `in-progress` | not yet written | Questions sent to the owner |
| DK-09 | Verify the exact candidate and prepare the review packet | `assigned` | not yet written | — |
| DK-10 | Obtain final owner and coauthor approval | `assigned` | not yet written | — |
| DK-11 | Deliver; submit only when separately authorized | `assigned` | not yet written | — |
