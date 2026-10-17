# Track 1: Understand and author the loop

Build and explain a small Python coding-agent harness. Allow **4–8 focused hours**, a project estimate. Lessons and runnable examples are authored; see the single [validation record](VALIDATION.md) for tested paths and outstanding checks.

Inspired by [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). Our Python code, fixtures, and explanations are original project work; [source details](SOURCES.md). No framework or neural-network training is required.

## Prepare once

Python **3.12+**, default 3.12, using uv. From the repository root:

```bash
uv python install 3.12
uv sync --frozen
```

Install uv using its [official instructions](https://docs.astral.sh/uv/getting-started/installation/). Initial setup may need network access; dependency-free replay runs offline afterward. Frozen commands preserve the lockfile, following [uv's project workflow](https://docs.astral.sh/uv/guides/projects/).

## Start and inspect

```bash
uv run --frozen --offline python learn.py
```

This runs the read replay and prints a fresh temporary directory containing work/ and trace.jsonl. No model call or shell command runs. Copy the printed trace path into:

```bash
uv run --frozen --offline python learn.py trace /tmp/loop-lab-REPLACE/trace.jsonl
```

REPLACE is a placeholder for that run's directory. Every invocation starts clean; source fixtures are unchanged. Inspect before deleting its temporary directory.

## Learning path

Read [the loop on one page](core-loop.md) first. Then:

| Lesson | Core exercise | Reference extensions |
| --- | --- | --- |
| [1. Minimal inference](01-minimal-inference.md) | Author one request | Compare replay with live transport |
| [2. One tool exchange](02-one-tool-exchange.md) | Dispatch and return a matching result | Inspect schema enforcement |
| [3. Author the loop](03-author-the-loop.md) | Repeat inference with updated history | Reproduce additional reference guards |
| [4. Complete a task](04-complete-a-task.md) | Inspect the deliberate repair | Execute the grader in Docker |
| [5. Control and inspect](05-control-and-inspect.md) | Observe an error and finite stop | Inspect execution-boundary internals |

Each lesson has an independent starting point and worked solution. You do not have to rebuild all transport, logging, and container machinery to understand the loop; retain those controls when using the supplied runnable lab.

## Completion and modes

| Level / mode | What it demonstrates |
| --- | --- |
| **Controller familiarity** | Author a request/exchange/loop, explain a trace, demonstrate an error and stop limit, change behavior deliberately. Replay responses are synthetic; file operations are real; command observations are scripted. |
| **Observed model behavior** | Complete the [read-only live experiments](live-observation.md): read a file, omit a tool, and encounter a missing file. No Docker needed; provider credentials required. |
| Docker integration extension | Actual program FAIL→edit→PASS, grader protection, bounded output, and timeout checks. Assistant choices remain scripted. Commands and requirements are in [Lesson 4](04-complete-a-task.md). |
| Live repair extension | Actual model-selected writes and Docker execution. Instructions are in [the live guide](live-observation.md). |

Controller completion does not establish model competence; a finished model turn does not establish task correctness. A separate [pilot checklist](pilot-checklist.md) tests whether another learner can follow the material without unwritten help.

## Reference

[Core loop](core-loop.md) · [Implementation](lab/loop.py) · [Trace format](trace-format.md) · [Live setup](live-observation.md) · [Validation and test commands](VALIDATION.md) · [Sources](SOURCES.md)

This synthetic learning lab does not establish production security or detection quality. [Back to collection](../../README.md).
