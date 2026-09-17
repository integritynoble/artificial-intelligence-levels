# DK-01 input inventory — versions, hashes, shareability

_Prepared 2026-09-17. Repository `f0f2931`, branch `dingyi/tmlr-prep`. Sources delivered by the owner in commit `de19f09` ("Publish the theory paper's editable source, figure code and ancillary dataset") with the cover note `PAPER_SOURCE_HANDOVER_EMAIL.md` (`f0f2931`)._

## 1. Manuscript source

| File | SHA-256 | Role | Shareable |
|---|---|---|---|
| `paper-sources/unified-theory/main.tex` (208,032 B) | `f656561662361db260adfc72f2145fd96062d9649957c5db141fa7831cdba60c` | The whole manuscript, one file | Yes (public repo) |
| `references.bib` (8,277 B, 30 entries) | `16792e3a30262e48a858efd02e0e2766125d7c6457fc5e8804fa2224bcd3d328` | Bibliography | Yes |
| `main.bbl` | `de79f5b04fb2e34ab4f95c36936bc4497d933afc4eb644198166e29e47b76043` | Pre-built bibliography (no BibTeX run needed) | Yes |
| `fig_hsc.pdf` | `3b07eff65544b8a06e84a1817afa28eab5efa1ab62c6e2ab0c204924ab7adf17` | Figure 2 as used by the build | Yes |
| `fig_regime.pdf` | `08766800ec0ffc512261f5127d3b3087256b62741c3c3eb1b52a1a981b6171a9` | Figure 1 as used by the build | Yes |
| `addenda_v2_5_v2_6.tex` | `411b2eb20627c01030a954cc23e5b984be3389893d3032ca4da29816e4d4c7af` | **Transcription** of published pp. 66–69; not included by `main.tex`; the PDF remains authoritative | Yes |
| `build_arxiv.sh` | `0430b784add912490dfc8d96bb5055a64f6df7d279ae714ec7dab17dc7676c45` | arXiv build script (names its output `..._v2_4.pdf`) | Yes |
| `ARXIV.md` | `4280c7f048d0d2f54b7c75a36d522adacbdc99796f00c5fd498c03a4db6c732f` | Submission notes | Yes |
| `abstract_arxiv.txt` | `bba30e053538af0d3f21676913a4600a3cc00488858ad1c60afc09ea65c8d112` | Plain-text abstract | Yes |
| `paper-sources/README.md` | `d1c53b8dbca23804db7543d224b0054c132ba090a4231d0298ed5873fa1d8fa6` | Owner's file-by-file map, version explanation and known gaps; **its build instruction says two `pdflatex` passes, which is one too few** | Yes |
| `paper-sources/figures/README.md` | `7b707e2b28e5716301675d829d459da1956018a4ef0065dc632292387295c819` | Figure provenance notes | Yes |

All 16 files under `paper-sources/` are listed here (9 manuscript files, 5 figure-code files in §2, and the 2 documentation files above).

No custom `.sty` files: the preamble uses standard TeX Live packages. Verified with TeX Live 2025 / pdfTeX 1.40.27.

## 2. Figure code and its data

| File | SHA-256 | Notes |
|---|---|---|
| `paper-sources/figures/make_figures.py` | `308a79dec14decf97e2d0e830d2fa8b76565249ce4d5e3cd37b804c19dd386d0` | Redraws both figures; **a rewrite**, not the original script; needs matplotlib |
| `data/regime_switch_frontier.csv` | `97ac14a02b6ac666f527b3dab1a7ab2d6badba965f4e52c8c8156d15c9ab6c54` | **Byte-identical to the archived CSV.** Two independent checks: the hash matches `source_hashes.frontier.csv` in the study manifest, and a direct `cmp` against `evidence/regime_switch/frontier.csv` inside the dataset reports no difference |
| `data/regime_switch_haiku.csv` | `ca95e0f1008280ef49cefad0930bd51185a7669121c37a214467b3d622c7bde8` | Same, verified the same two ways against `evidence/regime_switch/haiku.csv` |
| `data/hsc_curves.csv` | `6dfc55fd2ad68fe4117ad6b5eb0fb993692ca3af365a07b7e01e73cc752fa828` | **Transcribed from the paper's tables**, all three curves (raw and net) |
| `data/hsc_family_a_stronger_rungs.csv` | `abfbce796f613a2ba9b83680516af9f72558e1d55b92504ae443efa625f5b26b` | Per-rung values for the one curve with released episode evidence |

## 3. Ancillary dataset (the archive the paper's data statement names)

`downloads/Unified_Intelligence_Paper_Dataset.zip` — SHA-256 `decc0d4aa911d3dc06e8dee2551b891a499582a7a1e804488b6b468d1b41a83f`, 489,175 B, 27 members, root `Unified_Intelligence_v2_0_Paper_Dataset/`.

