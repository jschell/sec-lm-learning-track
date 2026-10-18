# Context and state

Status: runnable offline inspection lessons; independent learner walkthrough pending. No model runs in this module.
Estimated effort: three 20–40-minute sessions, excluding setup; project estimate.
Prerequisites: Python lists/dictionaries. Complete starting files are supplied; no earlier learner edits required.

Understand what reaches the next inference, what remains on disk, and what selection or summarization removes. Start with the existing [state map](../messages-and-model-input/state.md), then use these three worked lessons:

| Lesson | Run and inspect | Deliberate variation |
| --- | --- | --- |
| [1. Locate state](01-locate-state.md) | A real file read enters the second captured request | Inspect a copy with the tool result omitted |
| [2. Select evidence](02-select-evidence.md) | Full packet versus literal keyword selection | Change only the query; locate lost coverage information |
| [3. Summarize and resume](03-summarize-and-resume.md) | Full packet versus two authored summaries | Compare faithful/lossy notes, then explicit note loading |

This collection's loop starts with [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). Context selection, compaction and external notes draw on [Anthropic's original context-engineering explanation](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Fixtures, scripts, comparisons and completion questions are original project work.

## Setup from the repository root

Install [uv](../../docs/python-development.md), then:

```bash
uv python install 3.12
uv sync --frozen
```

Interpreter/environment setup may use the network. The lessons then run offline with the standard library: no model download, server, API key or Docker. The state exercise imports the repository's complete worked exchange and file/trace primitives; inspect [the short exchange](../../tracks/01-author-the-loop/lab/solutions/stages.py) and [this module's script](lab/inspect_context.py). No upstream source is copied.

Run the three commands from the lesson pages. Output directories must be new. They contain only generated synthetic work and reports; use a new name to repeat. Source fixtures are never modified. `.cache/` is ignored by git.

## What the artifacts mean

`*-input.json` files are candidate request objects for inspection, not actual model requests. The state lesson's `requests.json` captures inputs passed to a scripted model object. Only its file read is real execution; its assistant responses are authored. No trace exposes weights, KV-cache reuse or private reasoning.

The evidence reports list IDs, literal anchors, characters and UTF-8 bytes. They do not count tokens, validate truth, or show that a model understood an input. A missing marker is useful evidence of omission; a present marker is not proof of a supported claim. Each lesson includes a human explanation check. See [worked observations](worked-observations.md) after making your prediction.

## Session notes and transfer check

Copy these prompts into your own notes; there is no automated understanding score:

- Prediction, command/output directory and what actually changed:
- Which artifact demonstrates the change? Quote one ID or message position:
- Which fact or limit disappeared, and what conclusion would be unwarranted?
- What stayed on disk, and which code explicitly supplied it to the next input?
- Transfer: select with `--query 'collection gap'`. Explain why preserving the gap alone is also insufficient for answering the original task.

The expected transfer observation is C01 alone; both sign-in source outcomes are missing. Explain the difference between retaining a relevant warning and retaining enough evidence for the task. A learner should identify the contradiction and gap from the original packet without treating the application outcome as ground truth.

[Source record](SOURCES.md) · [Validation](VALIDATION.md) · [Collection](../../README.md)
