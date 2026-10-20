"""Check or deliberately update the SHA-256 manifests for fixtures and supplied teaching code.

Run `--check` (the default) to compare files with the recorded hashes. After an intended change
to a fixture, worked solution, starter or fix exercise, run `--update` and review the diff.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TEACHING_PATTERNS = ('solutions/*.py', 'starter/*.py', 'exercises/*.py', 'exercises/solutions/*.py',
                     'exercises/exercises.json', 'part0/*.py', 'part0/replay/*.json')
MANIFESTS = {
    'fixture-manifest.json': None,  # file list is curated; --update only refreshes hashes
    'teaching-code-manifest.json': TEACHING_PATTERNS,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_files(name: str, recorded: dict) -> list[str]:
    patterns = MANIFESTS[name]
    if patterns is None:
        return list(recorded)  # curated order is preserved
    curated = json.loads((HERE / 'fixture-manifest.json').read_text(encoding='utf-8'))['files']
    found = {str(p.relative_to(HERE)) for pattern in patterns for p in HERE.glob(pattern)}
    return sorted(found - set(curated))  # each file is recorded in one manifest only


def check() -> list[str]:
    """Return human-readable differences; an empty list means every manifest matches."""
    problems = []
    for name in MANIFESTS:
        manifest = json.loads((HERE / name).read_text(encoding='utf-8'))
        recorded = manifest['files']
        files = expected_files(name, recorded)
        for missing in sorted(set(files) - set(recorded)):
            problems.append(f'{name}: {missing} is not recorded')
        for extra in sorted(set(recorded) - set(files)):
            problems.append(f'{name}: {extra} is recorded but no longer present')
        for path in sorted(set(files) & set(recorded)):
            if digest(HERE / path) != recorded[path]:
                problems.append(f'{name}: {path} changed')
    return problems


def update() -> None:
    for name in MANIFESTS:
        target = HERE / name
        manifest = json.loads(target.read_text(encoding='utf-8'))
        manifest['files'] = {path: digest(HERE / path) for path in expected_files(name, manifest['files'])}
        target.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='rewrite hashes after an intended change')
    args = parser.parse_args()
    if args.update:
        update()
        print('Manifests updated; review the diff before committing.')
        return 0
    problems = check()
    for problem in problems:
        print(problem, file=sys.stderr)
    print('Manifests match.' if not problems else f'{len(problems)} manifest difference(s); '
          'if intended, run with --update and review the diff.')
    return int(bool(problems))


if __name__ == '__main__':
    raise SystemExit(main())
