# Publication notes

_Snapshot prepared 2026-09-13 from source commit `446a1bc7b2dfcf7ab02f664d48b1a7fc03f5b008`._

## Selection and provenance

| Published artifact | Source in the original repository |
|---|---|
| Theory v2.6 PDF | The named PDF member of `plan/10/AI_Level_Research_Package_v2_6_v0_3.zip`, followed by the author-only amendment documented below |
| Benchmark v0.4 PDF | `plan/10/AI_Level_Bench_v0_4.pdf` |
| Index v2.0 companion PDF | `ail_index_v2/The_AI_Level_Index_v2_0.pdf` |
| Public dataset v0.4 | `plan/10/AI_Level_Benchmark_Dataset_v0_4_complete.zip`, excluding four `__pycache__/*.pyc` members |

The benchmark and Index PDFs and the 155 retained dataset files are byte-identical to their selected source files/archive members. The current theory PDF differs from its source member only through the author-only amendment documented below; it is not byte-identical to that source member. The downloadable ZIP is rebuilt from those 155 files with a public-snapshot root name; it intentionally has a different hash from the original complete ZIP. Source and published hashes, including the original/current theory-PDF hashes and amendment provenance, are recorded in [PUBLIC_SNAPSHOT.json](PUBLIC_SNAPSHOT.json).

The enclosing research-package ZIP is not published: its other members are superseded benchmark v0.3 and dataset v0.3 artifacts. The source repository's newer cell-grid/generated material, runtime records, untracked drafts, local test edits, credentials, organizer-only archives and Git history are not part of this snapshot.

## Theory PDF author-only amendment — September 13, 2026

At the owner's explicit request, the public theory PDF now lists **Chengshuai Yang, Ting Xue and Dingyi Kang — NextGen PlatformAI C Corp, USA**. Only the author line, author running headers and PDF Author metadata were amended. The scientific text, equations, figures, tables, results and existing contribution statement are unchanged; no contributions or coauthor consent are invented by the edit.

The original two-author PDF remains recoverable at repository commit `12331315048e1cbf35a706f80ba572be81dcdd78`: [original PDF](https://github.com/integritynoble/artificial-intelligence-levels/blob/12331315048e1cbf35a706f80ba572be81dcdd78/papers/Unified_Intelligence_Theory_and_AI_Level_v2_6.pdf). No matching editable v2.6 source had been found when that amendment was made, so it is a direct PDF author amendment, not a source rebuild or a new scientific version. The manuscript source was published on 2026-09-17 in [`paper-sources/`](paper-sources/README.md); its author line has not been amended, and reconciling it with the amended PDF remains part of DK-02.

Author-order confirmation, actual contribution verification, all-author consent, editable-source synchronization and the anonymous TMLR submission edition remain pending under [Dingyi's assignment](DINGYI_KANG_PAPER_TASKS.md). The public PDF amendment does not complete DK-02, approve scientific claims or authorize journal submission.

The [amendment tool](tools/amend_theory_authors.py) reproduces the edit from the pinned Git original using the existing embedded font. It checks all 69 pages: text and positions outside the author regions are identical, rendered pixels outside those regions match at 144 dpi, and all 265 links are unchanged. Pages 66–69 are visually unchanged. The title page was also visually reviewed. These checks establish the amendment's scope, not scientific correctness.

To reproduce into a new, non-existing file with PyMuPDF and Pillow installed (verified with PyMuPDF 1.27.1), run `python3 -B tools/amend_theory_authors.py --output /tmp/ai-level-author-amendment-check.pdf`. The repository must contain recovery commit `12331315048e1cbf35a706f80ba572be81dcdd78`; the script refuses an existing output unless explicitly replacing the exact original release PDF.

## Known issues retained from upstream

1. **Version metadata is inconsistent.** Dataset Markdown and the archive manifest identify v0.4, while `dataset_card.json` retains `version: "0.8"`. Some scorer headers also retain older version labels. The root snapshot metadata records the selected release versions without rewriting these research artifacts.
2. **The benchmark PDF contains overlapping version/date strings.** Text extraction from its first page includes v0.4 and v0.2, and September 6 and September 3 dates. The filename/release bundle identifies the selected artifact; this upload does not repair its typesetting or claim the old editable sources rebuild it.
3. **Upstream inventories are historical.** `file_inventory.txt`, the dataset's `manifest.json` and `validation_report.json` are preserved upstream artifacts, not a newly generated inventory or validation certificate for this public snapshot. Use the root `PUBLIC_SNAPSHOT.json` and the verification command for the actual exported payload.
4. **The scorers are illustrative, not certification-complete.** In particular, `verifiers/harmonized_scoring.py::delegation_frontier` takes the maximum individually passing T band without enforcing that every lower T band passes at the same H ceiling. This does not implement the cumulative DI rule described by the dataset. No scorer fix or new scoring convention is introduced here.
5. **Published numbers remain historical.** Paper tables may use older instruments, scoring versions or preliminary samples. Uploading the PDFs does not reproduce those experiments, validate model rankings or resolve previously reported benchmark failures.
6. **Public development is not private certification.** Descriptions of hidden witnesses or certification protocols in public forms are specifications, not protected instances. Explicitly labelled development keys, including `hidden_defect_key_dev_public`, are public reference material, never secure certification answers. Specification-only entries do not establish runnable tests. This release does not expose a secret evaluation salt or certify all intelligence levels.
7. **Licensing remains explicit work.** No license file was present in the selected release archives. This upload does not copy a license from an unrelated historical package or create a new grant.

## Verification scope

`python3 -B tools/verify_public_snapshot.py` verifies hashes for every manifest payload, matching expanded/ZIP bytes, structural record counts, JSON/JSONL parsing and scorer syntax. It does not execute the scorers, load model weights, call providers, rerun paper experiments, inspect hidden datasets or establish benchmark validity.

Before a certification-oriented release, resolve the metadata/typesetting issues, test and repair scorer semantics, supply matching editable paper sources and an explicit license, and separately validate the full runtime and protected evaluation protocol. Technical upload completion and owner acceptance of scientific claims are different decisions; no scientific acceptance is recorded here.
