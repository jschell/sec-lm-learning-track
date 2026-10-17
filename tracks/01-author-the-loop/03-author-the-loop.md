# 3. Inspect and vary the loop

Status: authored; offline reference checked. Estimated effort: 60–120 minutes.
Prerequisites: tool call/result exchange. Use the supplied loop starter even if you skipped the earlier authoring exercises.

## Goal

Explain the harness control flow and deliberately change it. Reconstruct it if that helps your learning.

## Explanation

A single exchange becomes a loop when the second model response can request more work. At each iteration, the model receives the updated messages and can choose another tool or end its turn. The controller chooses which tools exist, validates execution requests, returns results, and enforces stopping limits.

This is the central mechanism demonstrated in [Huntley's workshop](https://ghuntley.com/agent/). The distinction between model-directed action and predefined workflows is discussed in [Anthropic's Building effective agents](https://www.anthropic.com/engineering/building-effective-agents). Our bounded loop is original implementation work.

Read [the loop on one page](core-loop.md) before the full file. Core completion requires one request, correctly linked results, repeated feedback, and a finite stop. Implementing every extra guard in the reference is an extension; keep those guards enabled when running its tools.

## Worked example

First run `uv run --frozen --offline python learn.py stage 3`. Inspect the short run_loop in [solutions/stages.py](lab/solutions/stages.py). Its synthetic model requests several unsuccessful operations before a successful read. Tools remain read-only. Then compare the additional guards in [lab/loop.py](lab/loop.py). Its main path is:

1. Build request from instructions, messages, schemas, and max_tokens.
2. Infer once and inspect content and stop_reason.
3. Reject unsupported/truncated responses before executing proposed effects.
4. Append the assistant content.
5. If end_turn contains no calls, record completed.
6. Preflight the whole call batch against the remaining call limit.
7. Dispatch sequentially, log each result, append all results together, and continue.

For two requested calls, both IDs are preserved and both results are appended in one user message. Sequential execution here is a teaching choice; it is not parallel scheduling.

```bash
uv run --frozen --offline python learn.py --scenario multi
uv run --frozen --offline python learn.py --scenario limit --max-turns 2
```

Expected: completed with two calls for multi; turn_limit with two calls for limit. The latter has a final result message but no subsequent model inference because the controller exhausted its turn budget. This lab does not resume terminal histories automatically.

## Optional reconstruction

Implement run_loop in [starter/loop.py](lab/starter/loop.py). The signature is the same as the reference implementation. The CLI injects your implementation without replacing the supplied model or tool code:

```bash
uv run --frozen --offline python learn.py --scenario read --loop-file tracks/01-author-the-loop/lab/starter/loop.py
uv run --frozen --offline python learn.py --scenario multi --loop-file tracks/01-author-the-loop/lab/starter/loop.py
uv run --frozen --offline python learn.py --scenario limit --max-turns 2 --loop-file tracks/01-author-the-loop/lab/starter/loop.py
```

Start with read. Add multiple calls, finite limits, error handling and trace events. Check the required behavior with `uv run --frozen --offline python learn.py check --stage 3 --file tracks/01-author-the-loop/lab/starter/loop.py`. The check covers no-tool completion, single and multiple calls, repeated inference, error feedback, and a two-turn stop. Then compare with run_loop in the reference. The untouched starter deliberately fails. Do not import the reference run_loop as your answer.

## Observe and vary

Change the controller's call limit, keeping the replay fixed:

```bash
uv run --frozen --offline python learn.py --scenario multi --max-calls 1
```

Expected: tool_limit and zero executed calls. The controller refuses the whole batch before side effects. Compare this with a design that stops halfway through a batch: what state would remain?

Also explain which parts of a request must remain stable and which change after tool execution. A list of available functions is different from the growing conversation.

## Completion check

Explain every transition of a read run, correctly return both results in multi, stop at a limit, and change one limit intentionally. Point to the exact lines that append assistant messages, execute tools, and append results.

## Troubleshooting and boundaries

Repeatedly sending the original messages hides the prior result from inference. Exiting on the first text block is wrong because a response can contain text and tool calls. Treating max_tokens as successful completion can execute an incomplete proposal; this lab stops without executing it. Replay tool-call IDs must be unique across the run.

No shell runs in these scenarios. A completed status describes conversation termination, not task correctness or model competence.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| Inference/tool-feedback loop | [Huntley workshop](https://ghuntley.com/agent/), pinned Go stages in [source record](SOURCES.md) | Conceptual adaptation, no source code copied |
| Client result format | [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Protocol documentation checked 2026-10-16 |
| Workflow versus agent | [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Limits and batch policy are project choices |

Try the small [read-only tool transfer](06-transfer-tool.md) before adding execution machinery.

[Next: complete a task](04-complete-a-task.md).
