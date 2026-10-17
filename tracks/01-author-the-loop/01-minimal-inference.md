# 1. Minimal inference

Status: authored; offline reference checked. Estimated effort: 30–45 minutes.
Prerequisites: Python functions, dictionaries, and lists. Start from the [track requirements](README.md).

## Goal

Build one request and identify what is supplied by the controller versus returned by the model.

## Explanation

Before an agent loop exists, there is an inference request. The controller supplies instructions, messages, output limits, and optionally tool definitions. The response contains generated content and a reason generation stopped. Nothing executes simply because the response mentions a command.

[Huntley's workshop](https://ghuntley.com/agent/) starts with a chat program before introducing tools. This lesson uses the same conceptual starting point with original Python examples. Our request shape follows [Anthropic's Messages API](https://platform.claude.com/docs/en/api/messages/create), not a universal schema all providers share.

In this lab, model.complete(request) is a tiny interface implemented by either Replay or MessagesHTTP. Replay returns an authored response; MessagesHTTP makes a REST request to the selected provider. Both live providers accept the Anthropic message format used here. See the [OpenRouter original endpoint documentation](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message). There is no SDK agent runner hiding a loop.

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
uv run --frozen --offline python tracks/01-author-the-loop/lab/check_authoring.py --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 1
uv run --frozen --offline python learn.py --scenario inference
```

The first command prints PASS lesson 1. The second prints status completed, tool_calls 0, and the directory containing the trace. Use the [trace guide](trace-format.md) to inspect the request and response.

## Authoring exercise

Implement infer_once in [starter/stages.py](lab/starter/stages.py). It receives a model and prompt; build one request and return one response. Then:

```bash
uv run --frozen --offline python tracks/01-author-the-loop/lab/check_authoring.py --file tracks/01-author-the-loop/lab/starter/stages.py --stage 1
```

The untouched starter raises NotImplementedError. That is expected until you write it. Compare with the worked stages only after trying.

## Observe and vary

Change the prompt in your implementation and inspect the request. The replay response stays the same: it is a fixture, not a model reacting to your words. Live inference is an optional separate path in the track README.

For a real conversation, preserve the assistant response and add a new user message before the next request. Removing history means the next request no longer contains that prior context. A stateless request API does not infer your local Python history.

## Completion check

Show the supplied messages, generated content, and stop reason. Explain why no tool ran and why a plausible answer is not proof of task success.

## Troubleshooting and boundaries

ModuleNotFoundError for loop usually means you invoked a snippet outside the lab directory; use the scripts above. No API key is needed for either command. A synthetic replay cannot measure model quality. Only synthetic data belongs in the lab trace.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| Chat before tools | [Huntley workshop](https://ghuntley.com/agent/) and pinned chat.go in [source record](SOURCES.md) | Original Python exercise; no upstream code copied |
| Request and response structure | [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages/create) | REST shape; checked 2026-10-16, live call not performed |

[Next: one tool exchange](02-one-tool-exchange.md).
