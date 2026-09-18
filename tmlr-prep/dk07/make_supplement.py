#!/usr/bin/env python3
"""DK-07: build the anonymous reproducibility supplement, then prove it is anonymous.

Two variants:

    --variant scripts   analysis code, tests and instructions only. Carries no
                        third-party data, so it needs no rights decision, but it
                        cannot be reproduced without separately obtaining the
                        evidence archive - which is stated plainly in its README
                        rather than glossed as "available online".

    --variant full      the same, plus the evidence archive's contents. This is
                        the only variant that is actually reproducible offline,
                        and it is the one that needs the owner's rights decision.

Anonymisation is explicit, and every substitution is logged:

  * The evidence archive's own README carries a Citation naming an author. That
    section is removed and replaced by a neutral line.
  * Our working files carry task identifiers (DK-05, DK-06) and the path
    tmlr-prep. The public repository contains a task file named after the author,
    so those strings are searchable and identifying. They are renamed.

After building, the script scans every file in the package - and every entry of
every nested archive - for identifying strings, then reports the result. A
non-empty finding is a build failure, not a warning.

Usage:
    python3 make_supplement.py --variant full --sources <repo> --evidence <unpacked archive> --outdir <dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import io
import re
import shutil
import zipfile
from pathlib import Path

# Strings that would identify the authors, their institution or the repository.
# Substrings are matched anywhere; surnames need a word boundary, or "Ting"
# matches "supporting", "routing" and "accounting" and the scan drowns in noise.
IDENTIFYING_SUBSTRINGS = [
    "Chengshuai", "Dingyi", "NextGen", "PlatformAI", "platformai", "spiritai",
    "integritynoble", "sarsi-intelligence", "tmlr-prep", "DK-0",
]
IDENTIFYING_WORDS = ["Yang", "Xue", "Kang", "Ting"]
# Third-party authors whose surnames legitimately appear when their work is
# cited; these are not leaks.
ALLOWED_CONTEXT = [
    "John Yang",        # SWE-bench author
    "Xueguang Ma",      # MMLU-Pro author
]

FIXED_TIME = (1980, 1, 1, 0, 0, 0)  # deterministic ZIP timestamps

# A git commit id is a precise pointer: searched on a hosting service it names
# the repository it came from, and therefore its owner. Nothing in the package
# reads these fields, so they are removed rather than kept and hoped about.
COMMIT_FIELD = re.compile(r"_commit$")
WITHHELD = "withheld for anonymous review"

# Fields that carry, or point at, the answer to an evaluation item.
ANSWER_FIELD = re.compile(r"expected|answer|solution|gold|verifier|rubric", re.I)


def truthy(value) -> bool:
    """The benchmark corpus stores booleans as the strings "True"/"False".

    Comparing with `is True` matches nothing and silently reports a clean
    separation that does not exist, so every flag goes through here.
    """
    return str(value).strip().lower() == "true"


def neutralise_provenance(root: Path, log: list[str]) -> dict[str, str]:
    """Replace git commit ids in the archive's manifests with a withheld marker."""
    changed: dict[str, str] = {}
    for path in sorted(root.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        hits: list[str] = []

        def walk(node, trail=""):
            if isinstance(node, dict):
                for key, value in node.items():
                    if COMMIT_FIELD.search(key) and isinstance(value, str) and value != WITHHELD:
                        node[key] = WITHHELD
                        hits.append(f"{trail}.{key}".lstrip("."))
                    else:
                        walk(value, f"{trail}.{key}")
            elif isinstance(node, list):
                for i, value in enumerate(node):
                    walk(value, f"{trail}[{i}]")

        walk(data)
        if hits:
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            changed[str(path.relative_to(root))] = "git commit id removed"
            for hit in hits:
                log.append(f"withheld commit id {path.name}:{hit}")
    return changed


def reseal_archive_checksums(root: Path, changed: dict[str, str], log: list[str]) -> None:
    """Rewrite the archive's checksums.sha256 to match the anonymised files.

    Anonymisation edits files the archive lists in its own checksums, so its
    bundled validator reports them as mismatches and exits 1 - a package that
    looks tampered with. Resealing keeps the validator meaningful for every
    file we did not touch; ANONYMISATION.md records the ones we did, with both
    the released and the resealed digest, so nothing is hidden by the reseal.
    """
    checksums = root / "checksums.sha256"
    if not checksums.exists() or not changed:
        return

    lines, reseal = [], []
    for line in checksums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, _, relative = line.partition("  ")
        target = root / relative
        if relative in changed and target.exists():
            new = hashlib.sha256(target.read_bytes()).hexdigest()
            reseal.append((relative, digest, new, changed[relative]))
            digest = new
        lines.append(f"{digest}  {relative}")
    checksums.write_text("\n".join(lines) + "\n", encoding="utf-8")

    note = [
        "# Files altered for anonymous review",
        "",
        "Three kinds of change were made to the released archive so it could be",
        "shipped for anonymous review: an author name was removed from its README,",
        "and git commit ids were removed from its manifests. Nothing else was",
        "touched, and no measurement, row or result was modified.",
        "",
        "`checksums.sha256` was resealed afterwards so the archive's own",
        "`tools/validate.py` still verifies every other file. The released digests",
        "are recorded here so the untouched files can still be checked against the",
        "public release, and so these edits can be audited after de-anonymisation.",
        "",
        "| File | Change | Released SHA-256 | In this package |",
        "|---|---|---|---|",
    ]
    for relative, old, new, why in sorted(reseal):
        note.append(f"| `{relative}` | {why} | `{old}` | `{new}` |")
    (root / "ANONYMISATION.md").write_text("\n".join(note) + "\n", encoding="utf-8")

    # validate.py also requires the recorded path set to equal the package's
    # file set, so the new file has to be listed too.
    digest = hashlib.sha256((root / "ANONYMISATION.md").read_bytes()).hexdigest()
    with checksums.open("a", encoding="utf-8") as fh:
        fh.write(f"{digest}  ANONYMISATION.md\n")
    log.append(f"resealed checksums.sha256 for {len(reseal)} anonymised file(s); recorded them in ANONYMISATION.md")


def count_certification_items(root: Path) -> dict:
    """Count evaluation items that ship together with their own answers."""
    out = {"items": 0, "ready": 0, "ready_with_answers": 0, "dev_with_answers": 0}
    for archive in sorted(root.rglob("*.zip")):
        with zipfile.ZipFile(archive) as zf:
            for name in zf.namelist():
                if not name.endswith(".jsonl"):
                    continue
                for line in zf.read(name).decode("utf-8", "ignore").splitlines():
                    line = line.strip()
                    if not line.startswith("{"):
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    out["items"] += 1
                    answers = any(
                        ANSWER_FIELD.search(k) and v not in (None, "", "{}", "[]", "null")
                        for k, v in item.items()
                    )
                    ready = truthy(item.get("certification_ready"))
                    out["ready"] += ready
                    if answers and ready:
                        out["ready_with_answers"] += 1
                    elif answers:
                        out["dev_with_answers"] += 1
    return out


def anonymise_evidence_readme(text: str, log: list[str]) -> str:
    """Remove the Citation section that names an author."""
    out, removed = [], False
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().lower() == "## citation":
            removed = True
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            out.append("## Citation")
            out.append("")
            out.append("Withheld for anonymous review.")
            out.append("")
            continue
        out.append(lines[i])
        i += 1
    if removed:
        log.append("evidence README: replaced the Citation section, which named an author")
    return "\n".join(out) + "\n"


# The test suite loads the published scorers from a repository-relative path.
# Inside the supplement that path does not exist, so the suite must resolve them
# from an environment variable or a bundled copy, and skip - visibly - when it
# cannot. Skipped is honest; a suite that errors out is not.
RESOLVER = '''
def _verifiers_dir():
    """Locate the published development scorers, or return None.

    They are not bundled: they belong to a release with no licence, and no
    result in the paper depends on them. Point AI_LEVEL_VERIFIERS at a copy of
    `datasets/ai-level-bench-v0.4/verifiers` to run the tests that compare
    against them; without it those tests skip rather than fail.
    """
    import os
    for candidate in (os.environ.get("AI_LEVEL_VERIFIERS"), HERE / "published_scorers"):
        if candidate and pathlib.Path(candidate).is_dir():
            return pathlib.Path(candidate)
    return None


VERIFIERS = _verifiers_dir()
'''


def make_tests_standalone(text: str, log: list[str]) -> str:
    """Rewrite the suite so it runs inside the package, skipping what it cannot load."""
    text = text.replace(
        '''REPO = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent''',
        '''HERE = pathlib.Path(__file__).resolve().parent''')
    text = text.replace(
        '''original = _load(
    "harmonized_scoring_v0_4",
    REPO / "datasets/ai-level-bench-v0.4/verifiers/harmonized_scoring.py",
)''',
        RESOLVER + '''
original = _load("harmonized_scoring", VERIFIERS / "harmonized_scoring.py") if VERIFIERS else None''')
    text = text.replace(
        '''VERIFIERS = REPO / "datasets/ai-level-bench-v0.4/verifiers"
gui = _load("gui_scoring_v0_4", VERIFIERS / "gui_scoring.py")
memory = _load("memory_scoring_v0_4", VERIFIERS / "memory_scoring.py")
ai_level = _load("ai_level_scoring_v0_4", VERIFIERS / "ai_level_scoring.py")''',
        '''gui = _load("gui_scoring", VERIFIERS / "gui_scoring.py") if VERIFIERS else None
memory = _load("memory_scoring", VERIFIERS / "memory_scoring.py") if VERIFIERS else None
ai_level = _load("ai_level_scoring", VERIFIERS / "ai_level_scoring.py") if VERIFIERS else None

needs_scorers = unittest.skipUnless(
    VERIFIERS is not None,
    "published development scorers not bundled; set AI_LEVEL_VERIFIERS to run these",
)''')
    # decorate the classes and cases that need the published scorers
    text = text.replace("class OriginalHelperDefect(unittest.TestCase):",
                        "@needs_scorers\nclass OriginalHelperDefect(unittest.TestCase):")
    text = text.replace("class OtherPublishedScorers(unittest.TestCase):",
                        "@needs_scorers\nclass OtherPublishedScorers(unittest.TestCase):")
    text = text.replace("    def test_monotone_surface_matches_original(self):",
                        "    @needs_scorers\n    def test_monotone_surface_matches_original(self):")
    text = text.replace("            old = original.delegation_frontier(surface, h_band, p)\n            if got is not None:\n                self.assertLessEqual(got, old)",
                        "            if original is not None:\n                old = original.delegation_frontier(surface, h_band, p)\n                if got is not None:\n                    self.assertLessEqual(got, old)")
    # the corrected module is renamed in the package; the loader must follow
    text = text.replace('_load("delegation_frontier_cumulative", HERE / "delegation_frontier_cumulative.py")',
                        '_load("frontier_cumulative", HERE / "frontier_cumulative.py")')
    log.append("analysis/test_frontier_cumulative.py: pointed the loader at the renamed module")
    log.append("analysis/test_frontier_cumulative.py: made standalone - the published scorers "
               "are resolved from AI_LEVEL_VERIFIERS or a bundled copy, and the tests that need "
               "them skip visibly when it is absent")
    return text


def neutralise_internal_ids(text: str, log: list[str], name: str) -> str:
    """Strip working-task identifiers that point back at the author's task file."""
    before = text
    text = re.sub(r"\bDK-0(\d)\b", lambda m: f"step {m.group(1)}", text)
    text = text.replace("tmlr-prep/dk05/", "analysis/").replace("tmlr-prep/dk06/", "analysis/")
    text = text.replace("tmlr-prep/dk0", "analysis/dk0").replace("tmlr-prep", "supplement")
    text = text.replace("recompute.py", "recompute.py")  # name is already neutral
    if text != before:
        log.append(f"{name}: removed working-task identifiers (DK-0x, tmlr-prep)")
    return text


def scan_for_leaks(root: Path) -> list[tuple[str, str, str]]:
    """Return (file, term, context) for every identifying string found."""
    findings = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as z:
                for info in z.infolist():
                    for term in IDENTIFYING_SUBSTRINGS:
                        if term.lower() in info.filename.lower():
                            findings.append((f"{path.name}:{info.filename}", term, "archive entry name"))
                    if info.filename.endswith((".md", ".txt", ".json", ".csv", ".py", ".jsonl")):
                        body = z.read(info).decode("utf-8", "ignore")
                        findings += _scan_text(body, f"{path.name}:{info.filename}")
            continue
        for term in IDENTIFYING_SUBSTRINGS:
            if term.lower() in path.name.lower():
                findings.append((str(path.relative_to(root)), term, "file name"))
        if path.suffix in {".md", ".txt", ".json", ".csv", ".py", ".jsonl", ".sha256"}:
            findings += _scan_text(path.read_text(errors="ignore"), str(path.relative_to(root)))
    return findings


def _scan_text(body: str, where: str) -> list[tuple[str, str, str]]:
    out = []
    patterns = [(t, re.escape(t)) for t in IDENTIFYING_SUBSTRINGS]
    patterns += [(t, rf"\b{re.escape(t)}\b") for t in IDENTIFYING_WORDS]
    for term, pat in patterns:
        for m in re.finditer(pat, body, re.I):
            ctx = " ".join(body[max(0, m.start() - 45):m.end() + 45].split())
            if any(a.lower() in ctx.lower() for a in ALLOWED_CONTEXT):
                continue
            out.append((where, term, ctx))
    # A commit id names its repository to anyone who searches for it. Match the
    # field rather than every 40-hex string, so the many content hashes in the
    # manifests are not reported.
    for m in re.finditer(r'"([A-Za-z0-9_]*_commit)"\s*:\s*"([0-9a-f]{7,40})"', body):
        out.append((where, m.group(1), f"git commit id {m.group(2)}"))
    return out


def build(sources: Path, evidence: Path | None, outdir: Path, variant: str) -> tuple[Path, list[str]]:
    log: list[str] = []
    stage = outdir / "supplement"
    if stage.exists():
        shutil.rmtree(stage)
    (stage / "analysis").mkdir(parents=True)

    # analysis code, with internal identifiers neutralised
    for src, dst in (
        (sources / "tmlr-prep/dk05/recompute.py", "analysis/recompute.py"),
        (sources / "tmlr-prep/dk06/delegation_frontier_cumulative.py", "analysis/frontier_cumulative.py"),
        (sources / "tmlr-prep/dk06/test_delegation_frontier.py", "analysis/test_frontier_cumulative.py"),
    ):
        text = neutralise_internal_ids(src.read_text(), log, dst)
        if dst.endswith("test_frontier_cumulative.py"):
            text = make_tests_standalone(text, log)
        (stage / dst).write_text(text)

    if variant == "full":
        if evidence is None:
            raise SystemExit("--evidence is required for the full variant")
        shutil.copytree(evidence, stage / "evidence")
        readme = stage / "evidence/README.md"
        readme.write_text(anonymise_evidence_readme(readme.read_text(), log))
        changed = {"README.md": "author name removed from the Citation section"}
        changed.update(neutralise_provenance(stage / "evidence", log))
        reseal_archive_checksums(stage / "evidence", changed, log)

    counts = count_certification_items(stage) if variant == "full" else None
    (stage / "README.md").write_text(readme_text(variant, counts))

    # manifest of every file, then a deterministic ZIP
    lines = []
    for p in sorted(stage.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.sha256":
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(stage)}")
    (stage / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")

    zip_path = outdir / f"supplement_{variant}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(stage.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(str(p.relative_to(stage)), date_time=FIXED_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, p.read_bytes())
    log.append(f"wrote {zip_path.name} with fixed timestamps and no owner/group metadata")
    return zip_path, log


def readme_text(variant: str, counts: dict | None = None) -> str:
    reproducible = variant == "full"
    if counts and counts["items"]:
        separation = f"""This package includes an inherited coordinate benchmark corpus of
{counts['items']:,} items, and **the answers are in it**. Of those items,
{counts['ready']} are flagged `certification_ready`, and
{counts['ready_with_answers']} of those ship with their own answer material -
`expected_json`, a named `verifier`, or the expected difficulty and headroom
fields. A further {counts['dev_with_answers']} development items also carry
answers, which is what a development corpus is for.

Read the certification-ready items as **disclosed**, not as a sealed evaluation
set. Anyone holding this supplement can read the expected answer for them, so a
score obtained by a system with access to this file is not evidence of
capability. No credential, access token or evaluation salt is included; this is
a statement about answer visibility, not about secrets."""
    else:
        separation = """No evaluation item corpus is included in this variant, so no answer material
ships with it. No credential, private answer key or evaluation salt is included."""
    return f"""# Supplementary material

Anonymous supplement. Everything here runs offline with Python 3.9 or newer and
the standard library only: no third-party packages, no model API key, no network
access, no GPU, and no cost.

## What this reproduces

`analysis/recompute.py` recomputes the paper's reported numbers from the
released evidence rows and compares each against the value printed in the paper.
It reimplements the paper's definitions rather than calling the evidence
archive's own analysis script, so agreement is not an artifact of a shared
implementation.

`analysis/frontier_cumulative.py` is a corrected implementation of the
delegation frontier, which the published development scorer computes without
the cumulative lower-band condition the paper requires.
`analysis/test_frontier_cumulative.py` is its regression suite, including a
randomised check against the rule as stated in the benchmark's own policy file.

## Steps

{"```text" if reproducible else "```text"}
{'python3 analysis/recompute.py --dataset evidence' if reproducible else 'python3 analysis/recompute.py --dataset <path to the evidence archive>'}
python3 -m unittest -v analysis/test_frontier_cumulative.py
{"```"}

Expected output:

- the recomputation reports **52 of 53** reported values reproducing, plus
  **132 of 132** cells of the two per-seed tables and **17 of 17** protocol
  claims. The single discrepancy is a rounding slip in prose that the paper's
  own tables contradict.
- the test suite reports **15 tests, 8 passing and 7 skipped**, exit code 0. The
  seven skips compare against the published development scorers, which are not
  bundled (see below); they run if you set `AI_LEVEL_VERIFIERS` to a copy of
  that directory, and then all 15 pass.

## What is included, and what is not

{"The evidence archive is included under `evidence/`, so the steps above run as written." if reproducible else "**The evidence archive is not included here.** The steps above therefore cannot be run from this supplement alone: they require the archive named in the paper's data-availability section, which is distributed separately. This package does not claim anonymous reproducibility."}

**The published development scorers are not bundled.** They belong to a release
that carries no licence, and no result in the paper depends on them. The tests
that compare the corrected frontier against the published one therefore skip
unless `AI_LEVEL_VERIFIERS` points at a copy.

Not included, and not available to us either:

- The scoring utility that produced the harness-curve figures. The paper names
  it; it is not in any released archive.
- The item generators, reference solvers and specification-key tests behind the
  item-family accuracies. The paper states that these are not released.
- Two of the three harness-scaling curves. Only one executor's episode rows were
  released; the other two curves appear in the paper's tables only.
- The record of one of the two library audits.

## Evidence classes

Reproduction means different things for different rows, and the recomputation
labels each one:

- **archived**: original observations, hash-matched to the study manifest.
- **reconstructed**: rows rebuilt from an aggregate log after the run. Agreement
  shows the reconstruction is consistent with the published table, not that the
  original run produced those rows.
- **published tables only**: no artifact; arithmetic consistency is all that can
  be checked.

## Which items here have their answers attached

{separation}
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True, type=Path)
    ap.add_argument("--evidence", type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--variant", choices=("scripts", "full"), required=True)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    zip_path, log = build(args.sources, args.evidence, args.outdir, args.variant)
    print(f"== build log ({args.variant})")
    for line in log:
        print(f"   {line}")

    size = zip_path.stat().st_size
    print(f"\n== package: {zip_path.name}  {size/1024/1024:.2f} MB  "
          f"({'within' if size <= 100*1024*1024 else 'OVER'} the 100 MB limit)")

    findings = scan_for_leaks(args.outdir / "supplement")
    print(f"\n== identity scan: {len(findings)} finding(s)")
    for where, term, ctx in findings:
        print(f"   LEAK {where}: {term!r} in {ctx[:90]}")
    if findings:
        raise SystemExit("identity leak found; package not fit to ship")
    print("   clean: no author, institution, repository or task identifier in any file or archive entry")


if __name__ == "__main__":
    main()
