# DK-04 claim-status table

_Prepared 2026-09-18 against the TMLR build (`tmlr-prep/dk03/build/`). DK-05 traces the paper's **numbers** to their artifacts; this table classifies the paper's **claims**, because the task requires distinguishing definitions, conjectures and proposed tests from things proved or measured._

Status values used here:

| Status | Meaning |
|---|---|
| **Definition** | Stipulated. Can be judged coherent or incoherent, not true or false |
| **Argued** | A position defended in prose, not a theorem and not a measurement |
| **Proved** | A stated proposition with an argument in the paper |
| **Measured** | Supported by reported measurement (evidence class in DK-05) |
| **Proposed test** | A protocol the paper specifies but does not run |

## Central claims

| # | Claim | Where | Status | Does the paper label it correctly? |
|---|---|---|---|---|
| 1 | Five conceptual families and six measured coordinates `[C, I, O, T, H, SA]` | §3 | Definition | Yes |
| 2 | The Unified scale U0–UΩ is cumulative and gated; promotion requires lower-level retention plus every coordinate gate | §8, §11.6 | Definition | Yes — "invariant operational definitions", and §23 lists the thresholds as hypotheses |
| 3 | Memory M is a separate ladder joined to I by a one-way gate | §5.1.1, Table 7 | Definition | Yes |
| 4 | The memory ladder "is measured at M1" | §1.3, §23, App. D | **Claimed measurement with no reported evidence** | **No.** No M1 method, data or result appears anywhere in the paper. DK-01 proposal A8 / change-log item 7 |
| 5 | GUI/screen understanding is a domain of C with GP0–GP5 as a diagnostic subscale that never promotes C | §4.1, addendum | Definition | Yes |
| 6 | Cumulative structure is typed, not universal (retention, frontier, nesting, none) | §11.7, Table 17 | Definition | Yes |
| 7 | The delegation frontier is cumulative: a pass at a hard band cannot certify above a failed easier band | §6 note, §11.4 gate, addendum §5 | Definition | Partly — **Eq. (8) and the §11.4 formula both state the non-cumulative form**; only the surrounding note and gate are cumulative (change-log item 1) |
| 8 | HLIS is a weighted geometric mean over achievement variables, each enforcing lower-level retention | §14.1–§14.2 | Definition | **No** — A_DI (Eqs. 15, 17) is a plain weighted mean with no retention term, and A_C's retention rule appears only in the addendum (change-log item 5) |
| 9 | **Proposition 1**: a success-only A_DI is invariant to an acceptance-only harness step | §14.9.1 | **Proved** (argument given) **and** measured twice | Yes — argument plus Table 39 and the paired Table 41 |
| 10 | The delivered-outcome primitive restores sensitivity to acceptance | §14.9.2 | Definition + measured | Yes — 86.7 → 93.3 in the net column, reproduced in DK-05 |
| 11 | Harness Gain separates executors where AUC does not | §18.4.2 | Measured (reconstructed rows; one of three curves released) | Yes, with the saturation caution stated |
| 12 | The regime-switch family discriminates the two archived configurations on these instances | §17.10 | **Measured** (archived originals; fully reproduced in DK-05) | Yes — "not model tiers in general" is stated in §17.10.2, §23 and the abstract |
| 13 | Four answer-key defects and two apparatus defects were found | §17.3–§17.8, §17.11 | Reported audit findings; the reasoning is given, the instances are not released | Yes — §23 says the audit has "unknown recall" and that unflagged items are "unaudited rather than validated" |
| 14 | The two library audits (5 and 45 errors) | §17.12, Table 36 | Partly evidenced — the 45-error run is documented inside the inherited dependency archive; the 5-error record is not released | Yes, as a finding; DK-01 A6 asks for the missing record |
| 15 | I3, I4, I5, IΩ and M2–MΩ | §5.1, App. D | **Proposed tests, unmeasured** | Yes, explicitly: "specified to the factor and unmeasured here… a level that has been defined and never run is a definition" |
| 16 | Level thresholds are working definitions requiring calibration | abstract, §23 | Argued | Yes |
| 17 | AI-Level complements rather than replaces capability-centred AGI definitions | §18.7 | Argued | Yes |

## Assessment

**The paper's labelling discipline is good.** Fifteen of seventeen central claims carry the status they deserve, and the strongest empirical claim (12) is hedged in three separate places. The upper levels are repeatedly and explicitly marked as defined-but-never-run — including an appendix whose stated purpose is to say so.

**Two claims are mislabelled**, both already in the change log:
- Claim 4: the memory ladder is said to be *measured* at M1, with no reported M1 evidence anywhere. This is the one place where the paper states a measurement it does not show.
- Claim 8: §14.2 says every achievement variable enforces lower-level retention. A_DI does not, and A_DI is the variable behind every measured number in §18.4.

**One definition contradicts itself** (claim 7): the frontier is defined non-cumulatively in two equations and cumulatively in the note, the gate and the addendum.

No claim describes the hierarchy as an established natural law, and no claim presents the levels as universally validated measurements. Every use of "universal" in the paper denies universality, and two uses of "validated" explicitly say unflagged items are *unaudited rather than validated*.
