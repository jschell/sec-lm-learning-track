# 1. Minimal inference

> **Core route:** **1 Exchange (supports this)** · [2 Errors](pilot-worksheet.md#2-follow-feedback-after-an-error) · [Loop recap](core-loop.md) · [4 Budget](pilot-worksheet.md#4-change-one-controller-setting) · [5 Transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool) · [Record](pilot-worksheet.md#explain-and-record-completion)

Status: authored; offline reference checked. Estimated effort: 30–45 minutes.
Full-page estimate includes reconstruction; provider setup/live observation is extra. Estimates are provisional project judgments, not learner timings.
Prerequisites: Python functions, dictionaries, and lists. Start from the [track requirements](README.md).

## Goal

Build one request and identify what is supplied by the controller versus returned by the model.

> **What this demonstrates:** One supplied request and its response. Replay makes no inference call; a final answer is not a task-success check.

## Explanation

Before an agent loop exists, there is an inference request. The controller supplies instructions, messages, output limits, and optionally tool definitions. The response contains generated content and a reason generation stopped. Nothing executes simply because the response mentions a command.

[Huntley's workshop](https://ghuntley.com/agent/) starts with a chat program before introducing tools. This lesson uses the same conceptual starting point with original Python examples. Our request shape follows [Anthropic's Messages API](https://platform.claude.com/docs/en/api/messages/create), not a universal schema all providers share.

In this lab, model.complete(request) is a tiny interface implemented by either Replay or MessagesHTTP. Replay returns an authored response; MessagesHTTP makes a REST request to the selected provider. Both live providers accept the Anthropic message format used here. See the [OpenRouter original endpoint documentation](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message). There is no SDK agent runner hiding a loop. The Stage 1/2 launchers are replay-only; for optional live inference use the controlled [hosted guide](live-observation.md). Live Stage 3 uses the guarded reference rather than the short teaching loop.

## Worked example

```python
request = {
    "system": "Explain the synthetic exercise.",
    "messages": [{"role": "user", "content": "What happens next?"}],
    "tools": [],
    "max_tokens": 1024,
}
response = model.complete(request)
```

A synthetic response has content=[{"type":"text","text":"..."}] and stop_reason="end_turn". The controller has learned only that the turn ended; it has not checked the answer. Replay usage counts are zero because no inference occurred.

Run the worked implementation:

```bash
uv run --frozen --offline python learn.py stage 1
```

This runs the complete single-request function in [solutions/stages.py](lab/solutions/stages.py) and prints a summary; add `--json` to print the full response. Inspect that function and the run's trace with the printed `learn.py trace` command. Requests and responses are recorded; replay responses are synthetic, while file reads are real. No tool is exposed in this stage.

## Optional reconstruction

Implement infer_once in [starter/stages.py](lab/starter/stages.py). It receives a model and prompt; build one request and return one response. Then:

```bash
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/starter/stages.py --stage 1
```

The untouched starter raises NotImplementedError. That is expected until you write it. Use the worked stages as a reference whenever needed. The check requires a real call to the supplied synthetic model and the actual returned response; plausible fabricated text fails.

## Observe and vary

Change the prompt in your implementation and inspect the request. The replay response stays the same: it is a fixture, not a model reacting to your words. Live inference is an optional separate path in the track README.

For a real conversation, preserve the assistant response and add a new user message before the next request. Removing history means the next request no longer contains that prior context. A stateless request API does not infer your local Python history.

## Completion check

Show the supplied messages, generated content, and stop reason. Explain why no tool ran and why a plausible answer is not proof of task success.

## Troubleshooting and boundaries

ModuleNotFoundError for loop usually means you invoked a snippet outside the lab directory; use the scripts above. No API key is needed for either command. Keep inputs synthetic.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| Chat before tools | [Huntley workshop](https://ghuntley.com/agent/) and pinned chat.go in [source record](SOURCES.md) | Original Python exercise; no upstream code copied |
| Request and response structure | [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages/create) | REST shape; checked 2026-10-16, live call not performed |

**Next in core:** [return to worksheet section 1](pilot-worksheet.md#1-follow-one-exchange). Supporting explanation for its Stage 2 exchange: [Lesson 2](02-one-tool-exchange.md).
