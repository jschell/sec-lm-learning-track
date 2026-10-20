# 2. One tool exchange

> **Core route** — *The loop:* [Part 0](00-the-loop.md) · **1 Exchange (supports this)** · [2 Errors](pilot-worksheet.md#2-follow-feedback-after-an-error) · [Loop recap](core-loop.md) — *Controls:* [4 Budget](pilot-worksheet.md#4-change-one-controller-setting) — *Evidence:* [5 Transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool) — *Application:* [Record](pilot-worksheet.md#explain-and-record-completion)

Status: authored; offline reference checked. Estimated effort: 45–60 minutes.
Full-page estimate includes reconstruction and variations; the core worksheet uses the supplied exchange. Estimates are provisional project judgments, not learner timings.
Prerequisites: Lesson 1 concepts; supplied starter is independently usable.

## Goal

Return a tool result that matches a model-requested call, with correct message ordering.

> **What this demonstrates:** A real workspace read, matching call/result IDs, and the result supplied to another request. Assistant responses are authored replay data.

## Predict before inspecting the exchange

If you arrived from worksheet section 1, you have already made this prediction and run the variation: use the hints under [Observe and vary](#observe-and-vary). Otherwise, from the repository root, before opening the worked messages below, write your prediction: if read_file requests `missing.txt`, will the next inference receive an error result, no result, or file contents? What will associate that feedback with the request? Keep your first answer. The complete worked function remains available in [solutions/stages.py](lab/solutions/stages.py).

## Explanation

A tool definition describes an available operation. A tool call is a request to perform it. Your registry and dispatch code turn that request into execution; the description grants no machine access by itself. The host program retains responsibility for validation and boundaries.

[Huntley](https://ghuntley.com/agent/) introduces read_file to expose this exchange. Anthropic's [client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) represents the call as tool_use in assistant content and the matching tool_result in the next user message. Other providers have different wire formats.

## Worked example

A definition includes a name, description, and input_schema. Our read_file schema requires exactly one string argument, path. The same rule is enforced in Python; the schema alone is not our enforcement.

```json
{"role":"assistant","content":[
  {"type":"tool_use","id":"read-1","name":"read_file","input":{"path":"notes.txt"}}
]}
```

The controller dispatches read_file and appends:

```json
{"role":"user","content":[
  {"type":"tool_result","tool_use_id":"read-1","content":"Synthetic exercise...","is_error":false}
]}
```

The content above is abbreviated for teaching. In an actual lab trace, the content is the bounded text returned by Tools.result. The ID ties this result to that call; the function name alone cannot distinguish repeated calls.

```bash
uv run --frozen --offline python learn.py stage 2
```

This runs the complete two-request tool exchange function in [solutions/stages.py](lab/solutions/stages.py) and prints a summary; add `--json` to print the full history and final response. Inspect that function and the run's trace with the printed `learn.py trace` command. Requests and responses are recorded; replay responses are synthetic, while file reads are real. The second request must contain the assistant call and the actual matching tool result.

The compact viewer shows proposed call IDs and newly supplied results; add --cumulative for bounded full history snapshots. Stage 2 has no standalone tool event: locate the actual dispatch in the worked function, then inspect the raw second request for complete bytes. The repeated-loop reference in Stage 3 additionally logs each dispatch as a tool event.

## Optional reconstruction

Implement exchange in [starter/stages.py](lab/starter/stages.py). Make one inference request, append its assistant content, dispatch tool_use blocks, append the results as one user message, then infer again with that history. Return the final response and feedback history; including that actual final assistant response at the end of returned history is also accepted.

```bash
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/starter/stages.py --stage 2
```

The check observes two actual inference requests, dispatch, and the returned feedback; a fabricated final answer fails. This bounded two-request exercise assumes the first response requests tools and the second ends. Lesson 3 removes that assumption. Use the supplied stages solution as your independent starting point if needed.

## Observe and vary

All commands on this page run from the repository root after [setup](README.md#prepare-once). First run the worked exchange above. Open its printed run directory using `learn.py trace RUN_DIRECTORY`. Locate:

1. Response 1's proposed call and ID.
2. `tools.dispatch` in the worked `exchange` function: this is the invocation, rather than a second kind of model response.
3. Request 2's matching result, `is_error`, and returned bytes; compare those bytes with `work/notes.txt`. Stage 2 has no separate dispatch event.

Now change only the requested path:

```bash
uv run --frozen --offline python learn.py stage 2 --read missing.txt
```

`--read` writes a changed copy of the replay, `read-replay.json`, into the new run and sets its expected result from whether the path exists in that run's workspace; the source fixture and earlier runs are unchanged. Inspect the **new** run. Compare the call path, matching result, and request 2 against your prediction. The mechanical check is the replay oracle accepting the actual error result; it does not grade your explanation or the final answer. To edit other parts of a response, copy `lab/replay/read.json` yourself and pass it with `--replay-file`.

<details><summary>Hint 1 — where to look</summary>

Use response 1 and request 2 in the viewer. Find the corresponding `exchange` lines that append assistant content and dispatch it.

</details>

<details><summary>Hint 2 — relevant relationship</summary>

Match the proposed call's `id` to `tool_use_id` in the following user message. An error is still feedback: inspect `is_error` and its content, then verify that message is in request 2.

</details>

<details><summary>Hint 3 — annotated explanation / self-check</summary>

The controller attempts the actual read. The missing path produces an error result with `tool_use_id=read-1` and `is_error=true`; that result is supplied to request 2. The scripted final text is unchanged and may now be false. Replay does not adapt to the error. The matching ID and actual feedback establish the exchange mechanics, not answer correctness or real-model recovery.

</details>

## Completion check

**Mechanical:** both runs reach their second request with the actual matching result; the variation carries an error. Optional reconstruction has its separate `learn.py check` command above.

**Explain:** If two successive calls use the same function name but different IDs and paths, how would you associate their results? If the final assistant claimed the missing file was read successfully, what evidence would contradict that claim?

<details><summary>Explanation self-check</summary>

Associate each result by call ID, not function name. The error result contradicts a successful-read claim; conversation completion is separate from correctness. A trace records the controller's observations. For a consequential external action, use an independent authorized read-back of the resulting state rather than trusting only the tool's success report.

</details>

## Key points

The model proposes; the controller validates and invokes. Matching IDs preserve the call/result relationship. Error results belong in subsequent input too. A terminal response does not establish task success.

## Optional: fix a broken exchange

Outside the core route and the pilot assessment. Each exercise is a short copy of the exchange with one defect, a `TODO` at the defect and an edit limit. From the repository root:

```bash
uv run --frozen --offline python learn.py fix exchange-missing-call
uv run --frozen --offline python learn.py fix exchange-skipped-inference
```

Each command copies the exercise into a fresh run directory and prints the file to edit, the exact check command and the hint command. Run the check before editing: the message names what the second request contained, what was expected, why it matters and where to look. Hints come in two rungs (`--hint 1`, then `--hint 2`) and never give the code. After your check passes, compare with the solution path the command printed. Re-running the command gives a fresh copy; earlier copies are retained.

A passing check means the exchange's mechanics matched the synthetic model's expectations; it does not grade your explanation.

## Troubleshooting and boundaries

Do not append only the tool result while omitting the assistant call. Do not put tool text into system instructions. File paths must be relative, with no '..' or symlinks. Reads are confined to a disposable synthetic workspace; files over 64 KiB are refused, and the result text keeps at most 4,096 characters before a `[truncated]` marker. A response whose tool-call IDs repeat is refused before anything is dispatched, because results are matched to calls by ID. Command execution is disabled in this exercise.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| File tool progression | [Huntley workshop](https://ghuntley.com/agent/); pinned read.go in [source record](SOURCES.md) | Conceptual inspiration; original fixtures/code |
| Schemas | [Anthropic: Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) | Checked 2026-10-16 |
| IDs, message ordering, errors | [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Checked 2026-10-16; no live API validation |

**Next in core:** [return to worksheet section 1 and record it](pilot-worksheet.md#record-section-1). Supporting explanation for section 2: [Lesson 3](03-author-the-loop.md).

Activity revision: 2026-10-19 (America/Los_Angeles), Plan 13 D. This original project activity borrows scoped practice/hints from [Exercism](https://exercism.org/docs/building/tracks/concept-exercises) and objectives/challenge/key-points structure from [The Carpentries](https://carpentries.github.io/sandpaper-docs/episodes.html), opened 2026-10-19. No upstream text or code copied. Existing pilot item IDs/forms and prior grades are unchanged; record this revision for future observations.
