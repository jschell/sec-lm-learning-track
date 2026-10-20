# Reading a Track 1 trace

Original project JSONL format, version implicit in this initial implementation. Synthetic data only. One JSON object per line; sequence numbers are increasing, time is a Unix timestamp. A trace is created with exclusive access and mode 0600.

| Event | Fields to inspect | Meaning |
| --- | --- | --- |
| start | prompt, provider, endpoint, model, max_turns, max_calls, max_tokens | Controller configuration |
| request | turn, request.system/messages/tools/max_tokens | Complete inference input except transport credentials and live model field added by adapter |
| response | turn, response.content/stop_reason/usage | Assistant output; replay usage is zero |
| tool | call, result, elapsed_seconds | Requested operation and controller result |
| proposal | proposal.call, label, origin | Authored requested action; not execution |
| decision | call, decision, reason | Permission choice; allowance alone does not establish execution |
| recording_only_decision | label, decision, executed, scope | Simulation label; this exercise invokes no operation on that path |
| effect | operation, path, characters_returned | Completed real read in the authority exercise; separate from setup/reporting |
| error | error_type, message; phase/learner_file when supplied | Terminal controller/provider/executor failure |
| stop | status, tool_calls, completed_tool_calls, dispatch_attempts, dispatch_uncertain | Why the run ended and what dispatch accounting is known |

Run a scenario, copy its printed directory path, then inspect:

```bash
uv run --frozen --offline python learn.py trace TRACE_PATH
```

TRACE_PATH is a placeholder: use the actual trace path from the CLI on your OS. The inspector prints event order, tool names, IDs, error flags, short result/assistant-text excerpts, permission/simulation/effect details when present, and stopping status without executing trace contents. Unknown event names remain visible. Excerpts are display prefixes, not complete JSON payloads. For full messages, open the JSONL in a text editor. Tool result content is bounded text: it often contains serialized JSON, but a truncated prefix is not guaranteed valid JSON. Check truncation markers before parsing or drawing conclusions.

For the read scenario, find read-1 in response.content, tool.call.id, tool.result.tool_use_id, and the next request.messages. The assistant tool message precedes the user result message. This ordering follows [Anthropic's original client-tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

Do not store real credentials, customer evidence, or copied engagement prompts in these traces. Absence of an error event does not establish task correctness. Traces record observable messages and execution, not hidden model reasoning.

Live start events record the selected provider and fixed endpoint. API keys and authentication headers are never recorded. OpenRouter response usage/model details remain in the raw response event; the client does not normalize advanced provider extensions.

Stages 1 and 2 record one response per inference request, with matching turn numbers. Full request snapshots intentionally repeat history for these bounded teaching runs; trace size can grow quadratically as histories grow. Long-running production tracing is outside this format’s scope. On an escaped learner failure, tool_calls is null when the number of completed effects is unknown. Preserve the workspace and trace to investigate.

## Exchange summaries

Response `proposed_call` entries show tool name, ID and bounded arguments. Request `input_snapshot` and history `history_snapshot` entries show calls and results with their message positions. Snapshots are cumulative: old feedback may reappear, so their entries are not new dispatch events. Each snapshot shows at most its last eight tool blocks and reports omissions; responses show at most eight proposals. Each payload excerpt is bounded separately.

Stage 2 has no standalone tool event. Follow proposed read-1 → matching result in request 2 → final response, then inspect tools.dispatch in the worked exchange and compare the returned fixture bytes. History presence alone does not prove execution. For complete input inspect the raw second request, and [preserve the workspace](pilot-worksheet.md#preserve-your-evidence) before temporary cleanup.

## Failure accounting and credential diagnostics

For the guarded and short repeated loops, tool_calls counts dispatches that returned (including error results). It is not a count of independently verified side effects. completed_tool_calls retains that known count; dispatch_attempts includes a dispatch that raised. If dispatch raises, dispatch_uncertain is true and tool_calls is null because an effect may already have happened. A returned dispatch is counted before its tool event is written, so a later trace-write failure does not erase the known count. Missing tool events therefore do not establish that nothing ran.

These fields describe observations within this process, not transactions or automatic rollback. On an escaped learner/launcher failure, counts may be unknown. If trace storage itself fails, a complete error/stop record may be unavailable; inspect the workspace and console failure before retrying. Do not infer success from a partial trace.

Configured Anthropic/OpenRouter credentials, their escaped forms and cached transport keys are removed from terminal diagnostics. Unexpected transport failures use a fixed category with no raw exception cause/context; HTTP errors retain bounded redacted fields. Credential values are trimmed at their edges and internal whitespace/control/non-ASCII characters are rejected before header construction. This protects the configured authentication diagnostics; it is not a general secret scanner for arbitrary fixture/model content. Keep credentials out of exercise data.
