# The loop on one page

Start here before reading the supporting code. This is an explanatory sketch of the mechanism, not a replacement executor. The runnable controller adds protocol validation, finite limits, trace events, and execution boundaries.

The inference/tool-feedback pattern comes from [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). The message and result names below follow [Anthropic's original client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

```python
messages = [{"role": "user", "content": task}]
for turn in range(turn_limit):
    response = infer(instructions, messages, tool_definitions)
    # First validate content/stop reason; never execute a partial proposal.
    messages.append({"role": "assistant", "content": response["content"]})
    calls = [b for b in response["content"] if b["type"] == "tool_use"]
    if not calls:
        break  # The turn ended; task correctness needs a separate check.
    results = []
    for call in calls:
        result = validate_and_dispatch(call)
        results.append({"type": "tool_result", "tool_use_id": call["id"],
                        "content": result})
    messages.append({"role": "user", "content": results})
```

| Transition | Owner | Runnable implementation |
| --- | --- | --- |
| Assemble instructions, messages, and tools | Controller | request construction in run_loop |
| Generate text or requested calls | Model (or synthetic replay) | model.complete |
| Validate stop reason, IDs, arguments, and limits | Controller | run_loop and Tools.dispatch |
| Read, edit, or execute an allowed operation | Tool implementation | Workspace / DockerExecutor |
| Associate result with call and append history | Controller | result.tool_use_id and messages.append |
| Request another inference or stop | Controller, informed by response | next iteration or explicit status |

**State:** messages and counters live in the harness. Model weights are not updated by appending a tool result. The provider performs generation inside each inference request; that token-generation loop is distinct from this application loop.

Read only run_loop in [lab/loop.py](lab/loop.py) first. Inspect helpers when a transition needs explanation. Request transport, Docker cleanup, and output draining are supporting machinery, not additional model capabilities.

**Core familiarity:** one request → one exchange → repeated feedback. **Extensions:** reproduce every reference guard, inspect Docker internals, and compare providers. Existing guards stay enabled when using the reference lab even if you do not reimplement them.

Finish by pointing to a requested call, the operation that actually ran, its returned result, and the next request containing that result. See [the trace guide](trace-format.md).
