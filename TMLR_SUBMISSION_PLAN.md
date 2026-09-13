# TMLR submission plan

_Prepared 2026-09-13 · Status: planning only; not submission-ready or submitted._

## Assigned preparation sprint and author update

At the owner's request, the public v2.6 PDF now lists **Chengshuai Yang, Ting Xue and Dingyi Kang — NextGen PlatformAI C Corp, USA**. The amendment changes only the author line, author running headers and PDF Author metadata; scientific content and the existing contribution statement remain unchanged. The [original two-author PDF](https://github.com/integritynoble/artificial-intelligence-levels/blob/12331315048e1cbf35a706f80ba572be81dcdd78/papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf) is recoverable at commit `12331315048e1cbf35a706f80ba572be81dcdd78`. Final author order, verified contributions and all-author consent remain pending. Matching editable-source recovery, synchronizing its author record and preparing an anonymous review build are still assigned tasks; the PDF amendment does not complete DK-02.

**Dingyi Kang owns all preparation work** in the [single 3–5-working-day task assignment](DINGYI_KANG_PAPER_TASKS.md), including verification, packaging and approval coordination. Scientific approval and each coauthor's consent remain with those authors. The accelerated target requires usable source/evidence and prompt decisions; the longer contingency estimates below still apply when those conditions fail.

## Recommendation

Target **Transactions on Machine Learning Research (TMLR)** first for [Unified Intelligence Theory and the Artificial Intelligence Level, v2.6](papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf). The priorities are no publication fee, preservation of the original scientific content, and reasonably prompt review.

TMLR charges authors no publication fees. Its scope includes performance-assessment methods and analytical frameworks for learning systems. Our assessment is that the paper's operational evaluation framework could fit; this is not an editorial endorsement or an acceptance prediction. Free publication does not cover any separate model API or research-computing costs. [Editorial policies](https://jmlr.org/tmlr/editorial-policies.html)

