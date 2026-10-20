# Track 1: run, inspect and explain

> **Core route:** [1 Exchange](#1-follow-one-exchange) · [2 Errors](#2-follow-feedback-after-an-error) · [Loop recap](core-loop.md) · [4 Budget](#4-change-one-controller-setting) · [5 Transfer](#5-transfer-the-mechanism-to-a-new-tool) · [Record](#explain-and-record-completion)

This worksheet is the Track 1 core route from the [track entry](README.md). Work through the sections in the order above; each core section ends with a **Next in core** link, and supporting lessons link back here. Sections 3 and 6 are optional. Save a copy for your observations. The complete worked code is supplied; reconstruction is optional. Record elapsed time rather than treating the track's project estimate as a deadline.

The inference/tool-feedback progression comes from [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). The questions and pilot procedure here are original project design. Matching call/result IDs follow [Anthropic's client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

For the structured pilot, follow [the protocol](../../docs/pilot/README.md): sections **1, 2, 4 and 5** here plus the selected context lesson. Sections 3 and 6 and all model/execution extensions are optional self-study, outside that assessment.

## Prepare

From the repository root, follow the [uv installation link and prerequisites](README.md#prepare-once), then:

```bash
uv python install 3.12
uv sync --frozen
```

The core runs below need no model weights, provider account or Docker. Initial Python/uv setup may use the network. Later `--offline` commands are synthetic replay with real, bounded file operations in fresh repo-local run directories. Each run is retained; inspect its printed directory. Do not edit the source fixtures to change a run.

## Preserve your evidence

Read this once before section 1; there is no separate preservation step later. Every run you make is retained under `.cache/exercises/track-1/<exercise>/<run-id>/` in this checkout. Record each printed run path and the repository revision in the progress and session records at the end; save your filled worksheet in a run directory if useful:

```bash
git rev-parse HEAD
uv run --frozen --offline python learn.py trace RUN_DIRECTORY
```

Replace RUN_DIRECTORY with the actual printed path. The same viewer accepts its trace.jsonl file, and `--cumulative` shows bounded full input/history snapshots. Each run keeps work/ where applicable, trace.jsonl and result.json. Re-running creates another directory and preserves earlier runs. All are ignored by Git; source fixtures remain unchanged.

There is no automatic deletion. When a run is no longer needed, delete that specific run directory with your file manager after retaining any notes you need. Only delete an exercise directory if you intend to remove all its runs. Keep credentials and customer data out of these synthetic exercise artifacts. No manual copy from an OS temporary directory is required.

## 1. Follow one exchange

Six short steps. Each step names what to find; the explanation sits in a collapsible block after the action, so try first and open it second. [Lesson 1](01-minimal-inference.md) and [Lesson 2](02-one-tool-exchange.md) are supporting explanations if you want more.

### Step 1: one request, no tools

```bash
uv run --frozen --offline python learn.py stage 1
```

The command prints a short summary and the paths of a new run. Open the run with the `learn.py trace` command it prints.

**Find:** the request the controller sent and the response it got back. Was a tool call proposed?

<details><summary>Checkpoint</summary>

The viewer shows one `request` and one `response` containing only text. The controller built the request; the scripted model returned text. No tool was offered or proposed, so nothing ran.

</details>

### Step 2: predict, then run one exchange

Stage 2 offers the model a `read_file` tool, and `notes.txt` is in the run's `work/` folder. **Predict:** will the bytes of notes.txt appear in request 1, in request 2, or in neither? Write your answer and one reason before running.

```bash
uv run --frozen --offline python learn.py stage 2
```

**Find in the summary:** how many inference requests were made, and how many tool calls completed?

### Step 3: find three things in the viewer

Run the `learn.py trace` command the summary printed. Each `request` line shows `input_added`: the messages newly added since the previous request. Adding a message is not the same as running a tool, and the label says so.

**Find:**

1. In the first `response`, the `proposed_call` and its `id`.
2. In request 2, a `result` whose `tool_use_id` equals that `id`.
3. The final `response` text.

<details><summary>Checkpoint and explanation</summary>

The scripted model proposed `read-1`. Request 2 carries the assistant's call and a result with `tool_use_id` `read-1`, followed by a final text response. The file's bytes first appear in request 2, inside that result; request 1 has only the task. A file on disk is not input until the controller puts it in a request. Compare this with your step 2 prediction.

</details>

### Step 4: find the dispatch

Open the `exchange` function in [solutions/stages.py](lab/solutions/stages.py). **Find** the line that calls `tools.dispatch`. Then open the run's `trace.jsonl` in an editor, go to the second `request` record, and confirm that its last message carries the full `tool_use_id` and the same text as `work/notes.txt` in the run directory (in the trace it is JSON-escaped, so quotes and `\n` appear).

<details><summary>Checkpoint and explanation</summary>

`tools.dispatch` is where the controller actually performs the read; Stage 2 records no separate `tool` event, so the code and the file comparison are your evidence. A result appearing in history is not, on its own, proof that a read happened. The viewer shortens long values; the raw JSONL holds the complete bytes.

</details>

### Step 5: change one factor

**Predict:** if the scripted model asks for `missing.txt` instead, what will request 2 carry: an error result, no result, or file contents? Will the final text change?

```bash
uv run --frozen --offline python learn.py stage 2 --read missing.txt
```

`--read` changes only the path in a copy of the replay saved as `read-replay.json` in the new run; source fixtures are unchanged. Open the new run in the viewer and compare request 2 and the final response with your prediction. Graduated hints: [Lesson 2, Observe and vary](02-one-tool-exchange.md#observe-and-vary).

<details><summary>Checkpoint and explanation</summary>

Request 2 carries a result for `read-1` with `is_error: true`. The final text is unchanged, and now false: replay responses are scripted and do not adapt to the error. This is why a final answer needs its own check.

</details>

<a id="record-section-1"></a>

### Step 6: record

- What proposed the read, what performed it, and how is the result matched to its call?
- Which responses were scripted? How many inference requests were made?
- Would the scripted final answer alone prove that the file was read?
- If the controller had not appended the tool-result message, would the file's bytes still reach request 2? Answer from the message contents, not the scripted final response.

The separate weights explanation for outcome 6 comes in [the loop recap](core-loop.md#state-observation-and-weight-explanation), after section 2.

Optional practice, outside the core and the pilot assessment: [fix a broken exchange](02-one-tool-exchange.md#optional-fix-a-broken-exchange) with `learn.py fix`.

**Next in core:** [section 2: follow feedback after an error](#2-follow-feedback-after-an-error).

## 2. Follow feedback after an error

Predict what happens when a tool returns an error, then:

```bash
uv run --frozen --offline python learn.py stage 3
```

Inspect the new trace with the `Inspect:` command printed after the JSON (`uv run --frozen --offline python learn.py trace RUN_DIRECTORY`). Locate one `is_error: true` result, the following request carrying it, a later successful read and the terminal status. Explain why a tool error need not stop the loop. The next scripted response was authored in advance; it is not evidence that a real model recovered. See [the loop lesson](03-author-the-loop.md).

<details><summary>Error-feedback self-check — open after your explanation</summary>

The controller appends the error result and makes another request. Later successful reads are real workspace operations; the recovery choices are authored replay responses. This does not measure real-model recovery.

</details>

Optional practice, outside the core and the pilot assessment: [fix a loop that hides errors](03-author-the-loop.md#optional-fix-a-loop-that-hides-errors).

**Next in core:** [the loop on one page (recap)](core-loop.md).

## 3. Separate a file edit from program execution

> **Optional — not part of the core route.** The core continues at [section 4](#4-change-one-controller-setting).

```bash
uv run --frozen --offline python learn.py --scenario repair
```

Use its printed `directory` to open `trace.jsonl` and `work/fizzbuzz.py`. Follow the edit and compare the copied file with [the supplied repaired solution](lab/solutions/fizzbuzz.py). Which file changed? Which command outcomes were supplied by the replay helper? Explain why the printed `command_execution: false` matters before describing a FAIL→PASS result as an actual program run.

For genuine contained execution, use the separate [Docker extension](04-complete-a-task.md). It is optional for this worksheet.

## 4. Change one controller setting

Before running, choose what you expect from the second command, where the model requests two calls in one response but the controller allows one:

- (a) The first call runs, then the loop stops with `tool_limit`.
- (b) Neither call runs; the loop stops with `tool_limit` before dispatch.
- (c) Both calls run; the limit applies from the next turn.
- (d) The model is told about the limit and requests one call instead.

Write your choice and one reason, then run both:

```bash
uv run --frozen --offline python learn.py --scenario multi
uv run --frozen --offline python learn.py --scenario multi --max-calls 1
```

Inspect both traces with the `Inspect:` command each run prints (`uv run --frozen --offline python learn.py trace RUN_DIRECTORY`). Compare the requested calls, actual `tool` events and stop status. Identify which component owns the budget and whether either call in the refused batch ran. An intentional `tool_limit` is a controller stop; this CLI can exit successfully while reporting that status. Read the JSON/trace, not only the shell exit code.

Record your prediction and one piece of evidence that supported or changed it. Later, [the recording-only missing-guard exercise](08-learn-from-missing-guards.md) lets you study and add these checks yourself; it is separate from core completion.

<details><summary>Budget self-check — open after comparing your traces</summary>

The ordinary batch dispatches both calls. With max_calls=1, the controller refuses the whole two-call batch before either dispatch: tool_limit and zero completed calls, so (b). A successful CLI exit does not mean the task completed.

The other choices each reflect a different belief: (a) that the controller checks the budget call by call after starting a batch; (c) that the budget only applies to later turns; (d) that the model enforces the budget. In this controller, the budget belongs to the controller and is checked against the whole batch before any dispatch.

</details>

**Next in core:** [section 5: transfer the mechanism to a new tool](#5-transfer-the-mechanism-to-a-new-tool).

## 5. Transfer the mechanism to a new tool

```bash
uv run --frozen --offline python learn.py transfer
```

This command prints a `trace` field and an independently observed line count. Explain the definition, Python argument checks, actual `count_lines` function, matching result and next request. The expected count is two; the runner checks an actual dispatch rather than accepting the final scripted text. Complete [the wrong-answer diagnosis](06-transfer-tool.md#diagnose-a-wrong-final-answer) before marking the task-outcome objective demonstrated. The same lesson has an optional implementation exercise.

**Next in core:** [explain and record completion](#explain-and-record-completion).

## 6. Locate untrusted instructions

> **Optional — not part of the core route.** The core continues at [explain and record completion](#explain-and-record-completion).

```bash
uv run --frozen --offline python learn.py --scenario injection
```

In the full trace, locate the embedded instruction in the `read_file` result and in the next request. Distinguish file text, system instructions and tool permissions. What prevents writes or commands here? Why does a safe scripted outcome not establish a model's resistance to injection? Use [the untrusted-content lesson](07-untrusted-content.md) for the fixture and source attribution.

## Explain and record completion

Using one of your traces, explain who creates the request, who proposes the action, where access is enforced, how a result returns, and why the loop stops. Identify the state that changed and explain why appending a result does not update model weights; [the loop recap](core-loop.md#state-observation-and-weight-explanation) and [the state companion](../../modules/messages-and-model-input/state.md) expand that distinction.

Apply the same distinctions to the entry page's illustrative claim, "I disabled the account." Name what in a trace would show a proposed call, an actual dispatch and the reported result, and name an independent authorized read-back that would verify the resulting account state. A tool success report alone is insufficient.

Complete the six progress rows below using your saved evidence and explanation. Record each additional item separately:

- Controller familiarity: explain an exchange, error, stop and deliberate variation using your evidence.
- Optional authoring/transfer modification: describe the actual change and observed effect.
- Model observation: none / inspected author records / own local run / own hosted run; include whether the task passed separately from whether inference completed.
- Help needed and remaining blockers: quote the unclear instruction and propose the smallest correction.

## Progress and evidence

Use the same six outcomes as the [entry page](README.md#by-the-end-you-can). For each row, record **not attempted / partial / demonstrated**, an evidence path/event and your initial explanation. Assistance is separate: **N** none, **V** navigation clarification, **H** conceptual hint, **W** worked explanation. A demonstrated answer with H/W remains assisted. Neither exit status 0 nor VERIFIED alone establishes understanding. Pilot scoring stays in its separate facilitator record.

| Outcome | Core activity | Saved evidence / initial explanation | Status | Help |
| --- | --- | --- | --- | --- |
| Locate the model response and distinguish a proposed tool call from actual dispatch. | Section 1: proposed call (step 3) and dispatch (step 4) | | Not attempted | |
| Match a call/result ID and locate that feedback in subsequent inference input. | Section 1: request 2's matching result (steps 3–4) | | Not attempted | |
| Explain repeated feedback after a tool error, separating scripted recovery from model observation. | Section 2: error and next request | | Not attempted | |
| Change a controller budget and explain which operations ran and why the loop stopped. | Section 4: both budgets | | Not attempted | |
| Check the task outcome separately from conversation completion. | Section 5: actual count versus final response | | Not attempted | |
| Locate which file and history contents reach the next request; explain separately why ordinary tool feedback does not update model weights. | Section 1: compare request 1 with request 2 (step 3); answer the outcome 6 question in the loop recap | | Not attempted | |

## Observation notes

| Exercise | Prediction / explanation | Evidence: trace event, field or file | Help or unclear instruction |
| --- | --- | --- | --- |
| One inference and one exchange | | | |
| Error feedback | | | |
| Edit versus execution | | | |
| Budget variation | | | |
| New tool | | | |
| Untrusted content | | | |

## Session details

Date / learner or author desk check / repository revision / OS / Python / uv:

Start and finish time / previous experience / assistance received:

An independent pilot uses a Python-capable learner who did not author the lab. An author running these commands is a desk check. Record every clarification needed before supplying it. Keep customer information and credentials out of the notes.

## Optional: observe your own model run

Choose a route and follow its complete setup. They use the same reference loop through different transport formats:

| Route | Starting instructions | Record |
| --- | --- | --- |
| Local CPU, no provider key | [Tool-feedback setup](../../modules/tool-requests-and-feedback/README.md#start-local-inference-from-a-blank-slate), then [360M/example recipe](../../modules/tool-requests-and-feedback/README.md#run-the-observed-working-configuration) | Model/hash/runtime, prompt style, trace, actual read, final answer and independent `task_passed` |
| Hosted Anthropic or OpenRouter | [Hosted read-only experiments](live-observation.md#provider-setup) | Provider/model, predictions, requested calls, supplied errors/results and whether the answer is supported |

For the direct local recipe, prepare **360M only** if you do not need the 135M comparison; the setup guide explains that choice. It installs/builds the runtime and retrieves the model—no existing local instance is assumed. Local setup needs a compiler and downloads; physical Pi 4 operation is not yet validated. The local exercise uses an explicit teaching JSON text adapter, so it does not validate the hosted Messages endpoint or native function calling. Do not pass a local URL to `learn.py --provider`; its provider choices are the two hosted services.

You can inspect [the recorded local comparisons](../../modules/tool-requests-and-feedback/observations/prompt-comparison.json) without running a model. Record this as **inspection of author observations**, not your own model run. If you run neither live route, controller familiarity can still be completed.

For recorded checks and outstanding observations, see [current validation](VALIDATION.md).

Instruction revision: Plan 13 D, 2026-10-19 (America/Los_Angeles). Record this revision with new observations; retain original pilot responses and grades without rescoring them under the changed wording.

Navigation revision: 2026-10-20 (UTC). Core route order, Next-in-core links and optional-section banners changed; the loop recap now follows section 2. Record this revision with new observations; section numbers, anchors and assessment items are unchanged.

Feedback revision: 2026-10-20 (UTC), Plan 14. Section 4 now asks for a choice among stated predictions; optional fix-exercise links follow sections 1 and 2. Record this revision with new observations; section numbers, anchors and assessment items are unchanged.

Section 1 revision: 2026-10-20 (UTC), Plan 15. Section 1 is split into six steps with collapsible checkpoints; `learn.py stage` prints a summary by default (`--json` for full output); the missing-file variation is `learn.py stage 2 --read missing.txt`; the weights note moved to the loop recap and the account-disable question to completion. Record this revision with new observations; anchors and assessment items are unchanged.

Review-fix revision: 2026-10-20 (UTC), Plan 16. Sections 2 and 4 give the exact trace command; the outcome 6 row points to a question in the loop recap. Section 1 is unchanged. Record this revision with new observations; anchors and assessment items are unchanged.
