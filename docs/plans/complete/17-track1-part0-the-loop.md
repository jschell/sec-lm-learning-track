# Plan 17: Track 1 Part 0, the loop first

Status: complete; owner requested this plan on 2026-10-20 (UTC) after adopting [decision 0003](../../decisions/0003-base-understanding-first.md), and it merged in [PR 35](https://github.com/jschell/sec-lm-learning-track/pull/35). [Author and published-revision checks](../../../tracks/01-author-the-loop/VALIDATION.md#plan-17-part-0-the-loop) are recorded. The comparison with Huntley's workshop that informs it was an author-side review; it is not learner evidence and does not replace [Plan 02](../active/02-track1-pilot.md).

## Outcome

A learner new to agents first establishes base understanding of the loop, in Huntley's order, before any focus area. Part 0 sits in front of the existing core route and leaves worksheet section 1 (frozen by Plan 15), section numbers, anchors, pilot assessment items and earlier grades unchanged.

Base understanding, as defined in decision 0003: the conversation is re-sent history; a tool definition, a proposed call and a dispatch differ; results, including errors, return as messages matched to calls by ID; the loop repeats until no call is proposed; the loop is small. The check is predicting request N+1 from request N.

## Boundaries

- Original Python and fixtures; Huntley's progression is cited, no upstream code is copied (the pinned repository has no licence file).
- Part 0's loop is deliberately guard-free, like Huntley's. Keep it safe by construction: scripted replay only (live mode refused), read-only tools only (`read_file`, `list_files`, and `count_lines` from the transfer), and replay files that end. Do not reuse it for execution.
- Reading, predicting and watching are core. Writing the loop and a real-model run are optional, per decision 0001 and decision 0003.
- Do not add a browser runtime, grading platform, new module or engagement integration. Do not create another Track 1 route: Part 0 becomes the start of the existing one.

## Stage A — Minimal loop and Part 0 commands

- Add a learner-facing minimal loop (about 15 lines of loop logic, plus the supporting tool-definition code it shows) as `lab/part0/minimal_loop.py`, structured like Huntley's two nested loops: an outer loop over scripted user turns, an inner loop that dispatches every proposed call, appends all results as one user message, and asks again until no call is proposed. Unknown tools and tool failures become error results, as in Huntley's first tool stage.
- Add `learn.py part0 STEP` for five steps, each with its own scripted replay:
  1. `chat`: two user turns, no tools; the history grows.
  2. `tools`: prints the read-only tool definitions (name, description, input schema) and the Python function each name dispatches to.
  3. `exchange`: one proposed `read_file` call, its result, the next request.
  4. `loop`: several turns including one error result (a missing file) before the final answer.
  5. `more-tools`: the same loop with `list_files` added; then point to the existing `count_lines` transfer.
- Output is a live transcript printed as the loop runs, in the spirit of Huntley's terminal: `You:`, `Model (scripted):`, `tool:`, `result:`, `error:` lines, plain text by default. Each run is also retained under `.cache/exercises/track-1/part0-STEP/<run-id>/` with `trace.jsonl` and `result.json`, and prints its `Inspect:` command, so later sections can view the same run.
- Tests: transcript lines for each step; history growth across the two chat turns; the error result reaches the next request; read-only tools only; live mode refused; finite on replay; repository-local retained runs; source fixtures unchanged. Update the teaching-code manifest.

Acceptance: each step runs offline with one command, prints a readable transcript, and cannot execute commands or edit files.

## Stage B — The Part 0 page

- Add `tracks/01-author-the-loop/00-the-loop.md`, one short section per step: one idea, a prediction to write first, the command, then a collapsible checkpoint. The predictions build towards "predict request N+1".
- The tool-definition step shows where the controller looks a tool up by name, and that a description grants no access.
- The loop step makes the point that the whole mechanism is small, then names what it deliberately lacks (stop-reason checks, limits, duplicate-ID checks) as things later sections add, without teaching them yet.
- Optional, after the core steps: write the loop yourself, checked by a Part 0 mode of the existing checker that covers feedback, multiple calls, multiple turns and error results, but not limits (limits are taught later). Optional: observe the same loop with a real model through the existing local or hosted routes.
- Close with key points that restate the five base-understanding statements.

Acceptance: a learner can complete Part 0 without reading any other page; every prediction precedes its answer; optional steps are labelled.

## Stage C — Entry page, route and outcomes

- Track 1 README: open with the loop and Huntley's point that it is small; the core route starts at Part 0, then sections 1, 2, the recap, 4, 5 and completion. Move the account-disable security framing below the route, as the first application; move the stack of limitation notes to a short "what this lab does and does not show" footer.
- Group the six outcomes under "The loop" (outcomes 1–3 and the history half of 6) and "Controls and evidence" (4, 5 and the weights half of 6), without renumbering. Add layer banners to the sections: the loop (Part 0, sections 1–2), controls (4), evidence (5, recap), application (completion).
- Worksheet: add a Part 0 record block before section 1, with prediction-and-observation rows for its steps. Section 1 text is unchanged. Update the core-route strip to include Part 0.
- Collection README: describe Track 1 as the base every focus area builds on.

Acceptance: links and anchors validate; existing anchors and section numbers are unchanged; the revision is recorded.

## Stage D — Focus areas build on the base

- Each module README states Track 1 base understanding (Part 0 at minimum) as a prerequisite and opens with one recall question about the loop, answered in a collapsible block. Modules: context and state; generation and sampling; messages and model input; output validation and uncertainty; tool interfaces and protocols; tool requests and feedback; untrusted input and authority.
- Label the Track 1 extensions (Lessons 4, 7 and 8 and worksheet sections 3 and 6) as focus areas built on the loop: containment, untrusted input and guards.

Acceptance: every module and extension names the base it assumes; no module depends on a learner's unfinished code.

## Stage E — Pilot and records

- Pilot protocol: after the baseline form, the learning route begins with Part 0, then the existing sections. Update `docs/pilot/README.md`, the pilot checklist and the alignment table so Part 0 evidence maps to the existing objectives. Assessment items and grades are unchanged.
- Add an instruction revision line to the worksheet; note it in Plan 02; record author checks in the Track 1 validation record; add memory entries; add a line to AGENTS.md pointing to decision 0003.
- Run the full suite, link checks, manifests and a fresh-worktree walkthrough of Part 0 and the core route.

## Evidence and stop rule

Author checks can show Part 0 runs and reads consistently. Whether it establishes base understanding is for the Plan 02 walkthrough. After Plan 17, stop tuning Track 1 and run that walkthrough; revisit decision 0003 with its evidence, including whether Part 0 makes parts of sections 1–2 redundant.

## Implementation checkpoints

- [x] A: minimal loop and `learn.py part0` steps with transcript output and tests.
- [x] B: Part 0 page with predictions, checkpoints and optional steps.
- [x] C: entry page, route, outcome grouping, banners and worksheet Part 0 block.
- [x] D: module prerequisites and recall questions; extensions labelled as focus areas.
- [x] E: pilot documents, records and fresh-worktree walkthrough.
- [x] Published-revision checks recorded ([merge `54729cc`](../../../tracks/01-author-the-loop/VALIDATION.md#published-plan-17-revision)).

## Sources

Huntley's progression and loop structure are cited from [his workshop](https://ghuntley.com/agent/) and the [pinned repository](https://github.com/ghuntley/how-to-build-a-coding-agent/tree/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e) (`chat.go`, `read.go`, later stages), inspected 2026-10-20 (UTC). Call/result pairing and error results follow [Anthropic's client-tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). Step design, predictions and checkpoints are project judgments informed by [the exemplar review](../../research/2026-10-20-learning-exemplar-review.md).
