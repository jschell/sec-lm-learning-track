# Reading a Track 1 trace

Original project JSONL format, version implicit in this initial implementation. Synthetic data only. One JSON object per line; sequence numbers are increasing, time is a Unix timestamp. A trace is created with exclusive access and mode 0600.

| Event | Fields to inspect | Meaning |
| --- | --- | --- |
| start | prompt, provider, endpoint, model, max_turns, max_calls, max_tokens | Controller configuration |
| request | turn, request.system/messages/tools/max_tokens | Complete inference input except transport credentials and live model field added by adapter |
| response | turn, response.content/stop_reason/usage | Assistant output; replay usage is zero |
| tool | call, result, elapsed_seconds | Requested operation and controller result |
| error | error_type, message; phase/learner_file when supplied | Terminal controller/provider/executor failure |
| stop | status, tool_calls | Why this run ended |

Run a scenario, copy its printed directory path, then inspect:

```bash
uv run --frozen --offline python learn.py trace /tmp/loop-lab-REPLACE/trace.jsonl
```

REPLACE is a placeholder: use the actual directory from the CLI. The inspector prints event order, tool names, IDs, error flags, short result/assistant-text excerpts, and stopping status without executing trace contents. For full messages, open the JSONL in a text editor. Tool result content is bounded text: it often contains serialized JSON, but a truncated prefix is not guaranteed valid JSON. Check truncation markers before parsing or drawing conclusions.

For the read scenario, find read-1 in response.content, tool.call.id, tool.result.tool_use_id, and the next request.messages. The assistant tool message precedes the user result message. This ordering follows [Anthropic's original client-tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

Do not store real credentials, customer evidence, or copied engagement prompts in these traces. Absence of an error event does not establish task correctness. Traces record observable messages and execution, not hidden model reasoning.

Live start events record the selected provider and fixed endpoint. API keys and authentication headers are never recorded. OpenRouter response usage/model details remain in the raw response event; the client does not normalize advanced provider extensions.

Stages 1 and 2 record one response per inference request, with matching turn numbers. Full request snapshots intentionally repeat history for these bounded teaching runs; trace size can grow quadratically as histories grow. Long-running production tracing is outside this format’s scope. On an escaped learner failure, tool_calls is null when the number of completed effects is unknown. Preserve the workspace and trace to investigate.
