"""Fetch only pinned tokenizer assets; validate hashes before use.

Original project loader. Sources and licenses: ../SOURCES.md.
"""
import hashlib
import json
from pathlib import Path
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = json.loads((HERE / 'assets.json').read_text(encoding='utf-8'))
CACHE = ROOT / '.cache/model-input' / MANIFEST['revision']


def checked_assets(directory: Path = CACHE) -> Path:
    """Return the asset directory, or raise ValueError for missing/altered bytes."""
    for name, digest in MANIFEST['files'].items():
        path = directory / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Missing or altered {name}; run lab/prepare.py (see module setup).')
    return directory


def prepare() -> None:
    """Download a fixed allowlist; retain upstream LICENSE alongside original bytes."""
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, digest in MANIFEST['files'].items():
        target = CACHE / name
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
            continue
        url = f"https://huggingface.co/{MANIFEST['repository']}/resolve/{MANIFEST['revision']}/{name}"
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read(12_000_001)
        if len(data) > 12_000_000 or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f'Unexpected bytes for {name}; no cache file replaced.')
        temporary = target.with_suffix(target.suffix + '.download')
        temporary.write_bytes(data)
        temporary.replace(target)
    checked_assets()
    print(f'Verified pinned tokenizer/template/license: {CACHE}')
