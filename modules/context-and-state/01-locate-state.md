# 1. Locate state

Goal: identify the exact transition that moves external file contents into the next input. This lesson uses authored responses and a real read-only file operation.

A file existing on disk does not itself place its bytes in a request. The controller dispatches a tool and appends its result before the next inference. This is the feedback transition in [Huntley's workshop](https://ghuntley.com/agent/). For the Anthropic-style message structure used here, a `tool_result` refers to the preceding `tool_use` by ID; see the [original client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

## Predict, then run

Before running, write which request will first contain `Synthetic status: pending review.` and whether ending the process will delete that file.

From the repository root after [setup](README.md#setup-from-the-repository-root):

```bash
uv run --frozen --offline python modules/context-and-state/lab/inspect_context.py state --output .cache/context-state-1
```

Open `.cache/context-state-1/requests.json` in an editor. The first request contains a task and read-file definition. The second contains the assistant's read request and the actual result, with matching IDs. File contents in `tool_result.content` are JSON-encoded by the existing file tool, so the string contains escaping. The final response is scripted and makes no claim about comprehension.

The executable transition is the complete existing `exchange` function:

```python
first = model.complete(first_request)
messages.append({'role': 'assistant', 'content': first['content']})
results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
messages.append({'role': 'user', 'content': results})
```

The next call supplies `messages`. See [the full runnable function](../../tracks/01-author-the-loop/lab/solutions/stages.py), including request construction. The wrapper snapshots requests at call time because the function subsequently mutates the same list.

## Vary and inspect the failure

Open `counterfactual-omitted-result.json`. It is a separate copy of request 2 with only the result message removed. The original capture remains intact. This copy has an unanswered tool call and is **inspection-only**, not a valid follow-up sent to a provider. Locate the missing bytes and explain why this is a controller input defect rather than proof that a model forgot the fact.

After the command exits, open `work/status.txt` and `trace.jsonl` inside the output directory. They remain on disk. The in-process list no longer exists in that process; a later process must explicitly read saved data to reuse it. Re-running with a different output name starts fresh supplied state.

## Explain and check

1. Which message first contains the actual returned text? Match the result ID to the call ID.
2. Which line moves file data into history? Which line later supplies that history?
3. Why does the omitted-result copy fail to preserve a complete exchange?
4. What evidence would be necessary to claim weight changes or KV-cache reuse?

Expected: request 2's final user message carries the result; dispatch reads and append adds it. Saved artifacts persist independently of the process. No model/runtime is loaded, so there is no evidence here of weight or cache behavior. The [state map](../messages-and-model-input/state.md) separates these mechanisms, with original sources.

[Next: selection](02-select-evidence.md) · [Sources and limits](SOURCES.md)
