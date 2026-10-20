# Plan 14: Targeted feedback and fix exercises for Track 1

Status: complete; owner requested plan and implementation on 2026-10-20 (UTC), merged in [PR 27](https://github.com/jschell/sec-lm-learning-track/pull/27). [Author and published-revision checks](../../../tracks/01-author-the-loop/VALIDATION.md#plan-14-targeted-feedback-and-fix-exercises) are recorded. Independent learner evidence remains under [Plan 02](../active/02-track1-pilot.md); nothing here claims it.

## Outcome and boundaries

A learner who writes or repairs a short exchange or loop gets a specific explanation of a common wrong implementation, not only "not verified". The learner can also practise three optional, bounded "fix this" exercises that isolate one defect each. This adapts two patterns sampled in [the exemplar review](../../research/2026-10-20-learning-exemplar-review.md):

- futurecoder's message steps: a plausible wrong solution receives its own targeted message;
- Rustlings' broken-file exercises: a small file with a `TODO` at the defect, a constraint, a one-line hint that narrows the location, and a mirrored solution.

These are original project implementations of the patterns; no upstream code or text is copied.

Keep the existing core route, six outcomes, worksheet section numbers, anchors and pilot items unchanged. The fix exercises are optional practice beside sections 1 and 2; they are not core completion requirements and not assessment items. Reuse the existing behavioral checker, run directories and CLI entry point. Do not add a browser runtime, watch mode, grading platform, mastery tracking, new module or engagement integration. Preserve [decision 0001](../../decisions/0001-worked-stages-first.md): checks remain narrow behavioral feedback and do not establish understanding.

## Stage A — Targeted checker diagnoses

When the existing stage 2/3 checks find a history mismatch, classify the observed request against the expected one and report:

- what was observed and what was expected (the call/result relationship involved);
- why it matters for the loop;
- where to look in the learner's function.

Cover at least: assistant call missing before its result; results never appended; results appended before the assistant call; a result whose `tool_use_id` does not match the call; result content that differs from the actual dispatch; an omitted error result; a missing second inference. Unrecognized mismatches keep the existing general message. Diagnoses must derive from observed requests and actual dispatch, never from the learner's source text.

Acceptance: each named wrong implementation produces its specific diagnosis in tests; correct implementations still pass; existing regressions keep failing.

## Stage B — Optional fix exercises and `learn.py fix`

Supply three broken files, each with a `TODO`, a stated edit limit and a single defect:

| Exercise | Stage checked | Defect |
| --- | --- | --- |
| `exchange-missing-call` | 2 | Results are appended without the assistant message that requested them |
| `exchange-skipped-inference` | 2 | The final answer is constructed locally instead of coming from a second inference |
| `loop-drops-errors` | 3 | Error results are filtered out before feedback |

A manifest lists each exercise's stage, constraint and a two-rung hint ladder (where to look, then which relationship to check). Mirrored solutions carry a one-line explanation comment.

`learn.py fix` lists exercises. `learn.py fix NAME` copies the exercise into a fresh retained run under `.cache/exercises/track-1/fix-NAME/<run-id>/work/` and prints the file path, the exact check command and the hint command. `learn.py fix NAME --hint N` prints one hint rung. Re-running `learn.py fix NAME` gives a fresh copy; earlier runs are retained. Source exercise files are never edited in place.

Acceptance: each unmodified exercise fails the existing check with its Stage A diagnosis; each mirrored solution passes; copying is exclusive and repository-local; unknown names and hint levels produce actionable errors.

## Stage C — Learner documents and predictions

- Lesson 2 and Lesson 3 gain an optional "Fix a broken …" section after their existing activity; the worksheet points to them as optional practice after sections 1 and 2.
- Worksheet section 4 states its prediction as choices whose wrong options encode specific misconceptions. The keyed answer must match behavior already asserted by existing tests (`tool_limit` and zero dispatched calls); cite those tests in the validation record rather than adding tests that mirror wording.
- The track README "Going further" table and `learn.py --help` list the fix exercises.
- Record attribution in the Track 1 source record, the instruction revision in the worksheet, and author checks in the Track 1 validation record.

Acceptance: optional practice is labelled as outside the core and outside the pilot assessment; links and anchors validate; the revision is recorded.

## Delivery and evidence

Deliver A–C in one reviewable PR because the exercises depend on the diagnoses. Run the Track 1 suite and dependent offline suites, the relative-link check, `git diff --check`, and a fresh-worktree walkthrough of `learn.py fix` for each exercise (unmodified fails with its diagnosis; mirrored fix passes). Record unperformed checks explicitly. Learner usefulness of the messages and exercises is not established by these checks; observe it in the Plan 02 walkthrough.

## Implementation checkpoints

- [x] A: targeted diagnoses implemented with regressions.
- [x] B: three fix exercises, manifest, mirrored solutions and `learn.py fix` implemented with regressions.
- [x] C: lessons, worksheet, help, source and validation records updated ([author checks](../../../tracks/01-author-the-loop/VALIDATION.md#plan-14-targeted-feedback-and-fix-exercises)).
- [x] Published-revision checks recorded ([merge `d383f22`](../../../tracks/01-author-the-loop/VALIDATION.md#published-plan-14-revision)).

## Original patterns and sources

futurecoder [`core/text.py` and chapter step definitions](https://github.com/alexmojaki/futurecoder/tree/def491c2a348371f56249d05c64e0cf70f33ac2b/core) (MIT) and Rustlings [exercises and `info.toml`](https://github.com/rust-lang/rustlings/tree/bc8e51115c9304fbd036f5d6fca683e71363468f) (MIT), both inspected at the pinned commits on 2026-10-20 (UTC) for the [exemplar review](../../research/2026-10-20-learning-exemplar-review.md). The exercise defects, messages, manifest format and CLI are original project design. These sources do not establish that the patterns improve learning for this audience.
