"""Offline integrity/structure checks; not a scientific benchmark evaluation."""
from __future__ import annotations

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATASET = 'datasets/ai-level-bench-v0.4/'
ZIP_NAME = 'downloads/AI_Level_Benchmark_Dataset_v0_4_public.zip'
ZIP_ROOT = 'AI_Level_Benchmark_Dataset_v0_4_public/'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_file(relative):
    path = PurePosixPath(relative)
    require(not path.is_absolute() and '..' not in path.parts and '\\' not in relative,
            'Unsafe payload path: ' + relative)
    target = ROOT / relative
    require(target.is_file() and not target.is_symlink(), 'Missing/unsafe file: ' + relative)
    require(target.resolve().is_relative_to(ROOT), 'Path outside snapshot: ' + relative)
    return target


def main():
    manifest = json.loads((ROOT / 'PUBLIC_SNAPSHOT.json').read_text(encoding='utf-8'))
    require(manifest['schema'] == 'ai-level-public-snapshot/v1', 'Unexpected manifest schema')
    payload = manifest['payload']
    require(len(payload) == 159, 'Expected 3 papers, 155 dataset files and 1 ZIP')
    counts = Counter()
    jsonl_records = 0
    for relative, metadata in payload.items():
        file = safe_file(relative)
        raw = file.read_bytes()
        require(len(raw) == metadata['bytes'], 'Size mismatch: ' + relative)
        require(hashlib.sha256(raw).hexdigest() == metadata['sha256'], 'Hash mismatch: ' + relative)
        require('__pycache__' not in file.parts and file.suffix != '.pyc', 'Bytecode in release')
        if file.suffix == '.pdf':
            require(raw.startswith(b'%PDF-'), 'Not a PDF: ' + relative)
        if relative.startswith(DATASET):
            counts[file.suffix] += 1
            if file.suffix == '.json':
                json.loads(raw.decode('utf-8-sig'))
            elif file.suffix == '.jsonl':
                for line in raw.decode('utf-8-sig').splitlines():
                    if line.strip():
                        json.loads(line)
                        jsonl_records += 1
            elif file.suffix == '.py':
                ast.parse(raw.decode('utf-8'), filename=relative)
    dataset_paths = {p for p in payload if p.startswith(DATASET)}
    actual_paths = {str(p.relative_to(ROOT)) for p in (ROOT / DATASET).rglob('*') if p.is_file()}
    require(dataset_paths == actual_paths, 'Dataset files differ from snapshot manifest')
    require(len(dataset_paths) == 155, 'Wrong dataset file count')
    require(counts['.json'] == 89 and counts['.jsonl'] == 43 and jsonl_records == 515,
            'Unexpected structured-data counts')
    require(counts['.py'] == 4 and counts['.png'] == 13, 'Unexpected scorer/image counts')

    def rows(name):
        return [json.loads(line) for line in safe_file(DATASET + name).read_text(encoding='utf-8').splitlines()
                if line.strip()]

    catalog = rows('canonical_method_catalog.jsonl')
    matrix = rows('level_benchmark_matrix.jsonl')
    forms = rows('ai_level_bench_public_dev_combined.jsonl')
    require(len(catalog) == len(matrix) == 82 and len(forms) == 124, 'Unexpected catalog/form counts')
    require(Counter(row['binding_status'] for row in catalog) ==
            {'development-bound': 56, 'specification-only': 26}, 'Unexpected method binding counts')

    with zipfile.ZipFile(safe_file(ZIP_NAME)) as archive:
        require(archive.testzip() is None, 'ZIP CRC failure')
        names = archive.namelist()
        expected = {ZIP_ROOT + p[len(DATASET):] for p in dataset_paths}
        require(len(names) == len(set(names)) and set(names) == expected, 'Unexpected ZIP members')
        for name in names:
            relative = DATASET + name[len(ZIP_ROOT):]
            require(archive.read(name) == safe_file(relative).read_bytes(), 'ZIP content mismatch: ' + name)

    print('PASS: all 159 payload hashes and sizes match the publication manifest')
    print('PASS: 155 dataset files match all 155 download ZIP members; no bytecode')
    print('PASS: 89 JSON files, 43 JSONL files / 515 rows, and 4 Python syntax checks')
    print('PASS: 82 method records, 82 matrix records, 124 combined public forms, 13 images')
    print('LIMIT: integrity/structure only; historical metadata and scorer issues remain')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, SyntaxError, zipfile.BadZipFile) as exc:
        raise SystemExit('FAIL: ' + str(exc))
