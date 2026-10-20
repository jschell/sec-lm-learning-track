# Track 1 validation

Updated 2026-10-20 UTC (2026-10-19 America/Los_Angeles). This is the authoritative current Track 1 check summary. Implementation tests, actual model observations, and independent learner usability are separate claims.

## Current status

Target Python 3.12+, default 3.12; uv 0.12.23. Prior author handoff check: Linux x86_64, CPython 3.12.15 in a new virtual environment; earlier implementation checks used 3.12.14. No hosted-provider credentials or local Docker execution were used in this desk check. [Commands, findings and scope](../../docs/validation/2026-10-17-learner-handoff.md).

| Check | Observed result |
| --- | --- |
| Standard-library functional suite through frozen/offline uv | **84 tests passed locally** |
| Worked request/exchange/loop behavioral checks | Passed for the short worked stages; loop contract also passed for the guarded reference |
| Wrong learner submissions | Core rejects fabricated response/feedback, skipped inference and discarded task policy; the separate --guards extension rejects ignored stop/batch/cumulative limits |
| Missing-guard comparison | Minimal and guarded loops produce the expected six observations with recording-only tools; core completion is distinct from the --guards extension |
| Terminal guards | Truncated, inconsistent-stop, batch-limit and cumulative-limit cases require no unauthorized dispatch; short and guarded loops pass |
| Injection data flow | Actual read reaches only tool-result data in the next request; read-only definitions and unchanged target verified |
| Task instructions and diagnostics | Read-only requests contain no grader instructions; bounded JSON diagnostics redact synthetic credentials; thinking blocks stop before dispatch |
| Trace and failure classification | One response per stage request; escaped learner replay exhaustion recorded as execution error with trace and unknown call count |
| Three stage launchers and transfer | Passed offline; transfer reads actual fixture contents; path and line-count edge cases checked |
| Replay scenarios and repair artifact | Passed; scripted observations distinguished from actual file edits |
| Short learn.py entry and trace inspection | Passed |
| Read-only mode and omitted tools | Dispatch blocks edits/commands and removed tools; alternatives remain available |
| Read-only live task wiring | Passed with synthetic provider response; not live behavior |
| Anthropic/OpenRouter exchanges and credentials | Mocked HTTP checks passed, including no cross-provider fallback or secrets in traces |
| Actual Docker FAIL→edit→PASS and execution controls | Expanded effective-protection and removal probes passed on published D/E revision; [exact run](#published-de-revision-and-final-author-walkthrough); no local Docker run |
| Actual hosted-model observation | **Not performed**; neither provider credential configured during corrective review |
| Actual local-model observation through the reference loop | Separately observed: explicit 360M/example configuration with a teaching text adapter. [Model/task records and CI recipe](../../modules/tool-requests-and-feedback/VALIDATION.md). This does not validate the hosted Messages transport |
| Learner handoff | [Worksheet](pilot-worksheet.md) commands desk-checked by the author; full-trace/history inspection and local/hosted routes clarified |
| Independent fresh-learner pilot | **Not performed**; [prepared checklist](pilot-checklist.md) |

## Pilot-preparation desk check

[Plan 11 preparation audit](../../docs/pilot/alignment-and-review.md#author-command-audit): fresh worktree and new uv environment on Linux x86_64/CPython 3.12.15; all required pilot commands and the two context-selection variants passed. Viewer regressions distinguish proposals, permissions, recording-only decisions and actual read effects. No hosted call or local Docker run was performed in this pass. The [pilot package](../../docs/pilot/README.md) is author-prepared; independent human review, learner responses and delayed observations remain pending.

## Learning-path and viewer desk check

Checked 2026-10-18 UTC (2026-10-17 America/Los_Angeles) on Linux x86_64/bash, CPython 3.12.15 and uv 0.12.23. A fresh detached worktree at `f031b13a76bf552206d3e51bd9edfec2bcba032c` received this change's candidate files; uv created a new environment. Git/uv, the installed interpreter and host cache already existed. This is not a fresh-OS, native Windows, WSL, macOS or Pi validation.

The revised core route passed using frozen/offline uv: stages 1/2/3, Stage 2 trace inspection, multi with normal/one-call budgets, and the supplied transfer. Stage 2 shows proposed read-1 and its matching result supplied in request 2, with actual bytes equal to work/notes.txt; no separate execution event was invented. Stage 3 retained five requests, three error results and a successful read. Multi completed with two calls; the one-call limit refused both calls and reported tool_limit with zero dispatches. Transfer observed two actual lines.

Top-level --help/-h and all five command-specific help routes passed. The worksheet's Python workspace-copy command preserved every source file's bytes and refused an existing destination with FileExistsError. The 53-test Track 1 suite passed in this fresh environment, including new exchange/error/repeated-history/bounded-payload and help regressions. Generated desk-check artifacts were inspected under the fresh worktree's ignored .cache/usability-audit/ and copied .cache/evidence/stage2-1/. Changed Markdown destinations/anchors and whitespace were checked separately.

No model, provider credentials, tokenizer or local Docker was used. Context behavior, assessment questions and historical model grades did not change. The six-outcome worksheet supports core progress; stable pilot IDs O1–O5 separately cover overlapping concepts and the named selection companion. Independent human review, learner performance and measured timing remain pending.

## Pre-pilot diagnosis clarification

Checked 2026-10-17 (America/Los_Angeles), Python 3.12.15 through frozen/offline uv: the unchanged Stage 2 exchange supplies actual notes.txt bytes in request 2 and not request 1. A bounded author probe changed only the replay's final answer to “There are 999 lines.” The actual count remained 2 and the unchanged transfer runner returned 0/VERIFIED, confirming its narrow wiring scope. This is an authored counterexample, not captured model behavior; no code, runner grade or fixture was changed. The transfer lesson now uses that case for task-outcome diagnosis. The weights statement is separately explained, not measured by replay. Changed Markdown links/fragments and whitespace were checked. No additional learner, model or platform validation occurred.

## Plan 13 Stage A: credential and failure boundaries

Author checks on Linux x86_64, CPython 3.12.14/uv 0.12.23, based on main `53618254f40aec2022657caf80a3400e9ea465b0` plus this PR's changes. Frozen/offline unittest suites passed: Track 1 (64), context (7), authority (7), output validation (9), tool-feedback (18). The worked Stage 3 core/guard check and supplied transfer also passed. No real credential, network inference or local Docker was used; the HTTP header probe never connects. These are pre-commit checks, not a completed learner pilot or a new Docker claim. Published CI will identify the exact candidate revision in the PR; merge checks must be verified at handoff.

New regressions exercise both provider credential normalization, empty/internal-control/non-ASCII rejection, local header failure, no leaked raw exception context, configured/escaped secret redaction in terminal logs, and real fixture effects before dispatch/trace exceptions. Returned dispatches remain counted when tool-event writing fails; raised dispatches report uncertain effects and tool_calls=null in both repeated-loop implementations. Malformed short-stage responses record error/stop; live Stage 3 is routed to the guarded reference and live Stages 1/2 are rejected before credentials are accessed.

Workspace retention, viewer/checker improvements, the activity revision and Docker/shared-CI work remain Plan 13 B–E. No learner understanding, platform portability or protection beyond these checks is inferred.

## Plan 13 B/C: retained runs and learner diagnostics

Author checks 2026-10-19 (America/Los_Angeles), Linux x86_64: 79 Track 1 tests passed locally on CPython 3.12.14/uv 0.12.23, and again in a fresh detached worktree/new uv environment on CPython 3.12.15. The fresh worktree began at merged Stage A `8d6d0776d244e0361eb0251e74b544d31654b12d` and received this PR's candidate files; Git/uv and host OS prerequisites already existed. Interpreter preparation downloaded Python 3.12.15; the learner commands ran frozen/offline. Dependent local offline suites also passed: context 7, authority 7, output validation 9, feedback 18. These pre-commit checks are not a fresh OS/platform or learner-pilot validation.

The fresh-worktree walkthrough retained 16 runs: stages 1–3, all eight scenarios, the one-call budget variation, supplied transfer, guard comparison, Stage 3 core/guard checker and Stage 2 launched from another working directory. All run directories, traces and summaries stayed beneath that checkout's ignored .cache/exercises/track-1/ root. Stage 1/2 directory viewing recognized short-stage completion, new-feedback and cumulative views worked, and the budget view displayed max_calls=1 with zero actual dispatches. All 14 fixture hashes remained unchanged. Audit stdout/stderr were inspected under the fresh worktree's ignored .cache/bc-audit/; they are author artifacts, not learner responses.

New regressions cover concurrent/exclusive run allocation, preservation of earlier files, private replay permissions, rejection of substituted output-directory symlinks, artifact ignore rules, all learner routes from outside the repo, friendly replay/loop/syntax errors, explicit summary marking when trace storage fails, valid Stage 2 histories with or without the actual final response, refusal of fabricated history, default feedback deltas/history reset, malformed/truncated/missing traces and budget visibility. Normal commands retain output; internal isolated unit checks may still use temporary directories. Viewer success means it read a terminal record, not that the task or learner passed.

The published PR/merge revision must identify CI results at handoff. No local Docker, hosted inference, real credential or learner validation was used for B/C. Plan 13 D/E remain open for the activity revision and advertised-protection/shared-CI checks.

## Hosted checks

[Merged-main run 38993985114](https://github.com/jschell/sec-lm-learning-track/actions/runs/38993985114) passed Python 3.12, Python 3.13, and actual Docker integration for merge commit e57b7bc9c3056a05279e15ea842356d161e6edfd. This includes the worked stages, behavioral rejection regressions, and read-only transfer exercise. Docker checks cover genuine FAIL→edit→PASS, a read-only grader, absent API credentials, bounded output, and timeout/child cleanup.

The current workflow runs the expanded suite on 3.12/3.13 plus the Docker integration check. See [main checks](https://github.com/jschell/sec-lm-learning-track/actions?query=branch%3Amain) for the latest revision. A workflow file alone is not passing evidence. No CI run substitutes for model observation or a learner pilot.

## Repeat implementation checks

From the repository root after [setup](README.md):

```bash
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 1
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 2
uv run --frozen --offline python learn.py check --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 3 --guards
uv run --frozen --offline python learn.py transfer
uv run --frozen --offline python learn.py --scenario injection
uv run --frozen --offline python learn.py guards
docker pull python:3.12-slim
uv run --frozen --offline python tracks/01-author-the-loop/lab/verify_docker.py
```

Fixture provenance/hashes and original protocol/runtime sources are in [SOURCES.md](SOURCES.md). Docker's floating image tag and unselected live model limit exact reproduction. Tests and the observation checklist are original project work; they make no general model-quality or production-safety claim.

Corrective-review implementation tests passed locally. Actual Docker checks, including the multibyte byte-prefix check, run in [the corrective branch CI](https://github.com/jschell/sec-lm-learning-track/actions?query=branch%3Afix%2Ftrack1-review). Hosted compatibility and live injection resistance remain open; follow the bounded [hosted smoke-test record](live-observation.md#bounded-smoke-test-record). Local read-only task observations have their separate record linked above; neither scripted injection nor an ordinary local read-and-answer run establishes injection resistance.

## Plan 13 D/E: activity and protection checks

Author candidate checks 2026-10-19 (America/Los_Angeles), Linux x86_64, Python 3.12.14/uv 0.12.23, based on merged B/C `204b563c805f24df3706cc8d7a7c3bf8781a8499`. The B/C merge's [Track 1 run 39363740585](https://github.com/jschell/sec-lm-learning-track/actions/runs/39363740585) passed offline Python 3.12/3.13 and its then-existing Docker checks. That is historical evidence for B/C, not the expanded checks in this revision.

The exchange activity now has a fresh missing-file prediction, runnable exclusive replay-copy variation, three collapsible hints, explicit mechanical/explanation checks and a changed-case question. Worksheet administration follows the immediate core exercises. Original pilot IDs, assessment forms, responses and grades were not changed; future observations must record the instruction revision. The 999-line counterexample remains authored text; weights remain an architectural explanation, not a replay measurement.

84 Track 1 tests passed, including a regression for Docker null CapDrop and retained noexec defaults. Five isolated source-removal probes were rejected by their targeted tests: cross-turn ID uniqueness, exact read arguments, parent-symlink rejection, exclusive trace creation and private trace mode. These are bounded author probes, not comprehensive mutation analysis. The explicit Docker integration now seeds both synthetic host provider values and checks effective identity, NoNewPrivs, capabilities, root/grader read-only mounts, isolated networking, tmpfs/noexec and resource settings. Seven disposable-container removal probes must detect the relevant weakened protection. No external connection or real credential is used. Local Docker is unavailable: only actual CI execution can establish whether these new integration checks pass.

CI path filters for protocol, generation/feedback and output-validation now include the shared Track 1 lab subtree; authority already included it, and context/model-input/Track 1 run without path filters. Markdown-only edits outside model-related trees do not trigger generation downloads. Fresh-environment walkthrough and published-revision evidence are recorded at handoff below. Independent human review, learner observations, retention, hosted inference and physical Pi checks remain pending.

### Published D/E revision and final author walkthrough

Published code revision [`592c822d11bd162cedaf30b98ee0e908a46ff297`](https://github.com/jschell/sec-lm-learning-track/commit/592c822d11bd162cedaf30b98ee0e908a46ff297), [PR 25](https://github.com/jschell/sec-lm-learning-track/pull/25): [Track 1 run 39364505709](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505709) passed Python 3.12/3.13 and **actual Docker integration**. Logs confirm effective runtime protections, both seeded host-only credentials, seven targeted configuration-removal probes, genuine FAIL→edit→PASS, bounded output and timeout/child cleanup. The first probes exposed two test assumptions, now corrected: Docker reports omitted CapDrop as null, and may retain noexec as a tmpfs default. The tmpfs check therefore requires the explicit configured policy as well as the observed mount and execution restriction; omission alone was not evidence that execution became possible. Docker image pulled in this run: `python:3.12-slim`, digest `sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1`.

Dependent published checks passed: [context 39364505608](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505608), [authority 39364505686](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505686), [output/feedback 39364505684](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505684), [protocol/MCP 39364505605](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505605), and [model input/tokenizer 39364505582](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505582). [Generation 39364505639](https://github.com/jschell/sec-lm-learning-track/actions/runs/39364505639) passed contracts on 3.12/3.13; its separate actual-model job was still running at this record's preparation. It is not claimed as passing new model evidence.

A fresh detached worktree at B/C merge `204b563c805f24df3706cc8d7a7c3bf8781a8499` plus candidate files, with a new uv environment on CPython 3.12.14, passed the final 84 Track 1 tests and dependent offline suites: context 7, authority 7, output 9, feedback 18, generation 14, direct protocol 4 (143 total). Git/uv, the interpreter and host prerequisites already existed. The core walkthrough passed stages 1/2/3, directory and cumulative viewing, the documented missing-file replay-copy variation, both budgets, supplied transfer, recording-only guards and the Stage 3 guard check. The changed result has is_error=true in request 2. Runs/notes remain beneath that checkout's ignored artifact root; all 14 fixture hashes are unchanged. Author audit captures are under ignored .cache/de-audit/ in that worktree. This was pre-commit author preparation, followed by the published code checks above—not a learner pilot or fresh-OS validation. Relative Markdown destinations/fragments and whitespace were checked at handoff.

Plan 13 author implementation is complete. This documentation close-out does not change the verified executable files. Merge verification remains the next handoff; independent human review, learner observations/delayed checks, hosted inference and physical Pi validation remain separate and pending.

## Plan 14: targeted feedback and fix exercises

Author candidate checks 2026-10-20 (UTC), Linux x86_64, CPython 3.12.3, uv 0.12.23 environment, on implementation commit `ce856cd95288d59b16fa3c989705e538f88e406f` (based on `0f19ec3b7180950482c2d5693c4a13377d443335`). [Plan 14](../../docs/plans/complete/14-track1-targeted-feedback-and-fix-exercises.md) adds targeted checker diagnoses and three optional `learn.py fix` exercises.

- A fresh detached worktree with a new uv environment passed 95 Track 1 tests: the previous 84 plus 11 in `test_fix_exercises.py`. They cover each named diagnosis from a deliberately wrong implementation, each unmodified exercise failing with its manifest diagnosis, each mirrored solution passing, manifest completeness, list/hint/error output, and fresh, private (0600), repository-local copies made from another working directory with the source file unchanged.
- In that worktree, each exercise was copied with `learn.py fix NAME`, checked unmodified (NOT VERIFIED with its targeted message), overwritten with its mirrored solution and checked again (VERIFIED). Copies stayed under the ignored `.cache/exercises/track-1/fix-*/` root; `git status` stayed clean.
- The section 4 prediction key (b) matches the runs in that worktree: `--scenario multi` completed with 2 tool calls; `--max-calls 1` stopped with `tool_limit` and 0 tool calls. Existing tests already assert this behavior (`test_entry_help.py` scenario route, `test_lab.py` multi-call and budget cases); no test mirrors the worksheet wording.
- All 14 fixture hashes match the manifest. Relative Markdown links/anchors and whitespace were checked. No other module imports the changed checker or CLI; `loop.py` and fixtures are unchanged, so dependent module suites were not re-run.

Not performed: published-revision CI (record at handoff), Docker checks (no executor code changed), hosted or local model runs, and any learner observation. Whether the messages and exercises help learners is unobserved; collect that under Plan 02.

### Published Plan 14 revision

[PR 27](https://github.com/jschell/sec-lm-learning-track/pull/27) merged as [`d383f223ca21dae62590e4fda8b831f40dd07eac`](https://github.com/jschell/sec-lm-learning-track/commit/d383f223ca21dae62590e4fda8b831f40dd07eac); its tree is identical to the checked PR head `1ddc840`. [Track 1 run 39436193431](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193431) passed offline Python 3.12 and 3.13 (unit tests including the fix-exercise regressions, stage 1/2/3 checks with guards, transfer) and the actual Docker job (`verify_docker.py`). Path-triggered dependent checks also passed: [context 39436193328](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193328), [authority 39436193338](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193338), [output/feedback 39436193616](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193616), [protocol/MCP 39436193427](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193427), [model input 39436193424](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193424) and the [generation contract jobs](https://github.com/jschell/sec-lm-learning-track/actions/runs/39436193539) on 3.12/3.13. That run's separate actual-model job was still running when this was recorded; Plan 14 changed no generation or model code, and it is not claimed as new model evidence.

Plan 14 author implementation is complete. Learner use of the targeted messages and fix exercises remains unobserved; record it in the Plan 02 walkthrough.

## Plan 15: section 1 focus

Author candidate checks 2026-10-20 (UTC), Linux x86_64, CPython 3.12.3, uv 0.12.23 environment, on implementation commit `412ce3a5f88ab33ae4f9204747901744341c9415` (based on main `baa49b3`). [Plan 15](../../docs/plans/active/15-track1-section1-focus.md) follows an AI-subagent review of worksheet section 1; that review is author preparation, not learner evidence.

- A fresh detached worktree with a new uv environment passed 100 Track 1 tests: the previous 95 plus 5 in `test_stage_output.py`. They cover the stage 1/2 summary (request and call counts, no tool-result or final text in stdout), `--json` matching the traced history, `--read missing.txt` giving `is_error: true` for `read-1` in request 2 with a private run-local `read-replay.json` and an unchanged source fixture, `--read notes.txt` succeeding, a `../` path returning an error result through workspace confinement, and rejected `--read` combinations. Existing tests that parse stage output kept passing.
- Core walkthrough in that worktree: stage 1 (one request, one text response), stage 2 (two requests, one completed call, `read-1` proposed and matched), `stage 2 --read missing.txt` (same IDs, `is_error: true`, unchanged final text), `stage 2 --json`, stage 3 (completed, 4 calls), `--scenario multi` (completed, 2 calls) and `--max-calls 1` (`tool_limit`, 0 calls), transfer, the stage 3 guard check and the recording-only guard comparison. `git status` stayed clean; all 14 fixture hashes match the manifest.
- Section 1's checkpoints were compared with that actual viewer output. Relative Markdown links/anchors and whitespace were checked. The pilot objective table in `docs/pilot/alignment-and-review.md` already maps outcome 6 (O4) to core-loop history, so it needed no change; its dated 2026-10-18 command audit is historical and was left as recorded.

Not performed: published-revision CI (record after merge), Docker checks (no executor code changed), model runs and any learner observation. Whether the shorter steps help learners is unobserved; section 1 now waits for Plan 02 evidence.
