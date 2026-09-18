#!/usr/bin/env python3
"""Audit a built supplement for four properties the build itself does not check.

The leak scanner in make_supplement.py answers "does the package name anyone".
These are the other claims the DK-07 record makes, each of which was asserted
before it was measured:

  1. dependencies   every packaged module imports only the standard library
  2. links          no embedded link, and in particular none that identifies
                    an author, institution or repository
  3. separation     development examples are distinct from the evaluation
                    instances the corpus marks certification-ready
  4. self-check     the bundled archive still passes its own validator, which
                    anonymising files it checksums would otherwise break

Usage:
    python3 audit_supplement_contents.py build/supplement_full.zip

Exit status is 0 when every check passes and 1 when any check reports a
finding, so it can gate a build the same way the leak scan does.
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import zipfile

# Fields that carry, or point at, the answer to an evaluation item.
ANSWER_FIELD = re.compile(r"expected|answer|solution|gold|verifier|rubric", re.I)

# A link that identifies the work, as opposed to a standards or specification URL.
IDENTIFYING_HOST = re.compile(
    r"github\.com/integritynoble|platformai|physicsworldmodel|spiritai|okstate",
    re.I,
)
LINK = re.compile(r"(?:https?://|mailto:)[^\s)\"',]+")


def truthy(value) -> bool:
    """The corpus stores booleans as the strings "True"/"False", not as JSON booleans.

    Comparing with `is True` silently matches nothing and reports a clean
    separation that does not exist, so every flag goes through here.
    """
    return str(value).strip().lower() == "true"


def check_dependencies(root: pathlib.Path) -> list[str]:
    findings = []
    local = {p.stem for p in root.rglob("*.py")}
    stdlib = set(sys.stdlib_module_names)
    for path in sorted(root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError as exc:
            findings.append(f"{path.relative_to(root)}: will not parse: {exc}")
            continue
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imported.add(node.module.split(".")[0])
        external = sorted(imported - stdlib - local)
        if external:
            findings.append(f"{path.relative_to(root)}: third-party import {external}")
    return findings


def check_links(root: pathlib.Path) -> tuple[list[str], collections.Counter]:
    findings: list[str] = []
    seen: collections.Counter = collections.Counter()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for url in LINK.findall(text):
            seen[url] += 1
            if IDENTIFYING_HOST.search(url):
                findings.append(f"{path.relative_to(root)}: identifying link {url}")
    return findings, seen


def check_separation(root: pathlib.Path) -> tuple[list[str], dict]:
    """Report evaluation items that ship together with their own answers."""
    summary = {
        "items": 0,
        "certification_ready": 0,
        "certification_ready_with_answers": 0,
        "development_with_answers": 0,
        "fields": collections.Counter(),
        "per_benchmark": collections.Counter(),
    }
    corpora = [p for p in root.rglob("*.zip")]
    for archive in corpora:
        with zipfile.ZipFile(archive) as zf:
            for name in zf.namelist():
                if not name.endswith(".jsonl"):
                    continue
                body = zf.read(name).decode("utf-8", "ignore")
                for line in body.splitlines():
                    line = line.strip()
                    if not line.startswith("{"):
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    summary["items"] += 1
                    answers = {
                        k
                        for k, v in item.items()
                        if ANSWER_FIELD.search(k) and v not in (None, "", "{}", "[]", "null")
                    }
                    ready = truthy(item.get("certification_ready"))
                    if ready:
                        summary["certification_ready"] += 1
                    if answers and ready:
                        summary["certification_ready_with_answers"] += 1
                        summary["per_benchmark"][name.split("/")[1]] += 1
                        for field in answers:
                            summary["fields"][field] += 1
                    elif answers:
                        summary["development_with_answers"] += 1

    findings = []
    if summary["certification_ready_with_answers"]:
        findings.append(
            f"{summary['certification_ready_with_answers']} items marked "
            f"certification_ready ship with answer material "
            f"({dict(summary['fields'])})"
        )
    return findings, summary


def check_self_validation(root: pathlib.Path) -> tuple[list[str], str]:
    """Run the bundled archive's own validator, if the variant carries one.

    Anonymisation edits files the archive lists in checksums.sha256, so without
    resealing them its validator exits 1 and the package looks tampered with.
    """
    validator = root / "evidence" / "tools" / "validate.py"
    if not validator.exists():
        return [], "no bundled archive in this variant"
    proc = subprocess.run(
        [sys.executable, "tools/validate.py"],
        cwd=validator.parent.parent,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return [], "the archive validates against its own checksums (exit 0)"
    detail = (proc.stdout + proc.stderr).strip().splitlines()
    return (
        [f"the bundled archive fails its own validator (exit {proc.returncode})"],
        " | ".join(line.strip() for line in detail[-6:]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=pathlib.Path)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        with zipfile.ZipFile(args.package) as zf:
            zf.extractall(root)

        print(f"auditing {args.package}\n")

        dep = check_dependencies(root)
        print("1. dependencies")
        print(f"   {'FINDING' if dep else 'standard library only'}")
        for f in dep:
            print(f"     {f}")

        link, seen = check_links(root)
        print("\n2. embedded links")
        for url, count in sorted(seen.items()):
            print(f"   {count:>3}x  {url}")
        if not seen:
            print("   none")
        print(f"   identifying links: {len(link)}")
        for f in link:
            print(f"     {f}")

        sep, summary = check_separation(root)
        print("\n3. development versus certification instances")
        if not summary["items"]:
            print("   no item corpus in this variant")
        else:
            print(f"   items                                : {summary['items']}")
            print(f"   marked certification_ready           : {summary['certification_ready']}")
            print(f"   ...of those, shipping with answers   : {summary['certification_ready_with_answers']}")
            print(f"   development items with answers       : {summary['development_with_answers']}")
            if summary["per_benchmark"]:
                print(f"   per benchmark                        : {dict(summary['per_benchmark'])}")
        for f in sep:
            print(f"   FINDING: {f}")

        selfcheck, detail = check_self_validation(root)
        print("\n4. the archive's own validator")
        print(f"   {detail}")
        for f in selfcheck:
            print(f"   FINDING: {f}")

        findings = dep + link + sep + selfcheck
        print(f"\n{len(findings)} finding(s)")
        return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
