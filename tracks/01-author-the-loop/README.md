# Track 1: Understand the agent loop

Read an agent trace and explain what the model proposed, what the controller actually did, and what evidence reached the next inference. For a security professional, this helps locate execution authority, missing feedback and unsupported claims of success when reviewing an agent system.

The starting mechanism comes from [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). Our Python implementation, fixtures and exercises are original project work; [source details](SOURCES.md).

## By the end you can

1. Locate the model response and distinguish a proposed tool call from actual dispatch.
2. Match a call/result ID and locate that feedback in subsequent inference input.
3. Explain repeated feedback after a tool error, separating scripted recovery from model observation.
4. Change a controller budget and explain which operations ran and why the loop stopped.
5. Check the task outcome separately from conversation completion.
6. Distinguish files, conversation history and supplied input, and explain why ordinary tool feedback does not update model weights.

Demonstrate these with a saved trace, a prediction/variation and your explanation. Record progress and assistance in the [worksheet](pilot-worksheet.md#progress-and-evidence). A successful command alone does not establish understanding.

## What you need

Basic Python functions, lists/dictionaries and terminal use; Git, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python **3.12+** (default 3.12, installed below). The core needs no model, API key or Docker.

Planning estimate: **2–4 focused hours for the numbered core route below**, excluding first-time setup, companion lessons and further exercises. This is provisional, not measured learner time. Individual lesson-page estimates cover their fuller exercises, including reconstruction or execution where stated; they are not additive requirements for this route. Record actual setup and learning time separately.

Author checks used Linux x86_64 with bash and Python 3.12; CI also checks Python 3.13. Native Windows, macOS and physical Pi operation have not been validated. Windows users can use a Linux terminal in WSL for these commands, but WSL has not been independently checked here. Use the actual paths printed on your machine; temporary directories need not be under /tmp. [Observed environments and limitations](VALIDATION.md).

## Prepare once

In a terminal, get the repository and enter it:

```bash
git clone https://github.com/jschell/sec-lm-learning-track.git
cd sec-lm-learning-track
uv python install 3.12
uv sync --frozen
```

If you already have a checkout, enter its root and run the last two commands. Initial preparation may need network access. The following core commands run offline with the supplied replay and bounded real file operations, using [uv's frozen project workflow](https://docs.astral.sh/uv/guides/projects/).

<a id="start-and-inspect"></a>
<a id="learning-path"></a>

## One core route

1. Read [the loop on one page](core-loop.md).
2. Follow [worksheet section 1: one exchange](pilot-worksheet.md#1-follow-one-exchange): run stages 1 and 2 and inspect the Stage 2 trace. [Lessons 1](01-minimal-inference.md) and [2](02-one-tool-exchange.md) explain these steps.
3. Follow [section 2: error feedback](pilot-worksheet.md#2-follow-feedback-after-an-error): inspect repeated requests and returned errors. [Lesson 3](03-author-the-loop.md) explains the loop.
4. Follow [section 4: budget variation](pilot-worksheet.md#4-change-one-controller-setting): predict and compare two settings. [Lesson 5](05-control-and-inspect.md) explains stopping behavior.
5. Follow [section 5: supplied read-only transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool): locate registration, dispatch and feedback. [The transfer lesson](06-transfer-tool.md) supplies details.
6. Preserve your evidence and [record completion](pilot-worksheet.md#explain-and-record-completion) against the six outcomes above.

Worksheet section numbers identify activities; lesson numbers identify supporting explanations. Sections 3 and 6 are further exercises, so the core intentionally skips them. Complete worked functions are supplied: run, predict, inspect, vary and explain before considering reconstruction.

Use `uv run --frozen --offline python learn.py --help` to discover commands. For a structured assessed pilot, a facilitator follows [the protocol](../../docs/pilot/README.md) using this same core plus the separately named **Select evidence** companion. Evidence selection is not an additional Track 1 completion requirement.

<a id="completion-and-modes"></a>

## Going further

Choose an activity after the core; these do not form a second required sequence.

| Activity | Starting point | Additional scope |
| --- | --- | --- |
| Reconstruct the loop or tool | Starters in [Lesson 3](03-author-the-loop.md) and [transfer](06-transfer-tool.md) | Author code, then compare worked behavior |
| Inspect repair or run a program | [Worksheet section 3](pilot-worksheet.md#3-separate-a-file-edit-from-program-execution), [Lesson 4](04-complete-a-task.md) | Replay edits real files; genuine command execution requires the Docker extension |
| Follow untrusted input | [Worksheet section 6](pilot-worksheet.md#6-locate-untrusted-instructions), [Lesson 7](07-untrusted-content.md) | Locate injected text in supplied input; no model-resistance claim |
| Learn missing guards | [Lesson 8](08-learn-from-missing-guards.md) | Recording-only comparison; guard authoring/checks remain separate from core completion |
| Observe a local model | [360M/example recipe](../../modules/tool-requests-and-feedback/README.md#run-the-observed-working-configuration) | Blank-slate CPU setup, downloads and teaching text adapter; successes and failures retained |
| Observe a hosted model | [Hosted guide](live-observation.md) | Provider credentials and actual inference; task accuracy checked separately |

## Reference

[Worksheet](pilot-worksheet.md) · [Implementation](lab/loop.py) · [Trace format](trace-format.md) · [Validation and test commands](VALIDATION.md) · [Sources](SOURCES.md)

The core establishes controller familiarity. Replay responses are authored, file operations are real, and command observations are scripted. It does not establish model competence or production security. [Back to collection](../../README.md).
