# The loop on one page

> **Core route:** [1 Exchange](pilot-worksheet.md#1-follow-one-exchange) · [2 Errors](pilot-worksheet.md#2-follow-feedback-after-an-error) · **Loop recap (you are here)** · [4 Budget](pilot-worksheet.md#4-change-one-controller-setting) · [5 Transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool) · [Record](pilot-worksheet.md#explain-and-record-completion)

In the core route, read this after worksheet sections 1 and 2: it recaps the request, exchange and repeated feedback you have run, and previews the guards you test in section 4. Read it before the full reference code in lab/loop.py. This is an explanatory sketch of the mechanism, not a replacement executor. The runnable controller adds protocol validation, finite limits, trace events, and execution boundaries.

The inference/tool-feedback pattern comes from [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). The message and result names below follow [Anthropic's original client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

```python
messages = [{"role": "user", "content": task}]
calls_used = 0
for turn in range(turn_limit):
    response = infer(instructions, messages, tool_definitions)
    if response["stop_reason"] not in {"end_turn", "tool_use"}:
        break  # Never dispatch a truncated proposal.
    messages.append({"role": "assistant", "content": response["content"]})
    calls = [b for b in response["content"] if b["type"] == "tool_use"]
    if bool(calls) != (response["stop_reason"] == "tool_use"):
        raise ValueError("inconsistent stop reason")
    if not calls:
        break  # The turn ended; task correctness needs a separate check.
    if calls_used + len(calls) > call_limit:
        break  # Refuse the whole batch before execution.
    results = []
    for call in calls:
        result = validate_and_dispatch(call)
        calls_used += 1
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

## State observation and weight explanation

Messages and counters live in the harness. In worksheet section 1 you compared requests 1 and 2 to observe which file/history contents the controller supplies. Use this section for the second half of outcome 6: explain in your own words why that observation says nothing about weights, and record it in the worksheet's progress table.

**Outcome 6 question.** From your section 1 trace: what grew between request 1 and request 2, and where does it live? What would have to be different for the model itself to have learned something, and could any trace from this lab show it?

<details><summary>Check your answer</summary>

The message list grew: request 2 carries the assistant's call and the tool result. That list lives in the controller, which resends it with each request; if the controller dropped it, the next request would no longer contain it. Learning in the model would mean changed parameters, produced by a separate training step. This replay loads no weights, and a trace of requests and responses cannot show a parameter change.

</details>

Separately, ordinary tool feedback is appended to messages rather than applied as a weight update. Training explicitly updates model parameters, as illustrated by the optimizer step in [PyTorch's original optimization tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html). This replay loads no weights and cannot empirically measure their change. [The state companion](../../modules/messages-and-model-input/state.md#five-places-to-look) expands the architectural distinction. The provider performs generation inside each inference request; that token-generation loop is distinct from this application loop.

Sections 1 and 2 used the small functions in [solutions/stages.py](lab/solutions/stages.py). When you want the guarded version, read only run_loop in [lab/loop.py](lab/loop.py). Inspect helpers when a transition needs explanation. Request transport, Docker cleanup, and output draining are supporting machinery, not additional model capabilities.

**Core familiarity:** one request → one exchange → repeated feedback. The supplied controller retains terminal and budget guards; section 4 changes one of them. The budget lines in the sketch above preview what section 4 tests, so predict section 4 from the sketch only if you want to check your reading of it. **Optional extensions, outside the core:** study missing guards in [the recording-only comparison](08-learn-from-missing-guards.md), reproduce additional reference guards, inspect Docker internals, and compare providers. Existing guards stay enabled when using the reference lab even if you do not reimplement them.

Check yourself by pointing to a requested call, the operation that actually ran, its returned result, and the next request containing that result in one of your section 1 or 2 traces. Reference: [the trace guide](trace-format.md).

**Next in core:** [worksheet section 4: change one controller setting](pilot-worksheet.md#4-change-one-controller-setting).
