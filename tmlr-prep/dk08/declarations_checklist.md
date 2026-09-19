# DK-08 declarations checklist — public status view

This is the **status** of every declaration TMLR requires, not the content of
any of them. Answers that are personal records, conflict-of-interest records or
approval records are held privately, outside this repository, and are marked
*held privately* below. The task file forbids publishing them here.

Requirements are taken from TMLR's [author guide](https://jmlr.org/tmlr/author-guide.html),
[editorial policies](https://jmlr.org/tmlr/editorial-policies.html) and
[FAQ](https://jmlr.org/tmlr/faq.html), read on 2026-09-18.

Legend: **resolved** · **unresolved** — needs an answer before submission · **n/a** — does not apply, with the reason given.

## Authorship and profiles

| # | Requirement | Status | Note |
|---|---|---|---|
| 1 | Every author holds a complete, active OpenReview profile, with affiliations, conflicts and publication history | **unresolved** | No author has confirmed their profile state. Needed from all three |
| 2 | Submission quota checked for each author | **unresolved** | TMLR limits concurrent submissions per author; unknown for Yang and Xue |
| 3 | Author set final — TMLR permits no addition or removal after submission | **unresolved** | Order and consent still pending; see DK-02 |
| 4 | Each author meets TMLR's contribution and responsibility conditions | **unresolved — and the manuscript is already inconsistent** | Page 59's contribution statement names only C.Y. and T.X., while the author list will carry three names |
| 5 | Each author agrees to submission | **unresolved** | No author has given this yet |

## Conflicts and editors

| # | Requirement | Status | Note |
|---|---|---|---|
| 6 | Conflicts of interest not covered by institutional history | **unresolved**, held privately | Must be collected from each author |
| 7 | Suitable action editors proposed | **candidates drafted** | Five action editors whose listed expertise matches, from TMLR's board of 400+. Final choice needs the conflict lists, since a conflict disqualifies an editor |
| 8 | Conflicting archival publications or concurrent submissions | **checked, one finding** | This work is **not** on arXiv — searched by title, by the earlier "Harness Intelligence Level" title and by author. But an `ARXIV.md` in the source prepares a v2.4 arXiv submission that was never made, and the author has a closely overlapping arXiv paper that this manuscript does not cite. See below |

## Declarations about the work

| # | Requirement | Status | Note |
|---|---|---|---|
| 9 | Funding and acknowledgements | **declared in the manuscript**, needs confirmation | Page 59 already states "no funding specific to this work… The measurement was run on the authors' own infrastructure". An author should confirm it is accurate and complete |
| 10 | Competing interests | **declared, but the declaration is doubtful** | Page 59 states "no competing interest". Two authors are affiliated with the operator of the site hosting this work and its benchmark, so that sentence should be revisited before it is relied on |
| 11 | Human subjects / IRB reporting | **likely n/a**, needs confirmation | No human-subjects data appears in the released evidence; the studies measure model–harness pairs. An author must confirm no human-subjects component exists |
| 12 | Statement of Broader Impact, required where the work "carries a significant risk of harm" | **unresolved** | A judgement call the authors must make. The work proposes a capability-measurement scale, which invites misuse as a capability claim; worth a short statement even if not strictly required |
| 13 | Original research, not a survey — TMLR stopped accepting surveys on 2026-09-01 | **resolved** | This is original research: it defines a framework and reports two measurement studies |

## LLM assistance

| # | Requirement | Status | Note |
|---|---|---|---|
| 14 | First-page footnote disclosing LLM tool use | **drafted, unresolved — and the manuscript's existing section is misleading** | Page 59 is headed "Author contributions and tool-use disclosure" but **discloses no tool use**, and sits on page 59 rather than page 1. The draft in `llm_assistance_disclosure.tex` supplies the footnote, but covers only Dingyi Kang's use |
| 15 | Ideas, claims and results are human-sourced | **resolved as drafted** | The assistance was engineering and verification; the theory, design, measurements and results are the authors' |

## Rights and licensing

| # | Requirement | Status | Note |
|---|---|---|---|
| 16 | CC BY 4.0 applies from submission onward, copyright retained by authors | **unresolved** | Needs the owner's explicit approval. This is the same gate as DK-07's rights question |
| 17 | Rights to include the evidence archive in a CC BY supplement | **unresolved** | The release carries no licence; see DK-07 |
| 18 | Rights to the inherited third-party benchmark archive embedded in that release | **unresolved** | See DK-07 |
| 19 | Repository licence not silently changed | **resolved** | Nothing in this work changes it |
| 19b | A repository licence exists at all | **unresolved — finding** | There is **no** `LICENSE` file anywhere in the repository. With no licence, the default is all rights reserved, which is why DK-07 cannot verify rights to anything in it. This is the root of the rights gate, not a separate issue |

## Anonymity and format

| # | Requirement | Status | Note |
|---|---|---|---|
| 20 | Submission anonymised, double-blind | **resolved** | Anonymous build verified clean across all 63 pages of text and metadata; see DK-02 |
| 21 | Supplementary material anonymised, PDF or ZIP, ≤ 100 MB | **built and verified, but blocked** | Both variants are anonymised and far inside the limit. **Neither may ship**: DK-07 decisions 1 and 6 are hard gates — rights, and whether to publish answers for 824 certification-ready items. Verified is not the same as shippable |
| 22 | TMLR LaTeX stylefile and template used | **resolved** | See DK-03 |
| 23 | The submission is not linked to an identified preprint version | **unresolved** | Versions 2.0 and 2.6 are publicly posted under the authors' names. Posting a preprint is permitted, but the TMLR submission must not be linked to it, and the archive we ship still describes itself by the v2.0 title — see DK-07 decision 5 |

## Candidate action editors

From TMLR's board of 400+, matched on listed expertise. **Not a final choice** — each must be checked against the authors' conflict lists, which do not yet exist.

| Action editor | Affiliation | Listed expertise that matches |
|---|---|---|
| **Olawale Elijah Salaudeen** | Microsoft | *benchmarking, …, validity* — the closest fit on the board: §17 of this paper is "The Validity of the Items" |
| Chinmay Hegde | New York University | *llm benchmarking* |
| Yali Du | King's College London | *llm agents, reinforcement learning* |
| Junpei Komiyama | Mohamed bin Zayed University of AI | *reasoning language models, reproducibility, hypothesis testing* |
| Haobo Fu | Tencent AIPD | *llm agent, vision language model* |
| Andrew Lampinen | Anthropic | *language models, memory episodic memory, cognitive science* — a different angle: relevant to the memory ladder rather than to evaluation |

All six were read from TMLR's published editorial board, not from a summary. The search was exhaustive over all **705** listed action editors: exactly two mention *benchmark* (Salaudeen, Hegde), exactly two mention *llm agent* (Du, Fu), and exactly one mentions *reproducibility* (Komiyama). There is no editor whose expertise mentions "evaluation" at all.

## Prior work by an author that this manuscript does not cite

Searching arXiv by author surfaced **"Self-Aware Recursively Self-Improving Agents for Personal Singularity"** (arXiv:2607.12254, 2026-07-14, Chengshuai Yang). Its subject — a persistent self-model of identity, goals, capabilities, limitations and developmental change, used to govern recursive self-improvement — overlaps this paper's Self-Awareness family and its I3–I5 self-improvement ladder directly.

**It appears nowhere in `references.bib` or `main.tex`.** That is a problem on two counts: TMLR asks about overlapping archival work, and omitting the closest prior work — the author's own — is the kind of gap a reviewer finds and reads badly. Citing one's own prior work in the third person is permitted under double-blind review.

## Consequences the authors should know before submitting

| Fact | Source |
|---|---|
| Submitted papers stay publicly accessible on OpenReview whether accepted, rejected, withdrawn or retracted. Only desk-rejected papers never appear | TMLR FAQ |
| Authors cannot be added or removed after submission | TMLR editorial policies |
| CC BY 4.0 applies from submission onward, not from acceptance | TMLR author guide |

## Count

**24 requirements: 6 resolved, 1 likely not applicable, 1 with candidates drafted, 1 checked with a finding, 1 built but blocked, 14 unresolved.** No submission is possible until the unresolved rows have answers, and none of them can be answered by Dingyi alone.
