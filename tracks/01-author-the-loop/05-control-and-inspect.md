# 5. Control and inspect

> **Core route:** [1 Exchange](pilot-worksheet.md#1-follow-one-exchange) · [2 Errors](pilot-worksheet.md#2-follow-feedback-after-an-error) · [Loop recap](core-loop.md) · **4 Budget (supports this)** · [5 Transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool) · [Record](pilot-worksheet.md#explain-and-record-completion)

Status: authored; offline checks verified. Estimated effort: 45–90 minutes.
Full-page estimate includes additional failure/guard exercises; the core worksheet requires only its budget variation. Estimates are provisional project judgments, not learner timings.
Prerequisites: use the supplied reference loop or your completed starter.

## Goal

Diagnose failed exchanges, enforce finite execution, and explain the limits of this learning harness.

> **What this demonstrates:** Observable failure and stopping behavior in the supplied lab. Model behavior, production security and learner usability require separate evidence.

## Explanation

An agent loop needs an owner for each failure. A missing file is a tool failure the model can observe. Invalid protocol structure is a controller failure. A provider outage is an inference failure. A turn limit is a deliberate stop. These should not all become “the agent finished.”

Anthropic's [tool-call protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) defines is_error on returned results. The finite retry policy, stop statuses, batch preflight, and path rules here are project choices extending the simple loop demonstrated by [Huntley](https://ghuntley.com/agent/).

## Learning objective: discover missing controller checks

After authoring the basic loop, [run the missing-guard comparison](08-learn-from-missing-guards.md). Predict what happens when a loop ignores stop_reason or forgets previously dispatched calls. The recording-only tools make those mistakes observable. Add a check, compare the behavior, and explain why the result changed. The initial authoring exercise does not require these guards to pass; this section teaches their purpose afterward.

The optional --guards check verifies that extension once implemented. The supplied execution-enabled reference keeps its controls throughout.

## Worked failure exercises

```bash
uv run --frozen --offline python learn.py --scenario recover
uv run --frozen --offline python learn.py --scenario truncated
uv run --frozen --offline python learn.py --scenario multi --max-calls 1
uv run --frozen --offline python learn.py --scenario limit --max-turns 2
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
```

| Scenario | Expected behavior |
| --- | --- |
| recover | Missing file, wrong argument type, unknown tool; three error results, then successful read |
| truncated | model_stop:max_tokens; proposed edit is not executed |
| multi with one-call limit | tool_limit; no partial execution of the two-call batch |
| limit with two turns | turn_limit; finite inference and tool calls |

Each replay reliably supplies the failure and follow-up responses shown in the table.

The tests additionally exercise path traversal and symlinks, ambiguous edits, duplicate IDs before side effects, output limits, terminal provider failure, and mocked HTTP serialization. Run [verify_docker.py](lab/verify_docker.py) separately for actual timeout, output, and container checks; mocks cannot prove those boundaries.

## Trace exercise

Use [the trace guide](trace-format.md). For one recover run:

1. Locate the first assistant tool_use and its result.
2. Show the matching IDs and is_error=true.
3. Locate the next inference request and verify it contains that result.
4. Find the successful read and final stop event.
5. Explain why a final assistant answer alone cannot reconstruct execution.

Now author one extra failing test in a copy of test_lab.py: send an extra unexpected argument to read_file, or call run_command when no executor is enabled. Confirm rejection before any operation occurs.

## Untrusted evidence

Follow the short [injected-file walkthrough](07-untrusted-content.md) to see instructions arrive as tool-result data. It uses the same loop and keeps writes/commands disabled.

## Enforcement and limits

- All tool paths are relative to a dedicated synthetic workspace; symlinks and '..' are rejected. This is a single-user lab, not a race-resistant multi-tenant file service.
- No command runs on the host. Docker gets no network, no forwarded key, a read-only root, dropped capabilities, a non-root UID, process/memory/CPU limits, and one writable workspace. /grader is read-only.
- Tool commands time out; forced container removal terminates their children. Cleanup failure is terminal and requires inspecting Docker rather than silently continuing.
- Requests and calls have finite counts; each request has an output-token cap and transport timeout. There is no dollar-budget enforcement or automatic retry.
- Files have per-file read/write limits and command output is drained while retaining at most 4096 source bytes. Text tool results retain at most 4096 Unicode characters before the truncation marker; these are separate limits. A split UTF-8 command character is decoded with replacement. The writable volume has no aggregate disk quota; runtime isolation and filesystem denial are not universal escape prevention.
- Traces contain full requests and bounded tool observations, including synthetic file contents. They are not redacted production telemetry and do not reveal private model reasoning.

The combination of untrusted content, private data, and external communication is discussed in [Simon Willison's original lethal-trifecta article](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). This lab avoids actual private data and does not certify resistance to prompt injection. Deeper engagement controls belong in Track 5.

## Completion check

Demonstrate an error returned to the model and a controller limit stopping a run. Explain which enforcement is independent of the model, which results are synthetic, and which boundaries require a real Docker check. State the limits honestly when handing the lab to another consultant.

## Troubleshooting

When trace storage remains writable, an error terminal status has an error trace event. A storage failure can leave an incomplete trace. Exceptions escaping a learner implementation, including replay exhaustion, are recorded as execution failures, with an unknown dispatch count when the controller cannot establish it. Inspect the workspace for completed effects; an error does not roll them back. A returned dispatch is counted before logging; a dispatch that raises is marked uncertain with tool_calls=null. See [failure accounting](trace-format.md#failure-accounting-and-credential-diagnostics). A model_stop status means generation ended for a reason this lab does not continue. The CLI does not resume such histories automatically. Re-run into a fresh workspace after inspecting the evidence. Do not replay uncertain side effects against an existing engagement environment.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| Simple loop baseline | [Huntley workshop](https://ghuntley.com/agent/) | Failure policies are original project additions |
| Tool-result errors | [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Checked 2026-10-16 |
| Execution controls | [Docker run](https://docs.docker.com/engine/containers/run/), [Docker security](https://docs.docker.com/engine/security/) | Actual versus configuration-only checks distinguished in validation record |
| Prompt-injection data flow | [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Original source; no general safety claim |

**Next in core:** [worksheet section 5: transfer the mechanism to a new tool](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool). [Track 1 entry](README.md).
