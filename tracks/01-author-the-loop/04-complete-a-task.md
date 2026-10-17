# 4. Complete a task

Status: authored; replay checked. Genuine Docker execution requires the integration check in [validation](VALIDATION.md). Estimated effort: 60–120 minutes.
Prerequisites: understand the loop; supplied working solution can be used directly. Docker is required only for actual program execution.

## Goal

Trace a read/search/run/edit/run task and distinguish a proposed repair from an independently checked result.

> **What this demonstrates:** A real file edit with scripted command observations by default. Only the explicit Docker path demonstrates actual program execution.

## Explanation

[Huntley's workshop](https://ghuntley.com/agent/) develops a coding agent with read, list, bash, edit, and search operations. Here the equivalents are read_file, list_files, run_command, edit_file, and code_search. Our command tool uses /bin/sh inside Docker rather than host bash. Our bounded literal search uses Python instead of ripgrep to avoid an extra dependency. These are explicit project design choices.

The supplied fizzbuzz function tests divisibility by three before divisibility by fifteen. Fifteen therefore becomes Fizz, never reaching the FizzBuzz branch. This deliberate defect requires changing branch order rather than merely creating a plausible-looking file.

## Worked replay

```bash
uv run --frozen --offline python learn.py --scenario repair
```

Expected: completed, six tool calls, and a fresh output directory. The sequence is:

| Turn | Calls | Observation |
| --- | --- | --- |
| 1 | list_files, code_search | Locate program and relevant line |
| 2 | read_file | Inspect the branch ordering |
| 3 | run_command | Scripted FAIL observation |
| 4 | edit_file | Actually replace the unique block in the disposable file |
| 5 | run_command | Scripted PASS observation |
| 6 | None | Synthetic final answer; end_turn |

The repair edit is real; the commands are not. Inspect [replay/repair.json](lab/replay/repair.json) and [ScriptedExecutor](lab/scenarios.py) to see exactly where observations come from. Compare the resulting file with [solutions/fizzbuzz.py](lab/solutions/fizzbuzz.py). Never describe replay as an autonomous live-model success.

## Genuine execution exercise

Docker is an explicit boundary before running generated code. Its options are documented in the original [Docker run reference](https://docs.docker.com/engine/containers/run/). DockerExecutor supplies arguments as a list without a host shell; only the contained /bin/sh receives the model's command.

```bash
docker pull python:3.12-slim
uv run --frozen --offline python tracks/01-author-the-loop/lab/verify_docker.py
```

The integration check executes the broken program against /grader/check.py, replays the same tool choices using an actual Docker executor, then executes the grader again. Expected: FAIL before, PASS afterward. The grader is outside /work and mounted read-only, so editing workspace tests cannot change its expected values.

This still uses synthetic assistant responses. For actual model-selected repair, follow the live-inference commands in the [track README](README.md). The trace must show actual run_command results with no SCRIPTED OBSERVATION marker. A live model may fail or choose another valid repair; report what happened.

## Authoring and variation

Use your Lesson 3 loop with the supplied repair replay:

```bash
uv run --frozen --offline python learn.py --scenario repair --loop-file tracks/01-author-the-loop/lab/starter/loop.py
```

Then inspect Tools.dispatch and Workspace.edit. Change an old_str in your own replay copy so it no longer matches. Verify that the edit fails and leaves the file unchanged. Do not automatically treat an edit failure as permission to replace an entire existing file.

When no Docker runtime is available, complete the replay and source inspection, and explicitly leave the genuine execution check unverified. There is no host execution alternative.

## Completion check

Explain why the old ordering fails, show the actual edit, identify where command evidence came from, and explain why the fixed grader is independent of the agent's writable files. Claim actual write-run-fix only after running the Docker test.

## Troubleshooting and boundaries

“Docker required” means the command path is disabled, not that you should remove containment. Pull the image before running; --pull=never prevents tool runs from downloading images implicitly. A permissions error usually means the Docker daemon cannot access the bind-mounted directory or UID 65534 cannot write /work; the scripts prepare only their own temporary workspace for that UID.

The floating image tag is recorded as a reproducibility limit. Pin a digest for repeated operational comparisons. The fixed grader is readable, and executing candidate Python can attempt deception; this small check is not proof against adversarial code.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| Coding primitives and FizzBuzz teaching example | [Huntley workshop](https://ghuntley.com/agent/), pinned stages in [source record](SOURCES.md) | Bug, grader, Python implementation, and fixtures are original project material |
| Container options and isolation components | [Docker run reference](https://docs.docker.com/engine/containers/run/) and [Engine security](https://docs.docker.com/engine/security/) | Configuration checked against docs; local runtime limits in validation record |

[Next: control and inspect](05-control-and-inspect.md).
