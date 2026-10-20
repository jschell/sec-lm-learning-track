# Plan 15: Focus Track 1 worksheet section 1

Status: planned; owner requested this plan on 2026-10-20 (UTC) after an author-side review of worksheet section 1. Not implemented. The review was performed by an AI subagent: it is author preparation, not learner evidence, and does not replace [Plan 02](02-track1-pilot.md).

## Problem

Section 1 is the first activity every learner meets, and it asks for too much at once. In one section the learner predicts, runs two stages, reads code, uses the viewer, reads raw JSONL, considers an omitted-result thought experiment, reads the weights note, answers the account-disable question, performs the Lesson 2 variation and answers four record questions. That covers three of the six core outcomes.

Specific problems confirmed against the current text and a local run:

1. `learn.py stage 2` prints the full history, including the tool result and the final answer, before the learner opens the viewer. The terminal gives away what the viewer step asks the learner to find.
2. The viewer paragraph explains `input_added`, `input_reset` and `--cumulative` before the learner has seen viewer output; `input_reset` never appears in Stage 2.
3. The opening prediction asks about request 1 before the learner has seen any request, so there is little to anchor it.
4. The account-disable question has no trace to answer from and no place to record the answer.
5. Lesson 2's missing-file variation uses a 12-line Python snippet. It works, but the step teaches test plumbing more than the concept.
6. There is no "you should see" checkpoint a learner can use without the explanation being spoiled.
7. The record questions do not ask the learner to separate proposal from dispatch.

Keep, as the review also recommends: the predict → run → inspect cycle, the reminder that scripted responses are not model evidence, the missing-file variation and its point that the unchanged final text may now be false, the short Stage 2 viewer output, and the supplied worked code.

## Outcome and boundaries

A learner completes section 1 in short steps, each with one idea, one action and one thing to find. The terminal no longer reveals the answer before inspection, and the variation needs one command.

Keep the six core outcomes, the `#1-follow-one-exchange` and `#record-section-1` anchors, other worksheet section numbers, pilot assessment items and earlier grades. Keep complete worked code and narrow behavioral checks ([decision 0001](../../decisions/0001-worked-stages-first.md)). Do not add a new route, module, browser runtime or grading platform. Record the change as an instruction revision.

## Stage A — Stage command output

- `learn.py stage 1` and `stage 2` print a short summary by default: run directory, trace and summary paths, number of inference requests, completed tool calls and status. They do not print the tool result or final text.
- `--json` restores the current full output for learners who want it.
- `learn.py stage 2 --read PATH` changes only the path the scripted first response requests. It writes the changed replay copy into the run directory (never editing the source fixture) and sets the replay's expected outcome from whether that path exists in the copied workspace. Paths stay subject to the existing workspace confinement. It cannot be combined with `--replay-file` or `--live`.
- Existing behavior for `--replay-file`, run retention, summaries and Stage 3 output stays unchanged.

Acceptance: tests cover the default summary (no tool-result or final text in stdout), `--json` parity with the previous payload, `--read missing.txt` producing `is_error: true` in request 2 with the source fixture unchanged, an existing path succeeding, and rejected combinations. Existing tests that parse stage output keep passing.

## Stage B — Restructure section 1

Split section 1 into short steps under the existing heading:

1. **Run Stage 1.** Locate the request the controller built and the response; no tool is offered.
2. **Predict, then run Stage 2.** With a request now seen, predict whether notes.txt's bytes appear in request 1, request 2 or neither. Read the summary output.
3. **Open the viewer.** Find three named items: a proposed call with its ID, request 2 carrying the matching `tool_use_id`, and the final text. Explanation in a collapsible block. Introduce only the viewer terms that appear in Stage 2 output.
4. **Find the dispatch.** Locate `tools.dispatch` in the worked `exchange` function, then confirm the full IDs once in the raw JSONL.
5. **Vary one factor.** Run `learn.py stage 2 --read missing.txt`, predicting first, and compare request 2 and the final text. Lesson 2's snippet is replaced by the same command; its hints and self-check stay.
6. **Record.** Add a proposal-versus-dispatch question ("What proposed the read, what performed it, and how is the result matched to its call?") to the existing record questions.

Move material that does not belong in the first exercise:

- the weights note to the loop recap (`core-loop.md` already holds the state/weights section), keeping a short pointer from section 1;
- the account-disable question to "Explain and record completion", where there is a place to answer it;
- the omitted-result thought experiment to the record step as one question, or to the recap.

Update the worksheet progress table so outcome 6's activity names where its evidence now comes from (request 1 versus request 2 in section 1; the weights explanation in the recap). Update `docs/pilot/alignment-and-review.md` and `docs/pilot/README.md` to match, without changing assessment items or the five objectives.

Acceptance: section 1 has at most one new concept per step, each step names what to find, explanations sit behind collapsible blocks after the action, and every outcome remains evidenced somewhere on the core route. Links and anchors validate.

## Stage C — Records

Add an instruction revision line to the worksheet, a Plan 02 note telling the facilitator to record it, author checks in the Track 1 validation record, and a memory entry. Rerun the fresh-worktree walkthrough of the core route with the new commands.

## Evidence and limits

Author checks can show the commands work and the text is consistent. They cannot show that section 1 is now easier to learn from. After this plan, stop revising section 1 until the Plan 02 learner walkthrough provides evidence; record which revision the learner saw.

## Implementation checkpoints

- [ ] A: stage summary output, `--json` and `--read` implemented with tests.
- [ ] B: section 1 restructured; weights, account-disable and thought experiment moved; outcome mapping updated in worksheet and pilot documents.
- [ ] C: revision, Plan 02 note, validation record and memory updated; fresh-worktree walkthrough recorded.
- [ ] Published-revision checks recorded.

## Sources

The step-by-step structure, explanation after action and named checkpoints are project judgments informed by patterns recorded in [the exemplar review](../../research/2026-10-20-learning-exemplar-review.md) (futurecoder steps, Carpentries challenges with collapsible solutions). The client-tool call/result relationship remains sourced from [Anthropic's tool-use documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) as in the existing lessons. No upstream text or code will be copied.
