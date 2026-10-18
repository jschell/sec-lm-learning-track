# Track 1: run, inspect and explain

Use this worksheet alongside the [track entry](README.md) and [one-page loop](core-loop.md). Save a copy for your observations. The complete worked code is supplied; reconstruction is optional. Record elapsed time rather than treating the track's project estimate as a deadline.

The inference/tool-feedback progression comes from [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). The questions and pilot procedure here are original project design. Matching call/result IDs follow [Anthropic's client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

For the structured pilot, follow [the protocol](../../docs/pilot/README.md): sections **1, 2, 4 and 5** here plus the selected context lesson. Sections 3 and 6 and all model/execution extensions are optional self-study, outside that assessment.

## Session details

Date / learner or author desk check / repository revision / OS / Python / uv:

Start and finish time / previous experience / assistance received:

An independent pilot uses a Python-capable learner who did not author the lab. An author running these commands is a desk check. Record every clarification needed before supplying it. Keep customer information and credentials out of the notes.

## Prepare

From the repository root, follow the [uv installation link and prerequisites](README.md#prepare-once), then:

```bash
uv python install 3.12
uv sync --frozen
```

The core runs below need no model weights, provider account or Docker. Initial Python/uv setup may use the network. Later `--offline` commands are synthetic replay with real, bounded file operations in newly copied workspaces. Each invocation starts fresh; inspect the printed directory before removing it. Do not edit the source fixtures to change a run.

## 1. Follow one exchange

Run the worked examples, read their small functions in [solutions/stages.py](lab/solutions/stages.py), then explain what changed between them:

```bash
uv run --frozen --offline python learn.py stage 1
uv run --frozen --offline python learn.py stage 2
```

Each command prints `Trace:` followed by its path. Copy the **Stage 2** path, replacing TRACE_PATH below with that actual path:

```bash
uv run --frozen --offline python learn.py trace TRACE_PATH
```

The viewer is a compact event summary. Open the same JSONL file in your editor to inspect complete `request` and `history` values. Stage 2 records the result in the second request and final history; it does not emit a separate `tool` event. Stages 1–2 finish with a response/history; the repeated loop additionally writes an explicit `stop` event. Find the assistant `tool_use`, the matching `tool_result.tool_use_id`, and the returned file text in the second request. Compare that text with `work/notes.txt` beside this trace.

Record: What performed the read? Which responses were scripted? How many inference requests were made? Would the scripted final answer alone prove that the file was read?

## 2. Follow feedback after an error

Predict what happens when a tool returns an error, then:

```bash
uv run --frozen --offline python learn.py stage 3
```

Inspect the new trace. Locate one `is_error: true` result, the following request carrying it, a later successful read and the terminal status. Explain why a tool error need not stop the loop. The next scripted response was authored in advance; it is not evidence that a real model recovered. See [the loop lesson](03-author-the-loop.md).

## 3. Separate a file edit from program execution

```bash
uv run --frozen --offline python learn.py --scenario repair
```

Use its printed `directory` to open `trace.jsonl` and `work/fizzbuzz.py`. Follow the edit and compare the copied file with [the supplied repaired solution](lab/solutions/fizzbuzz.py). Which file changed? Which command outcomes were supplied by the replay helper? Explain why the printed `command_execution: false` matters before describing a FAIL→PASS result as an actual program run.

For genuine contained execution, use the separate [Docker extension](04-complete-a-task.md). It is optional for this worksheet.

## 4. Change one controller setting

Predict the difference between these runs before executing them:

```bash
uv run --frozen --offline python learn.py --scenario multi
uv run --frozen --offline python learn.py --scenario multi --max-calls 1
```

Inspect both traces. Compare the requested calls, actual `tool` events and stop status. Identify which component owns the budget and whether either call in the refused batch ran. An intentional `tool_limit` is a controller stop; this CLI can exit successfully while reporting that status. Read the JSON/trace, not only the shell exit code.

Record your prediction and one piece of evidence that supported or changed it. Later, [the recording-only missing-guard exercise](08-learn-from-missing-guards.md) lets you study and add these checks yourself; it is separate from core completion.

## 5. Transfer the mechanism to a new tool

```bash
uv run --frozen --offline python learn.py transfer
```

This command prints a `trace` field and an independently observed line count. Explain the definition, Python argument checks, actual `count_lines` function, matching result and next request. The expected count is two; the runner checks an actual dispatch rather than accepting the final scripted text. Follow [the transfer lesson](06-transfer-tool.md) for the optional implementation exercise.

## 6. Locate untrusted instructions

```bash
uv run --frozen --offline python learn.py --scenario injection
```

In the full trace, locate the embedded instruction in the `read_file` result and in the next request. Distinguish file text, system instructions and tool permissions. What prevents writes or commands here? Why does a safe scripted outcome not establish a model's resistance to injection? Use [the untrusted-content lesson](07-untrusted-content.md) for the fixture and source attribution.

## Observation notes

| Exercise | Prediction / explanation | Evidence: trace event, field or file | Help or unclear instruction |
| --- | --- | --- | --- |
| One inference and one exchange | | | |
| Error feedback | | | |
| Edit versus execution | | | |
| Budget variation | | | |
| New tool | | | |
| Untrusted content | | | |

## Optional: observe your own model run

Choose a route and follow its complete setup. They use the same reference loop through different transport formats:

| Route | Starting instructions | Record |
| --- | --- | --- |
| Local CPU, no provider key | [Tool-feedback setup](../../modules/tool-requests-and-feedback/README.md#start-local-inference-from-a-blank-slate), then [360M/example recipe](../../modules/tool-requests-and-feedback/README.md#run-the-observed-working-configuration) | Model/hash/runtime, prompt style, trace, actual read, final answer and independent `task_passed` |
| Hosted Anthropic or OpenRouter | [Hosted read-only experiments](live-observation.md#provider-setup) | Provider/model, predictions, requested calls, supplied errors/results and whether the answer is supported |

For the direct local recipe, prepare **360M only** if you do not need the 135M comparison; the setup guide explains that choice. It installs/builds the runtime and retrieves the model—no existing local instance is assumed. Local setup needs a compiler and downloads; physical Pi 4 operation is not yet validated. The local exercise uses an explicit teaching JSON text adapter, so it does not validate the hosted Messages endpoint or native function calling. Do not pass a local URL to `learn.py --provider`; its provider choices are the two hosted services.

You can inspect [the recorded local comparisons](../../modules/tool-requests-and-feedback/observations/prompt-comparison.json) without running a model. Record this as **inspection of author observations**, not your own model run. If you run neither live route, controller familiarity can still be completed.

## Explain and record completion

Using one of your traces, explain who creates the request, who proposes the action, where access is enforced, how a result returns, and why the loop stops. Identify the state that changed and explain why appending a result does not update model weights; [the state companion](../../modules/messages-and-model-input/state.md) expands that distinction.

Record each demonstrated item separately:

- Controller familiarity: explain an exchange, error, stop and deliberate variation using your evidence.
- Optional authoring/transfer modification: describe the actual change and observed effect.
- Model observation: none / inspected author records / own local run / own hosted run; include whether the task passed separately from whether inference completed.
- Help needed and remaining blockers: quote the unclear instruction and propose the smallest correction.

For recorded checks and outstanding observations, see [current validation](VALIDATION.md).
