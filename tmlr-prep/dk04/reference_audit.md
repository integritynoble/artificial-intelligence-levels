# DK-04 reference audit — all 30 references

_Prepared 2026-09-18 against `paper-sources/unified-theory/references.bib` (SHA-256 `16792e3a…5d328`). Every entry was checked against the cited work itself, not against memory or a search snippet._

## Method

| Group | How it was verified |
|---|---|
| 16 entries with an arXiv identifier | Queried the arXiv API for each identifier and compared the returned title and publication year with the entry |
| 5 entries with a DOI | Queried Crossref for each DOI and compared title, container, volume, issue, pages and year |
| 4 conference entries with page ranges | Checked against the publisher's own record (PMLR and the ACL Anthology) |
| 1 technical report with a specific month | Checked against the issuing organization's published report |
| 4 standard works without identifiers | Checked against the publisher or standards body record |

## Result

**29 of 30 entries are correct in every checked field. One has a wrong month.**

### The one error

| Entry | Field | Bib says | Actual |
|---|---|---|---|
| `arc2026` | month | April 2026 | The ARC Prize Foundation released ARC-AGI-3 on **25 March 2026** and published the technical report on **27 March 2026** |

The title, author (ARC Prize Foundation), institution and year are correct; only the month is wrong. Proposed correction in the change log (item 15).

### Verified by arXiv identifier (16)

All titles and years match:

`hendrycks2025agi` 2510.18212 · `phan2025hle` 2501.14249 · `wang2024mmlupro` 2406.01574 · `rein2023gpqa` 2311.12022 · `glazer2024frontiermath` 2411.04872 · `jain2024livecodebench` 2403.07974 · `jimenez2023swebench` 2310.06770 · `yao2024taubench` 2406.12045 · `wei2025browsecomp` 2504.12516 · `mialon2023gaia` 2311.12983 · `yue2023mmmu` 2311.16502 · `lu2023mathvista` 2310.02255 · `hsieh2024ruler` 2404.06654 · `xie2024osworld` 2404.07972 · `maharana2024locomo` 2402.17753 · `li2025screenspotpro` 2504.07981

### Verified by DOI (5)

| Entry | Checked | Result |
|---|---|---|
| `sheridan1978` | 10.21236/ADA057655 | title and year match |
| `parasuraman2000` | 10.1109/3468.844354 | IEEE Trans. SMC–Part A **30(3):286–297, 2000** — matches |
| `endsley1999` | 10.1080/001401399185595 | Ergonomics **42(3):462–492, 1999** — matches |
| `klein2004` | 10.1109/MIS.2004.74 | IEEE Intelligent Systems **19(6):91–95, 2004** — matches |
| `lee2004` | 10.1518/hfes.46.1.50.30392 | Human Factors **46(1):50–80, 2004** — matches |

### Verified against the publisher's record (4)

| Entry | Claimed | Publisher record |
|---|---|---|
| `morris2024levels` | PMLR 235:36308–36321, 2024 | matches (`proceedings.mlr.press/v235/morris24b.html`) |
| `chiang2024arena` | PMLR 235:8359–8388, 2024 | matches (`proceedings.mlr.press/v235/chiang24b.html`) |
| `patil2025bfcl` | PMLR 267:48371–48392, 2025 | matches (`proceedings.mlr.press/v267/patil25a.html`); PMLR 267 is the 42nd ICML, 2025 |
| `bai2024longbench` | ACL 2024, 3119–3137 | matches (`aclanthology.org/2024.acl-long.172`) |

### Standard works and reports (4, plus the one error above)

`openai2024simpleqa` (OpenAI technical report, 2024), `amershi2019` (CHI 2019), `perrow1984` (Basic Books, 1984), `sae2021j3016` (SAE J3016, 2021 revision) — all correct as cited.

## How the references are used in the text

Verifying a reference list is not only checking that the works exist; it is checking that the paper says true things about them. Each in-text characterization was compared with the cited work:

| Where | What the paper says | Correct? |
|---|---|---|
| §12 | "The levels-of-automation tradition (Sheridan & Verplank 1978; Parasuraman et al. 2000; Endsley & Kaber 1999) established that autonomy is graded and multi-stage" | Yes |
| §12 | "Klein et al. (2004) and Amershi et al. (2019) add the requirement that automation acting as a team member be predictable and directable" | Yes |
| §12 | "Lee & See (2004) supplies the account of reliance this framework's intervention axis operationalizes" | Yes |
| §18.7 | "Morris et al. separate performance, generality and autonomy and argue for staged operational definitions rather than a binary AGI label" | Yes |
| §18.7 | "Hendrycks et al. define AGI in terms of versatility and proficiency across a psychometrically grounded set of cognitive domains" | Yes — the paper defines AGI as matching the cognitive versatility and proficiency of a well-educated adult, grounded in Cattell–Horn–Carroll theory across ten domains |
| §22 | "Irreversibility … follows Perrow (1984); indexing an autonomy claim by the conditions it holds under follows SAE International (2021)" | Yes |
| Table 37, §18.1 | One-line characterizations of 18 contemporary benchmarks | Consistent with each benchmark's own description |

No reference is cited for a claim it does not support, and no citation was found attached to the wrong work.

## Novelty claims

Every "first" in the paper is scoped to the paper's own framework — "the first instantiation of the ladder", "the first measured harness scaling curves", "the first axis built outside the envelope" — rather than to the field. Read in context this is accurate, since it refers to the first instantiation *of this framework's* ladder. A reviewer skimming §1.2 could read "the first measured harness scaling curves" as a field-first claim, so a three-word qualifier would remove the ambiguity (change log item 16, low priority).

The paper also states plainly what it does **not** claim: §18.7 positions AI-Level as "a harness-centric complement to capability- and human-reference-centered definitions rather than a replacement".
