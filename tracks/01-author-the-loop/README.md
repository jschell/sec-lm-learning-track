# Track 1: Understand and author the loop

Status: lessons and runnable reference implementation authored. Offline checks verified; see [validation](VALIDATION.md) for execution limits.

Build a small Python coding-agent harness and explain every transition. Allow **4–8 focused hours**, a project estimate rather than a schedule. No framework, local-model setup, or neural-network training is required.

The progression is inspired by [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). Explanations, Python implementation, fixtures, and exercises here are original project work, not a translated copy of his Go files. See [source provenance](SOURCES.md).

## Requirements and starting commands

Python **3.12+**, with **uv** as the default environment and command runner. The project pins 3.12 as its default interpreter in `.python-version`; `requires-python` permits newer versions. All commands below run from the repository root.

Install uv using the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/), then prepare the interpreter and environment:

```bash
uv python install 3.12
uv sync --frozen
```

Initial uv/Python setup may require network access. After setup, the dependency-free replay lessons run offline without an account or API key. The commands use `--frozen` to preserve the committed lockfile and `--offline` to prevent downloads. This follows [uv’s project workflow](https://docs.astral.sh/uv/guides/projects/).

```bash
uv run --frozen --offline python --version
uv run --frozen --offline python tracks/01-author-the-loop/lab/cli.py --scenario read
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
```

The CLI prints a new temporary directory containing work/ and trace.jsonl. Every invocation starts with clean synthetic fixtures and refuses to overwrite a trace. Inspect before deleting that directory. The source fixture is never modified.

## Lessons

| Lesson | Work | Suggested time |
| --- | --- | --- |
| [1. Minimal inference](01-minimal-inference.md) | Author one model request | 30–45 min |
| [2. One tool exchange](02-one-tool-exchange.md) | Dispatch a call and return its result | 45–60 min |
| [3. Author the loop](03-author-the-loop.md) | Implement repeated inference/tool feedback | 60–120 min |
| [4. Complete a task](04-complete-a-task.md) | Inspect, run, edit, and verify a repair | 60–120 min |
| [5. Control and inspect](05-control-and-inspect.md) | Diagnose failure and enforce limits | 45–90 min |

Each lesson can start from supplied working material; it does not depend on your previous edits. Authoring tasks have starter files; the reference solution remains available for comparison. Copy starter files to your own directory before editing if you want to preserve them.

## Execution modes

| Mode | What is real | What is simulated / required |
| --- | --- | --- |
| Synthetic replay | Loop, validation, file reads/search/edits, traces | Assistant responses and repair command observations are authored fixtures; no model inference or command execution |
| Docker integration | Actual grader execution, FAIL→edit→PASS, timeout and boundary checks | Assistant responses are still synthetic; Docker and an image are required |
| Live inference | Anthropic Messages API requests and model-selected calls | Requires your own key and model ID; commands remain disabled unless --execute is explicitly supplied |

These modes teach different things. Replay is not evidence a model can solve the task. Docker integration is not evidence a live model chose the right repair.

### Genuine contained execution

Install and start Docker separately, then preload the image (network access is needed for the pull, not for tool containers):

```bash
docker pull python:3.12-slim
uv run --frozen --offline python tracks/01-author-the-loop/lab/verify_docker.py
```

The script runs the broken program against a fixed read-only grader, applies the replayed edit through the real file tool, and runs the grader again. It also checks output limits, read-only grader access, absent API credentials, and child-process cleanup on timeout. It fails rather than using a host shell if Docker is unavailable.

### Live inference, optional

Set ANTHROPIC_API_KEY and ANTHROPIC_MODEL in your terminal using your usual secret handling. Do not put credentials in files or commit them. The key belongs to the controller and is not passed to containers.

```bash
uv run --frozen --offline python tracks/01-author-the-loop/lab/cli.py --live --model "$ANTHROPIC_MODEL"
uv run --frozen --offline python tracks/01-author-the-loop/lab/cli.py --live --model "$ANTHROPIC_MODEL" --execute
```

Live calls send the synthetic prompt, tool descriptions, and returned fixture content to Anthropic and may incur charges. The implementation makes at most 12 inference requests by default, each with max_tokens=1024, and has no automatic retries. This is **not a hard dollar budget**. Select an account-accessible model; no specific model is assumed. Truncated/unsupported stop reasons do not trigger tool execution.

## Files to inspect

- [loop.py](lab/loop.py): start at run_loop; then inspect Tools.dispatch, Workspace, Replay, AnthropicHTTP, and DockerExecutor as needed.
- [Starter stages](lab/starter/stages.py) and [worked stages](lab/solutions/stages.py).
- [Loop starter](lab/starter/loop.py); the worked loop is run_loop in loop.py.
- [Replay fixtures](lab/replay/read.json), [repair replay](lab/replay/repair.json), and [fixed grader](lab/grader/check.py).
- [Trace guide](trace-format.md), [source provenance](SOURCES.md), and [validation record](VALIDATION.md).

## Completion

Explain a complete run; identify model decisions and controller decisions; show an error returned to the model; demonstrate a limit stopping execution; deliberately change loop behavior. For an actual write-run-fix result, run the Docker integration check. A second learner should be able to repeat the documented steps without unwritten setup.

This is a synthetic learning lab, not a production security boundary or detection-quality benchmark. See Lesson 5 for limits. [Back to collection](../../README.md).
