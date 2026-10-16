# Track 1 validation record

Date: 2026-10-16. This records observed checks, not a promise of model success.

## Local verification

Environment: Linux, CPython 3.12.14, uv dependency-free lockfile. No Docker CLI/daemon is available; bubblewrap also cannot establish the requested namespace boundary in this environment, so it is not used as a fallback.

| Check | Result |
| --- | --- |
| Standard-library functional suite | 16 tests passed |
| Worked lesson 1 and lesson 2 protocol checks | Passed |
| Synthetic repair replay | Completed; six tool calls; actual edited file equals reference repair |
| Synthetic recovery replay | Completed; missing file, invalid type, unknown tool returned as errors |
| Multiple calls, turn/call limits, truncated response | Verified by tests and CLI walkthrough |
| REST adapter request serialization | Mocked HTTP test passed; no network inference |
| Docker configuration | Argument inspection test passed; not execution evidence |
| Actual Docker FAIL→edit→PASS and controls | Passed in hosted CI; not run locally |
| Live hosted-model run | Not performed; no credentials used |
| Independent human learner walkthrough | Not performed |

## CI

[Hosted CI run 38979681402](https://github.com/jschell/sec-lm-learning-track/actions/runs/38979681402) passed all three jobs for implementation commit b333ec7cdbec176982f58e672d667fc0ddd7da07: offline Python 3.11, offline Python 3.12, and actual Docker integration on Ubuntu. The Docker job verified actual grader failure before the edit and success afterward, read-only grader access, absent API key, output truncation, timeout, and child/container cleanup.

Subsequent documentation-only changes update this record and remove incidental blank-line changes. Check the PR for the latest run. These results do not establish live-model success or replace a human learner walkthrough.

## Repeat the checks

```bash
python3 -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
python3 tracks/01-author-the-loop/lab/check_authoring.py --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 1
python3 tracks/01-author-the-loop/lab/check_authoring.py --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 2
docker pull python:3.12-slim
python3 tracks/01-author-the-loop/lab/verify_docker.py
```

See [SOURCES.md](SOURCES.md) for original protocol/runtime sources. This validation record and its tests are original project artifacts. Docker's floating image tag, optional live model selection, and changing provider behavior limit exact reproduction; replay fixture hashes pin the offline starting material.