| Group | Contents | Checks run |
|---|---|---|
| Harness-scaling-curve evidence | `episodes.csv` (48 rows), `rung_results.csv`, `resource_summary.csv`, `analysis_results.json`, `canonical_report.txt`, `study_manifest.json` | `validate.py` → `hsc_episodes: 48`, `errors: []` |
| Regime-switch evidence | `frontier.csv`, `haiku.csv`, `paired_results.csv`, `analysis_results.json`, `study_manifest.json` | `validate.py` → `regime_switch_episodes: 24` |
| Analysis code | `tools/analyze.py`, `tools/validate.py`, `tools/build_release.py` | Standard library only; runs with exit 0 |
| Schemas and docs | 2 JSON schemas, `PROTOCOL.md`, `DATA_DICTIONARY.md`, `LIMITATIONS.md`, `README.md`, `run_log_template.csv` | read |
| Inherited dependency | `dependencies/HIL_Coordinate_Benchmark_Datasets_v1_2.zip` (70 files) | Hash `6b1d1517eea503067ee44eb4406a66678107444212cd0b9c382aa161042b5c18` matches the value its own `dependencies/README.md` declares. **Opened and inspected** (see below) |
| Integrity | `checksums.sha256` | 26 of 26 OK, 0 failed |

### 3a. Inside the inherited dependency archive

Opened on the fourth review pass, because the paper's data-availability sentence points at an ancillary archive for its audit tooling. It contains more than the coordinate datasets:

| Item | Relevance to this paper |
|---|---|
| `tools/audit_items.py` | The item-validity audit: recomputes every key it can from reference implementations, so an authoring error fails the build |
| `tools/validate.py`, `tools/verify_development_item.py` | The structural checks the paper contrasts the audit against |
| `docs/AUDIT_v1_1.md` | **The written record the paper's §17.12 describes**: the audit run unchanged against v1.1 reported **45 errors**, matching the "Per-coordinate, v1.1" row of the paper's two-library audit table |
| `tools/c_ladder.py` | Reference implementations and a level-graded generator for **four C families** (causal, logic, factuality, induction) — the *library's* families, **not** the paper's §17 item families |
| `docs/PROTOCOL.md`, coordinate datasets (C/I/O/T/H/SA benches, GUI assets, `scoring_config.json`) | Inherited v1.2 material, aligned to framework v1.9 |

**Not** in this archive: any record of the second audit (the harness-level v1.0 library, 5 structural errors), and any generator, reference solver or specification–key test for the §17 families (expression-language, covering, decidability) — a text search for those family terms returns nothing.

**Naming mismatch to resolve:** the source's data-availability sentence names `HIL_Benchmark_Library_v1_1.zip` as the ancillary archive holding "the three checks". No such file was delivered. The delivered archive is `HIL_Coordinate_Benchmark_Datasets_v1_2.zip`, whose tooling appears to be that material one version on (proposal A9).

**Executor identities recorded in the manifests** (carry these exactly):
- Regime switch: `haiku = claude-haiku-4-5`; **frontier: `model_id: null`, `executor_version: null`, `evidence_status: "not_archived"`** — the owner asks explicitly that this not be filled in after the fact.
- Harness curve: reported executor `Claude Code 2.1.234`, reported model `default`, `reconstructed_model: claude-opus-5` marked `reconstructed_from_local_transcripts`. The "reconstructed" qualifier must travel with the number. Family B is a different vendor's CLI, deliberately unnamed.

## 4. Evidence classification (required by DK-01)

| Class | Items |
|---|---|
| **Original archived observations** | The two regime-switch CSVs (24 episodes; hashes match the manifest and the figure-code copies). Gaps within them: no frontier model ID or executor version, 6 frontier rows lack wall time and target spread, neither file has a termination-reason field. |
| **Reconstructed** | The 48 harness-curve episode rows (rebuilt from the canonical aggregate runner log; the tracked artifact is a text report). Token and resource data (from local transcript caches, deduplicated by message ID). The `claude-opus-5` model identity. |
| **Reported in-line only (no archive)** | The Family B curve, the weaker Family A curve, and the paired HG0/HG1 rerun. `hsc_curves.csv` transcribes these from the paper's tables, so they are not independent evidence. |
| **Not archived / missing** | Raw task workspaces, withheld key directories, criterion registers, acceptance process records, snapshot and restore events, complete routing records, separate termination reasons, and the full host/cost envelope. Also: the generators, reference solvers and specification–key tests **for the §17 item families** (expression-language, covering, decidability — the delivered `c_ladder.py` covers four different, library-side families); the record of the harness-level v1.0 audit (5 structural errors); the archive named `HIL_Benchmark_Library_v1_1.zip`; the reference library behind the §16.1 counts (224/34/30/160); any M1 memory measurement. |
| **Newly available** (found on the fourth pass, previously listed as missing) | The item-audit tooling and its written record: `audit_items.py` and `docs/AUDIT_v1_1.md` (45 errors against v1.1), inside the inherited dependency archive. This evidences one of the paper's two library audits. |
| **Private, not shareable** | `integritynoble/sarsi-intelligence-level` (implementation plans, internal benchmark material, six other papers). The owner will add specific files to the public repository on request. |

## 5. Environment used for these checks

TeX Live 2025 (pdfTeX 1.40.27); Python 3.12.6; macOS 26.5.2 arm64; PyMuPDF 1.28.2 and matplotlib in a throwaway virtual environment (system `python3` has no matplotlib).
