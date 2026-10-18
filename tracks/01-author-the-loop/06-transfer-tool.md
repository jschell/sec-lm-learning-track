# Transfer: add a read-only tool

Status: authored; offline implementation checks only. Estimated effort: 20–40 minutes.
Prerequisites: explain the request → dispatch → feedback loop in Lesson 3. All starting files are supplied.

This original exercise extends [Huntley's progression from chat to callable tools](https://ghuntley.com/agent/). It tests whether you can connect another operation to the same loop. It does not introduce an evaluation platform or establish model competence.

## Goal

Locate registration, argument checks, actual read and matching feedback for a supplied new tool; implement it afterward if useful.

## Run and inspect

From the repository root after [setup](README.md):

```bash
uv run --frozen --offline python learn.py transfer
```

Expect completed, an observed count of two lines for notes.txt, and a trace path. The model responses are scripted; count_lines actually reads the synthetic workspace. Inspect [transfer_support.py](lab/transfer_support.py): definition → argument validation → injected function → matching tool result. The description guides selection; Python enforces the arguments and workspace boundary. The protocol is documented by [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

## Diagnose a wrong final answer

Predict the separate grades for this **authored counterexample**, then explain your evidence. It changes only the assistant's final text relative to the supplied successful exchange. It is not a captured model failure or a new command to run:

```text
Task: count notes.txt and report the observed count.
Actual count_lines result: 2
Matching result supplied to the next inference: 2
Final assistant answer: "There are 999 lines."
Loop stop: completed
Runner: VERIFIED: new read-only tool dispatched; matching result returned to the loop.
```

1. Did the tool execute correctly and did its result reach the next request?
2. Did the conversation complete? Did the task succeed?
3. Which claim does VERIFIED cover, and what additional comparison detects the wrong answer?

Record your explanation before checking below. In your own successful run, locate the equivalent result, next request, final answer and stop; check each separately.

<details>
<summary>Check your diagnosis</summary>

Tool execution and feedback integration passed; the loop completed. The task failed because the final answer says 999 while the actual count is 2. Compare the reported answer with the observed count to grade that task. The [existing runner](lab/run_transfer.py) verifies dispatch/observed count and completion, not final-answer accuracy. Its VERIFIED message can therefore coexist with this incorrect answer; do not treat it as an overall task grade. Preserve the narrow wiring check rather than silently changing its meaning.

</details>

This counterexample and questions are original project teaching material. The [inference/dispatch/feedback progression](https://ghuntley.com/agent/) is Huntley's; the task-outcome distinction is made explicit by this exercise.

## Make one change

Implement count_lines in [starter/transfer.py](lab/starter/transfer.py), using workspace.read(path). Count using Python's [str.splitlines semantics](https://docs.python.org/3.12/library/stdtypes.html#str.splitlines): blank lines count, an empty file has zero lines, and a final newline does not add an extra line. The supplied Workspace retains path checks.

```bash
uv run --frozen --offline python learn.py transfer --file tracks/01-author-the-loop/lab/starter/transfer.py
```

The untouched starter fails. A worked function is in [solutions/transfer.py](lab/solutions/transfer.py). The runner checks an actual dispatch and observed fixture count, rather than accepting the scripted assistant's final text. The tests exercise additional contents and invalid paths. This is a small behavior check, not proof of understanding.

Change the tool description in transfer_support.py and predict what changes. Replay will still request the same tool; it cannot measure description quality. Optional live observation uses `learn.py transfer --live --provider openrouter --model YOUR_MODEL`, with credentials configured as in [the live guide](live-observation.md). Record what actually happens; live behavior is not yet validated by this project.

## Completion

Explain where the tool is registered, where its arguments are validated, where the file read occurs, and how its result reaches the next inference. Show why changing the tool implementation changes execution while changing only its description does not change a fixed replay. Keep the supplied loop unchanged for this transfer exercise.
