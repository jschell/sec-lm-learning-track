# Track 1 validation

Updated 2026-10-16. This is the authoritative current check summary. Implementation tests, actual model observations, and independent learner usability are separate claims.

## Current status

Target Python 3.12+, default 3.12; uv 0.12.23. Local environment: Linux, CPython 3.12.14. No live provider credentials were used. Docker is unavailable locally.

| Check | Observed result |
| --- | --- |
| Standard-library functional suite through frozen/offline uv | **30 tests passed locally** |
| Worked request/exchange/loop behavioral checks | Passed for the short worked stages; loop contract also passed for the guarded reference |
| Wrong learner submissions | Fabricated response, skipped second inference, and fabricated feedback rejected |
| Three stage launchers and transfer | Passed offline; transfer reads actual fixture contents; path and line-count edge cases checked |
| Replay scenarios and repair artifact | Passed; scripted observations distinguished from actual file edits |
| Short learn.py entry and trace inspection | Passed |
| Read-only mode and omitted tools | Dispatch blocks edits/commands and removed tools; alternatives remain available |
| Read-only live task wiring | Passed with synthetic provider response; not live behavior |
| Anthropic/OpenRouter exchanges and credentials | Mocked HTTP checks passed, including no cross-provider fallback or secrets in traces |
| Actual Docker FAIL→edit→PASS and execution controls | Passed in hosted CI for the previously verified implementation; no local Docker run |
| Actual hosted-model observation | **Not performed** |
| Independent fresh-learner pilot | **Not performed**; [prepared checklist](pilot-checklist.md) |

## Hosted checks

[Verified run 38990959595](https://github.com/jschell/sec-lm-learning-track/actions/runs/38990959595) passed Python 3.12, Python 3.13, and actual Docker integration for commit 6a2499ec1d192795908cf25b351cbe017c9442ba, before the new usability/read-only exercises. Docker checks covered genuine FAIL→edit→PASS, a read-only grader, absent API credentials, bounded output, and timeout/child cleanup.

The current workflow runs the expanded suite on 3.12/3.13 plus the Docker integration check. See [current usability branch checks](https://github.com/jschell/sec-lm-learning-track/actions?query=branch%3Adocs%2Fmechanics-usability) for the latest revision. A workflow file alone is not passing evidence. No CI run substitutes for model observation or a learner pilot.

## Repeat implementation checks

From the repository root after [setup](README.md):

```bash
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 1
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 2
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 3
uv run --frozen --offline python learn.py transfer
docker pull python:3.12-slim
uv run --frozen --offline python tracks/01-author-the-loop/lab/verify_docker.py
```

Fixture provenance/hashes and original protocol/runtime sources are in [SOURCES.md](SOURCES.md). Docker's floating image tag and unselected live model limit exact reproduction. Tests and the observation checklist are original project work; they make no general model-quality or production-safety claim.
