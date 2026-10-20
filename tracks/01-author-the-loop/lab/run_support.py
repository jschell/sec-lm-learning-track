"""Retained, ignored learner artifacts; source fixtures are never a run workspace."""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import uuid

REPOSITORY = Path(__file__).resolve().parents[3]


class RunDirectory:
    """Create a private, exclusive run beneath this checkout, independent of cwd."""
    def __init__(self, exercise: str, repository: Path = REPOSITORY) -> None:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', exercise):
            raise ValueError('exercise must be a simple lowercase name')
        base = repository.resolve(strict=True)
        for part in ('.cache', 'exercises', 'track-1', exercise):
            base = base / part
            if base.is_symlink():
                raise ValueError('exercise output directories must not be symlinks')
            base.mkdir(mode=0o700, exist_ok=True)
            if base.is_symlink() or not base.is_dir():
                raise ValueError('exercise output path must be a real directory')
        for _ in range(8):
            self.root = base / uuid.uuid4().hex
            try:
                self.root.mkdir(mode=0o700)
                break
            except FileExistsError:
                continue
        else:
            raise FileExistsError('could not allocate a unique exercise run')
        self.trace = self.root / 'trace.jsonl'
        self.result = self.root / 'result.json'

    def copy_fixtures(self, source: Path, docker: bool = False) -> Path:
        """Copy into a fresh work area; only Docker's mount needs other-UID access."""
        work = self.root / 'work'
        shutil.copytree(source, work)
        for item in [work, *work.rglob('*')]:
            item.chmod((0o777 if docker else 0o700) if item.is_dir() else (0o666 if docker else 0o600))
        return work

    def finish(self, summary: dict) -> dict:
        """Write a single summary exclusively; callers supply sanitized diagnostics."""
        summary = {**summary, 'directory': str(self.root), 'trace': str(self.trace),
                   'result': str(self.result)}
        descriptor = os.open(self.result, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump(summary, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        return summary


def accounting(result: dict) -> dict:
    """Keep unknown dispatch counts unknown in launcher summaries."""
    return {key: result.get(key) for key in
            ('tool_calls', 'completed_tool_calls', 'dispatch_attempts', 'dispatch_uncertain')}


class ObservedDispatch:
    """Observe actual dispatch entry/return for the short-stage launcher's summary."""
    def __init__(self, tools: object) -> None:
        self.tools = tools
        self.attempts = 0
        self.completed = 0
        self.uncertain = False

    @property
    def definitions(self) -> list:
        return self.tools.definitions

    def dispatch(self, call: dict) -> dict:
        self.attempts += 1
        self.uncertain = True
        result = self.tools.dispatch(call)
        self.completed += 1
        self.uncertain = False
        return result

    def counts(self) -> dict:
        return {'tool_calls': None if self.uncertain else self.completed,
                'completed_tool_calls': self.completed, 'dispatch_attempts': self.attempts,
                'dispatch_uncertain': self.uncertain}


def load_implementation(path: Path, name: str) -> object:
    """Load an explicit Python file; callers handle learner code failures."""
    path = path.resolve(strict=True)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f'expected a Python .py file: {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def record_failure(trace: object | None, error_type: str, message: str, counts: dict) -> bool:
    """Best-effort error/stop records; storage failure must not mask a run's status."""
    if trace is None or trace.handle.closed:
        return False
    try:
        trace.write('error', error_type=error_type, message=message)
        trace.write('stop', status='error', **accounting(counts))
    except (OSError, ValueError):
        return False
    return True
