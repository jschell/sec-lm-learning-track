# Track 1 validation

Updated 2026-10-20 UTC (2026-10-19 America/Los_Angeles). This is the authoritative current Track 1 check summary. Implementation tests, actual model observations, and independent learner usability are separate claims.

## Current status

Target Python 3.12+, default 3.12; uv 0.12.23. Prior author handoff check: Linux x86_64, CPython 3.12.15 in a new virtual environment; earlier implementation checks used 3.12.14. No hosted-provider credentials or local Docker execution were used in this desk check. [Commands, findings and scope](../../docs/validation/2026-10-17-learner-handoff.md).

| Check | Observed result |
| --- | --- |
| Standard-library functional suite through frozen/offline uv | **79 tests passed locally** |
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
| Actual Docker FAIL→edit→PASS and execution controls | Passed in hosted CI for the previously verified implementation; no local Docker run |
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
