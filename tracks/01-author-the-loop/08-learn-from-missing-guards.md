# Learn from the missing guards

Status: runnable comparison. Estimated effort: 15–25 minutes.
Place in track: the later [Control and inspect section](05-control-and-inspect.md), after the tool exchange and repeated feedback in Lesson 3.

## Goal

Predict how missing stop-reason and call-budget checks change recorded proposals, then add a check and explain its effect without executing actions.

## Why observe a failure?

A minimal loop teaches how model-requested tools become execution and feedback. Omitting a guard can also teach why the controller needs one. Blocking every incomplete implementation at the first learning checkpoint obscures that progression.

In [Huntley's inspected code_search_tool.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/code_search_tool.go), the inner loop dispatches tool_use blocks, sends results back, and continues until no calls are present. It does not branch on stop_reason or impose turn/call budgets. It does set a per-response MaxTokens value. Its bash implementation runs directly through the host shell. These are observations of this pinned file, not a claim about every version or SDK behavior.

We preserve the minimal-loop lesson while making its omissions visible. The comparison below is original Python teaching code; no upstream implementation is copied.

## Predict, run, explain

```bash
uv run --frozen --offline python learn.py guards
```

The supplied [comparison](lab/compare_guards.py) sends the same authored proposals to a deliberately incomplete loop and the guarded reference. Its tools **only record labels**; they never read evidence, edit files, run commands or contact a service. The comparison has a finite outer limit. The normal command retains its comparison trace, per-case artifacts and result.json in the printed repo-local guards run directory. The parent trace records authored comparison observations; per-case trace detail varies between the minimal and guarded controllers.

Predict the recorded labels before reading the output:

| Authored response | Minimal loop | Guarded loop |
| --- | --- | --- |
| Truncated response containing one proposed call | Records partial | Records nothing; model_stop:max_tokens |
| Two-call batch with budget one | Records a and b | Records nothing; tool_limit |
| One prior call, then two calls with total budget two | Records a, b and c | Records a only; refuses the next whole batch |

A completed conversation label in the minimal loop does not establish valid execution. The result depends on which response fields and controller state the code actually checks.

Read minimal_loop in the comparison. Add one missing check in your own copy, rerun, and predict which row changes. Then inspect the reference's handling. Keep the recording-only tools while experimenting; this intentionally incomplete loop is not supplied as an execution-enabled controller.

> **What this demonstrates:** how specific omissions change dispatch, using simulated proposals. It does not require a model to misbehave, execute destructive actions or imitate a production harness.

## Check the later learning objective

Core familiarity checks verify requests, dispatch, matching feedback, repeated inference, the supplied task policy and a finite turn limit:

```bash
uv run --frozen --offline python learn.py check --stage 3 --file tracks/01-author-the-loop/lab/solutions/stages.py
```

The output explicitly states that the guard extension was not checked. After studying the comparison, verify terminal reasons and whole-batch/cumulative call budgets separately:

```bash
uv run --frozen --offline python learn.py check --stage 3 --guards --file tracks/01-author-the-loop/lab/solutions/stages.py
```

Use your starter file in place of the worked solution if reconstructing. An incomplete implementation can demonstrate core mechanics while failing the guard extension; those are different observations. Neither command is a production-safety certificate. The supplied reference retains its guards in ordinary runs and in the Docker execution path.

## Completion

Explain each row, identify which response field or counter changes the decision, and show one deliberate code change affecting the result. Then compare this controller-owned decision with [untrusted instructions arriving in tool data](07-untrusted-content.md), where model behavior and host permissions are separate questions.

Original sources: [Geoffrey Huntley's workshop](https://ghuntley.com/agent/) and the pinned implementation above. Guard policies, simulation and checkpoints are project teaching choices. [Source record](SOURCES.md) · [Return to track](README.md).
