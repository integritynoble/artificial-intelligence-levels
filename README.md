# Artificial Intelligence Levels

Research papers and a public development dataset for **AI-Level**: measuring AI agents and language models through explicit coordinate tests, reference harnesses and reported uncertainty.

This is a publication snapshot, not a complete benchmark service or an independently certified intelligence ranking. Public examples must not be reused as protected certification tests.

## Papers

| Paper | Version | Download |
|---|---|---|
| Unified Intelligence Theory and the Artificial Intelligence Level | 2.6 | [Theory PDF](papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf) |
| AI-Level Bench: Measuring the Intelligence Level of Agents and Language Models in Every Coordinate | 0.4 | [Benchmark PDF](papers/AI_Level_Bench_v0_4.pdf) |
| The AI-Level Index | 2.0, companion | [Index PDF](papers/The_AI_Level_Index_v2_0.pdf) |

The theory, benchmark and dataset are the version-matched 2.6 / 0.4 / 0.4 publication bundle. The Index v2.0 is a separate companion with its own instrument studies and historical results; those results are not new measurements on this dataset snapshot. The benchmark and Index PDFs retain their source bytes and draft labels. The theory PDF has the author-only amendment described below; its scientific content is unchanged. Matching editable sources for the theory v2.6 and benchmark v0.4 PDFs were not found in the inspected release bundle.

**Theory authors:** Chengshuai Yang, Ting Xue and Dingyi Kang — NextGen PlatformAI C Corp, USA. At the owner's request, the theory PDF's author line, author running headers and PDF Author metadata were amended on September 13, 2026. Its existing contribution statement is unchanged. The [original two-author PDF](https://github.com/integritynoble/artificial-intelligence-levels/blob/12331315048e1cbf35a706f80ba572be81dcdd78/papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf) remains recoverable in Git. This PDF amendment does not establish coauthor consent or journal-submission readiness; see [publication notes](PUBLICATION_NOTES.md).

[TMLR submission plan](TMLR_SUBMISSION_PLAN.md): a no-publication-fee journal recommendation, content-preserving preparation workflow, readiness checklist and provisional 1–2-week preparation estimate. The paper has not been submitted through this plan.

[Dingyi Kang's paper tasks](DINGYI_KANG_PAPER_TASKS.md): all preparation tasks assigned to Dingyi for a conditional 3–5-working-day sprint, with daily deliverables and owner-review checks. The public theory PDF now includes Dingyi; matching editable-source recovery, author confirmation, verified contribution statements and the anonymous TMLR edition remain pending.

## Public dataset

[Browse the dataset](datasets/ai-level-bench-v0.4/) · [Download the public ZIP](downloads/AI_Level_Benchmark_Dataset_v0_4_public.zip) · [Read the dataset card](datasets/ai-level-bench-v0.4/DATASET_CARD.md)

The snapshot contains:

- 82 canonical testing-method records and 82 level-matrix records.
- 124 combined public development forms, including specification-only templates.
- C, C^GUI, GP, I, M, O, SA, T, H, DI, HG and U definitions, contracts and examples.
- 13 GUI image assets and four illustrative Python scoring modules.
- 155 source/data/asset files; four compiled Python cache files from the upstream ZIP are excluded.

The 82 method records comprise 56 `development-bound` and 26 `specification-only` entries. Documenting a level does not mean a runnable, validated or secure test exists for it. The public scorer examples do not constitute the full agent/model runner, and no private evaluation salt, hidden-test instance or organizer archive is included.

## Verify the download

From the repository root, using Python 3.9 or newer and its standard library:

```bash
python3 -B tools/verify_public_snapshot.py
```

This checks payload hashes, JSON/JSONL parsing, record counts, Python source syntax and agreement between the ZIP and the expanded dataset. It needs no model API key, network request or GPU. A passing result establishes package integrity only—not scientific validity, scoring correctness or clinical/other domain applicability.

## Read before using the scores

Known upstream issues are recorded in [PUBLICATION_NOTES.md](PUBLICATION_NOTES.md), including stale version fields, overlapping benchmark-PDF version/date text and a delegation-frontier helper that does not enforce cumulative lower-band retention. Research payloads have not been silently corrected during this upload. Do not use this snapshot alone to issue an official AI-level certificate.

[PUBLIC_SNAPSHOT.json](PUBLIC_SNAPSHOT.json) records the source commit, original archive hashes, original/current theory-PDF hashes and author-amendment provenance, exact member hashes, all exported payloads and the four exclusions. The source is [`integritynoble/sarsi-intelligence-level`](https://github.com/integritynoble/sarsi-intelligence-level) at `446a1bc7b2dfcf7ab02f664d48b1a7fc03f5b008`; its history and unrelated working files were not imported.

## Contributions and reuse

Use this repository's Issues to propose public test forms or report errors. Include the coordinate/level, task, control or ablation, external verification method, provenance and permission to share. Do not submit confidential data, private test answers, access tokens or personal information.

This snapshot does not assign a new software or dataset license. No explicit license accompanied the selected release artifacts; public availability should not be interpreted as an unrestricted reuse grant. Contact the paper authors for reuse permission pending an explicit license decision.
