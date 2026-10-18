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

## Make one change

Implement count_lines in [starter/transfer.py](lab/starter/transfer.py), using workspace.read(path). Count using Python's [str.splitlines semantics](https://docs.python.org/3.12/library/stdtypes.html#str.splitlines): blank lines count, an empty file has zero lines, and a final newline does not add an extra line. The supplied Workspace retains path checks.

```bash
uv run --frozen --offline python learn.py transfer --file tracks/01-author-the-loop/lab/starter/transfer.py
```

The untouched starter fails. A worked function is in [solutions/transfer.py](lab/solutions/transfer.py). The runner checks an actual dispatch and observed fixture count, rather than accepting the scripted assistant's final text. The tests exercise additional contents and invalid paths. This is a small behavior check, not proof of understanding.

Change the tool description in transfer_support.py and predict what changes. Replay will still request the same tool; it cannot measure description quality. Optional live observation uses `learn.py transfer --live --provider openrouter --model YOUR_MODEL`, with credentials configured as in [the live guide](live-observation.md). Record what actually happens; live behavior is not yet validated by this project.

## Completion

Explain where the tool is registered, where its arguments are validated, where the file read occurs, and how its result reaches the next inference. Show why changing the tool implementation changes execution while changing only its description does not change a fixed replay. Keep the supplied loop unchanged for this transfer exercise.