TMLR explicitly permits papers of any justified length. There is no mandatory 12-page limit: the current 69-page PDF is not excluded solely by its length, although a long main text can delay review. The submission must use the official TMLR LaTeX template. Appendices can remain in the same PDF, but reviewers need not read them, so essential evidence must stay in the main text. [Author guidelines](https://jmlr.org/tmlr/author-guide.html)

## How soon can we submit?

**Allow provisionally 1–2 weeks of preparation, subject to recovering the source and resolving the evidence audit.** This is a work estimate, not a scheduled completion promise. Waiting for missing materials or author decisions adds elapsed time.

| Scenario | Estimated preparation time | Conditions |
|---|---|---|
| Best case | 3–5 working days | Matching editable source and necessary evidence are recovered promptly; only bounded corrections, formatting and submission checks are needed; authors respond promptly. |
| Planning allowance | 1–2 weeks | Source recovery succeeds and the evidence audit can be resolved with existing artifacts and agreed claim qualifications. |
| Reconstruction or additional validation | 2–4 weeks or longer | Source must be reconstructed, important results lack supporting artifacts, or new experiments are necessary. Re-estimate after the audit; this is not an upper bound. |

The main dependencies are not yet closed. A PDF upload alone is not readiness for journal submission. New paid experiments are not authorized by this plan.

**After submission:** TMLR accepts submissions year-round and targets a final decision in approximately nine weeks, without a guarantee. Main bodies exceeding 12 pages can take longer. That target is not time to acceptance; publication additionally depends on acceptance and camera-ready verification. [FAQ](https://jmlr.org/tmlr/faq.html)

## Preserve the original; prepare a separate edition

Preserve the original two-author PDF in Git and retain the documented author-amended public PDF and other snapshot payloads as the current release baseline. Prepare further manuscript changes, editable source, submission PDF and anonymized supplement in a separate submission workspace. Reformatting will change pagination. See [publication notes](PUBLICATION_NOTES.md) for the author-only amendment and recovery commit.

The default is to retain the title, central framework, coordinate and level definitions, mathematical development, and supported results. Do not shorten automatically to 12 pages. Moving detailed catalogs or derivations into appendices is optional, with owner approval and a section-by-section content map.

Preserving content cannot mean preserving a verified error or an unsupported conclusion. Record every substantive correction, qualification or removal, with its reason and owner decision. Distinguish stipulated definitions and proposed tests from proved statements and empirically validated measurements; do not describe the hierarchy as an established natural law without evidence.

TMLR evaluates whether claims have clear, convincing support and interest for its research audience. Evidence gaps can require stronger evidence or narrower claims. Framing the contribution around learning-system evaluation should clarify the actual research, not conceal its limitations. [Acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html)

## Current readiness gaps

These findings concern the inspected release, not every artifact the authors may possess. See the [publication notes](PUBLICATION_NOTES.md) and the theory paper's limitations and data-availability sections.

| Gap | Required resolution before submission |
|---|---|
| Matching editable v2.6 source was not found in the inspected bundle. | Obtain the matching source and bibliography from the authors. If unavailable, reconstruct and compare every section, equation, table and figure against the preserved PDF. Do not treat an older draft as the matching source. |
| Empirical studies are preliminary and cover only limited settings. | Map each numerical claim to its study, executor/model, sample size, artifact and analysis. Do not generalize a limited experiment into validation of every coordinate or a universal model ranking. |
| The paper identifies reconstructed episode rows and missing original records/artifacts. | Label reconstructed rows explicitly; do not present them as original logs. Recover evidence where possible, and qualify or revise claims where it is unavailable. Never invent missing model versions or records. |
| The public development dataset is not the original experiment archive or a complete benchmark runner. | Provide the evidence needed for retained central claims. Separate development examples, specification-only levels and actual executed evaluations in the supplement and manuscript. |
| Published companion artifacts have known metadata and scoring issues. | Assess whether each issue affects this paper's retained claims. Any relied-on implementation must be tested and corrected in a separately versioned artifact, or excluded from the claim with an explicit limitation. Keep the original snapshot intact. |
| Anonymization, accurate tool-use disclosure, author consent and submission rights have not been checked. | Complete the final submission checklist below; do not infer approval from the public GitHub upload. |

The existing `python3 -B tools/verify_public_snapshot.py` command checks package integrity and structure only. It does not reproduce experiments, certify intelligence levels or establish scientific correctness.

## Preparation workflow

Suggested effort ranges can overlap. At the first checkpoint, revise the schedule using actual source and evidence availability.

| Step | Work and expected effort | Deliverable / completion check |
|---|---|---|
| 1. Establish the source | 0.5–1 working day once materials are available. Locate the matching source, bibliography, figures and experiment artifacts; inventory missing items. | Source/provenance inventory and a readiness decision: proceed, reconstruct, or resolve specific evidence gaps. |
| 2. Build the submission edition | 1–2 working days if source is usable. Convert to the official template; preserve content; fix references, equations and layout. | Compiling source and PDF, plus a content map back to v2.6. Reconstruction is additional work. |
| 3. Audit evidence and claims | 1–3 working days with accessible artifacts, partly parallel with Step 2. Recalculate supported results and check theory assumptions, citations and limitations. | Claim-to-evidence table, reproducible commands/results, and a substantive-change log. Any unresolved central claim blocks readiness. |
| 4. Package and check | 0.5–1 working day. Prepare anonymous PDF/supporting files; inspect metadata, links, build logs, tables and references. | Exact candidate PDF and supplement, checksums and a short verification report identifying what was and was not reproduced. |
| 5. Obtain author approval | Allow 0.5–1 working day for review, plus any waiting time. Present the exact candidate and unresolved decisions to the owner and coauthors. | Explicit approval of that candidate, authorship, disclosures and submission terms. Submission occurs only after separate authorization. |

This plan does not require testing all LLMs or launching the full AI-Level platform before submitting the theory paper. The experiments must be adequate for the claims actually retained; a small study cannot support broad, unqualified ranking claims.

## Final submission checklist

Check these against current journal instructions again immediately before submitting.

- [ ] Final manuscript and supplement are anonymized, including PDF metadata and identifying links; preprints already online are permitted, but the submitted version must not link to a named version.
- [ ] Complete, active OpenReview profiles exist for every author; supplementary material is within the permitted PDF/ZIP format and 100 MB limit.
- [ ] Authors understand that TMLR submissions carry CC BY 4.0 from submission onward. Required rights/permissions are confirmed. This plan does not itself license the repository or its dataset. [Author guidelines](https://jmlr.org/tmlr/author-guide.html)
- [ ] All authors consent; author list is final; each author has sufficient submission quota. No conflicting archival publication or concurrent archival submission exists. [Editorial policies](https://jmlr.org/tmlr/editorial-policies.html)
- [ ] Any LLM assistance is disclosed accurately in a first-page footnote; human authors verify and take responsibility for the ideas, claims and results. The submission presents original research, not a survey: TMLR stopped considering surveys on September 1, 2026. Authors understand that reviewed submissions generally remain public even if rejected or withdrawn; desk-rejected submissions are the exception. [FAQ](https://jmlr.org/tmlr/faq.html)
- [ ] Funding, competing interests, relevant ethics/human-subjects information and any required broader-impact statement are complete. [Author guidelines](https://jmlr.org/tmlr/author-guide.html)
- [ ] Central claims have support, missing evidence is disclosed, and all substantive changes have been approved. No unresolved scientific blocker is hidden behind a passing package-integrity check.
- [ ] The exact final PDF, supplement and source version have passed technical checks, and the owner has separately authorized journal submission.

## Minimal owner review

The preparation work should produce a short review packet so the owner need not rerun routine technical checks:

1. **Read the final abstract, conclusions and substantive-change log.** Confirm that the original contribution is retained and each changed claim is acceptable; inspect linked passages where needed.
2. **Read the one-page evidence/verification summary.** Confirm that limitations are accurately stated and no unresolved central claim is being presented as validated.
3. **Approve the exact candidate and author declarations.** Confirm coauthor agreement, truthful disclosures, rights and submission terms; provide explicit permission to submit only when ready.

Suggested approval record, to be completed later in the appropriate author-controlled record:

> Candidate commit / PDF SHA-256: ____ · scientific changes approved: ____ · coauthor consent confirmed: ____ · submission terms confirmed: ____ · authorized submitter: ____ · owner / date: ____

No scientific acceptance or journal-submission authorization is recorded by publishing this plan. This Markdown plan is public planning material, not an anonymized submission supplement.
