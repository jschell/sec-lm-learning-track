# Plan 16: Track 1 review fixes and CI hygiene

Status: implemented in a reviewable change; owner requested this plan, including CI hygiene, on 2026-10-20 (UTC) after an author-side review of tests, CI and validation claims at `1566b4e`, and asked for implementation after PR 32 merged. [Author checks](../../../tracks/01-author-the-loop/VALIDATION.md#plan-16-review-fixes-and-ci-hygiene) are recorded; published-revision checks follow merge. The review was performed by an AI subagent: it is author QA, not learner evidence, and does not replace [Plan 02](02-track1-pilot.md).

## Findings carried forward

Re-checked by the author on `1566b4e` before planning:

- The worked `run_loop` in `lab/solutions/stages.py` dispatches two calls that share one ID and reports `completed` with two calls; the guarded `lab/loop.py` rejects duplicate IDs. The worked `exchange` has the same gap.
- Lesson 8 asks learners to predict the recorded labels and then shows the answer table immediately.
- `VALIDATION.md` line 11 still reports 84 local tests; the suite has 100.
- Lesson 5 says Docker has "one writable workspace", but the executor also mounts an 8 MB `noexec` tmpfs at `/tmp`.
- Running `learn.py` with no arguments runs a scenario instead of showing help.
- `stage 3`, `--scenario` runs and `transfer` print raw JSON without an `Inspect:` command, and worksheet sections 2 and 4 say "inspect the trace" without giving it. With `--json`, the `Run:`/`Summary:`/`Trace:` lines follow the JSON on stdout, so the output is not valid JSON.

Reported by the reviewer and not yet reproduced (verify each before changing code): removing Docker `--user`, `no-new-privileges` or `noexec` leaves the offline suite passing (only the real-daemon CI job would fail); five tool-boundary caps and one run-directory symlink check survive mutation; one test is over-mocked; argparse errors name scripts such as `stage_demo.py`; an untouched transfer starter reports only `status: error`; `list_files` shows symlink names; `read_file` results truncate at about 4 KB (`TEXT_OUTPUT_CHARS`); `fixture-manifest.json` does not cover solutions or starters. Both placeholders `TRACE_PATH` and `RUN_DIRECTORY` appear in learner documents.

Kept as is, with reasons recorded: a learner file can pass the stage 3 check with `from loop import run_loop`. [Decision 0001](../../decisions/0001-worked-stages-first.md) states the checks are not an anti-cheating system, and Lesson 3 already says not to import the reference. The loop recap's budget code previews the section 4 answer; the reviewer judged the placement defensible, and the recap gains one line saying it previews the guards.

## Boundaries

Keep worksheet section 1 frozen (Plan 15), the six core outcomes, section numbers, anchors, pilot items and earlier grades. Keep complete worked code and narrow behavioral checks. Do not add an anti-cheating layer, grading platform, new module or route. Record learner-visible wording changes as an instruction revision.

## Stage A — Correctness of the worked code

- Add a short, visible duplicate-ID check to the worked `exchange` and `run_loop`: reject a response whose tool-call IDs repeat (within the response, and for `run_loop` across turns) before any dispatch, recorded as an error with no dispatch. Keep it to a few lines with a teaching comment; this changes code learners read, so Lessons 2 and 3 mention it in one sentence.
- Regression: duplicate IDs cause no dispatch and an error status in both worked functions; existing checks and fix exercises still pass.

Acceptance: the worked code and the guarded reference agree on duplicate IDs; tests fail if the check is removed.

## Stage B — Accurate documentation

- Validation record: update the summary row to the current count with its date and revision, and link to the latest dated section instead of repeating historical counts elsewhere.
- Lesson 5: describe the writable workspace and the `/tmp` tmpfs (size, `noexec`) accurately, matching `loop.py`.
- Placeholders: use `RUN_DIRECTORY` in current learner and pilot documents (the viewer accepts a run directory or its `trace.jsonl`). Leave dated historical records unchanged.
- State the `read_file` result limit (`TEXT_OUTPUT_CHARS`) where the tool is described, and say whether `list_files` lists symlink names while reads reject them.
- Loop recap: one line noting that its budget code previews what section 4 tests.

Acceptance: each statement matches the code it describes; links and anchors validate.

## Stage C — Consistent command output

- `stage 3`, `--scenario` runs and `transfer` end with an `Inspect: uv run --frozen --offline python learn.py trace RUN_DIRECTORY` line, as stages 1 and 2 do.
- With `--json`, stdout carries only JSON; the `Run:`/`Summary:`/`Trace:` lines go to stderr. Tests parse stdout with `json.loads`.
- `learn.py` with no arguments prints the same help as `--help`; `learn.py --scenario NAME` and existing commands keep working.
- Argparse usage and errors show `learn.py COMMAND` rather than internal script names.
- The stage summary labels counts as completed dispatches that may include error results (for example "Completed tool calls (error results included)").
- An untouched transfer starter reports that `count_lines` is not implemented yet and names the file to edit, instead of only `status: error`.
- Worksheet sections 2 and 4 give the exact trace command (sections 2 and 4 are not frozen).

Acceptance: tests cover each output contract; existing tests that parse output are updated deliberately, not weakened.

## Stage D — Learner text

- Lesson 8: move the answer table into a collapsible block after the prediction prompt.
- Outcome 6: add one question, in the loop recap and the worksheet progress row, that asks the learner to distinguish "the context list grew" from "the model learned", answered from their own trace.

Acceptance: predictions precede their answers; outcome 6 has an answerable question on the core route.

## Stage E — Test gaps

- Add an offline test that inspects the Docker command the executor builds and fails if `--user`, `--security-opt no-new-privileges`, `--network none`, read-only root, dropped capabilities or the `noexec` tmpfs option is removed. The real-daemon CI job remains the behavioral check.
- Reproduce the reviewer's cap and symlink mutations (`MAX_FILE_BYTES`, `TEXT_OUTPUT_CHARS`, `COMMAND_OUTPUT_BYTES`, argument size checks, run-directory symlink rejection). For each that survives, add a focused boundary test; record any that were already caught.
- Identify the over-mocked test and replace the mock with the real component where that stays deterministic and offline; record the decision if the mock is kept.
- Extend `fixture-manifest.json`, or a sibling manifest, to hash worked solutions, starters and fix exercises so unintended edits are detected; document the update procedure.

Acceptance: each targeted removal or mutation makes a test fail; no test merely mirrors document text.

## Stage F — CI hygiene

- Add `timeout-minutes` to every job in all workflows, sized from recent run durations with headroom, and a per-ref `concurrency` group that cancels superseded runs on pull requests but not on `main`.
- Pin `actions/checkout`, `actions/upload-artifact` and any other tag-referenced actions to full commit SHAs with the version in a comment, as `setup-uv` already is. Resolve each SHA from the upstream repository and record it.
- Pin the Docker executor image by digest in both the workflow pull and the executor default, recording the tag, digest and date checked; document how to update it. Keep the existing evidence that records the digest actually pulled.
- Confirm path filters still trigger dependent suites after the changes.

Acceptance: workflows pass on the published revision; every external action and image reference is immutable and its provenance recorded.

## Delivery and evidence

Deliver as one reviewable PR, or split CI hygiene (F) into its own PR if workflow changes need separate review. Run the Track 1 suite and dependent offline suites, link and whitespace checks, fixture hashes, and a fresh-worktree walkthrough of the core route. Local Docker is unavailable; Docker behavior is established only by the published CI run. Record unperformed checks explicitly. After Plan 16, stop tuning Track 1 against AI reviews and proceed to Plan 02's human evidence.

## Implementation checkpoints

- [x] A: duplicate-ID check in worked code with regressions.
- [x] B: validation, Lesson 5, placeholders, limits and recap wording corrected.
- [x] C: output contracts consistent across commands, with tests.
- [x] D: Lesson 8 spoiler hidden; outcome 6 question added.
- [x] E: Docker-flag, cap/symlink mutation, mock and manifest test gaps addressed.
- [x] F: CI timeouts, concurrency, action SHA pins and image digest pin.
- [ ] Published-revision checks recorded.

## Sources

Anthropic's [tool-use documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) remains the source for call/result ID pairing. Implementation must recheck GitHub's official documentation for [workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) (`timeout-minutes`, `concurrency`) and [security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) (pinning actions to a full commit SHA), and Docker's documentation on [pulling an image by digest](https://docs.docker.com/reference/cli/docker/image/pull/), before relying on them. These are references to verify during implementation, not claims of checks already performed.
