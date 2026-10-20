# Plan 13: Correct Track 1 reliability and self-directed learning gaps

Status: A–C merged; D implemented and author-checked; E implemented, awaiting expanded actual Docker CI and published-revision verification. [B/C checks](../../../tracks/01-author-the-loop/VALIDATION.md#plan-13-bc-retained-runs-and-learner-diagnostics) include a fresh-worktree walkthrough. [Stage A author checks](../../../tracks/01-author-the-loop/VALIDATION.md#plan-13-stage-a-credential-and-failure-boundaries) are recorded; merge verification remains part of the handoff. Owner requested this corrective plan on 2026-10-19 (America/Los_Angeles). It covers the first-attempt technical feedback and the explicit requirement to keep exercise output together in ignored repository-local directories. It does not claim an independent learner pilot has been completed.

## Outcome and boundaries

A learner follows the existing Track 1 core, keeps all exercise artifacts in one predictable place, receives actionable feedback for common mistakes, and can distinguish a proposed action, an execution record, supplied feedback and independently checked outcomes. Existing advertised execution protections receive meaningful checks.

Retain Python 3.12+, uv, Markdown-first lessons, complete worked examples before optional reconstruction, and the existing six core outcomes. Preserve [decision 0001](../../decisions/0001-worked-stages-first.md), the optional missing-guard learning objective and [decision 0002](../../decisions/0002-feedback-integration-and-model-outcomes.md). Keep wiring checks separate from final-answer grades. Do not add a browser runtime, grading platform, framework, new module or engagement integration.

## Evidence to carry forward

Baseline: main `ff8129f69556743614c30f1f4e11f43e004e1e41`. The owner's screenshots contain reviewer observations and suggested fixes, not a full learner response/timing record.

Locally reproduced without real credentials/network calls: a malformed synthetic credential enters an error trace; passing a directory to the viewer raises IsADirectoryError; the budget viewer prints only tool_limit; Stage 2 rejects a valid exchange that also returns the final assistant message. Inspection also shows the credential-isolation check has no seeded host secret and the Docker suite does not directly assert several advertised protections. Do not present the reviewer's broader mutation/platform claims as independently reproduced.

Treat these as correctness/readiness findings. Learner understanding, actual assistance and retention remain separate under [Plan 02](02-track1-pilot.md).

## Stage A — Credential handling and truthful failure records

- In the hosted adapter, normalize permitted surrounding whitespace, reject empty/malformed header credentials before use, and avoid raw credential-bearing exception messages. Sanitization must cover both the adapter and terminal logging boundary; stripping a trailing carriage return alone is insufficient.
- Preserve useful provider/error categories without recording raw authentication headers or exception bodies. Check trace files, stdout/stderr and chained exceptions using synthetic keys, including CR/LF, whitespace-only values and local header-validation failures. No real key or hosted call is needed.
- Review dispatch accounting in the guarded reference: a dispatch can return before trace writing fails, or raise after an effect. Distinguish confirmed completed calls from attempts/uncertain outcomes. Never label an uncertain effect as zero/no execution. Preserve existing normal-run tool_calls contracts where meaningful; document failure semantics explicitly rather than silently changing the count definition.
- Give the short worked stages bounded, useful handling for malformed responses and failures. Keep their teaching control flow visible; do not copy the whole guarded harness into them or turn optional guard checks into a core requirement. Limit live use to a suitably controlled path or clearly reject unsupported live-stage behavior.

Acceptance: synthetic credential values cannot be recovered from captured diagnostics/traces; regressions cover post-dispatch trace failure and uncertain dispatch outcomes; short-stage errors produce actionable status/trace information without hiding possible effects.

## Stage B — One ignored repository-local run location

Normal learner commands, including stages, scenarios, transfer and the recording-only guard comparison, create unique runs under:

```text
.cache/exercises/track-1/<exercise>/<run-id>/
    work/          # when the exercise uses files
    trace.jsonl
    result.json
```

- Resolve the root from the repository/code location, not the shell's current directory. Reuse a small shared run-directory helper with exclusive creation; concurrent/repeated invocations must not collide or overwrite earlier runs. Reject unsafe exercise/path components and avoid following a substituted output-root symlink.
- Copy supplied fixtures into work/; never edit source fixtures. Use restrictive permissions for run roots/traces and scope Docker-compatible writable permissions to the actual mounted work area. Do not make replay-only workspaces world-writable. Recording-only comparisons may use labelled subdirectories for each controller/case.
- Every command prints its run directory and trace/summary paths. Summaries distinguish mode, completion/error, confirmed call counts and uncertainty. If setup or trace writing fails, report the failure without fabricating a complete record. Never put credentials in a summary.
- Keep the existing .cache ignore rule; confirm git status excludes all generated artifacts. Replace learner tempfile output and manual .cache/evidence copying with direct retained runs. Test internals may still use temporary isolated directories; unrelated modules retain their own explicit output contracts.
- Document retention and explicit manual cleanup of a chosen run/subtree. Do not add automatic deletion, age-based eviction or a cleanup service. Users can copy/archive runs when desired, but copying is no longer required for normal completion.

Acceptance: running from the repo and another working directory places learner artifacts in the same repo-local root; repeat runs preserve earlier bytes; fixtures stay unchanged; generated files are ignored; no learner run is scattered into /tmp. The worksheet records the printed run path directly.

## Stage C — Viewer, checker and learner error handling

- Accept either a run directory or a trace file. Handle missing/empty files, blank lines, invalid JSON, absent required fields and a truncated final line with useful path/line diagnostics. Show readable valid records when possible and label incomplete/malformed traces; do not claim completion merely because the CLI could read part of a file. Account for Stage 1/2 ending with response/history rather than a stop event.
- Display configured max_calls/max_turns and actual/uncertain call counts beside stop status. Make newly supplied feedback stand out from repeated history. Retain access to a clearly labelled cumulative view; recognize divergent histories without guessing a fresh dispatch from message presence. Preserve bounded escaping and permission/simulation/effect distinctions.
- Relax Stage 2's returned-history bookkeeping to accept both the complete feedback history and that history plus its actual final response, while still rejecting missing/fabricated feedback. Give precise expected/observed errors; do not say a result is missing when only final-message convention differs.
- Replace common learner tracebacks with actionable errors for bad replay/loop paths, syntax/import failures, missing edit keys and wrong working-directory assumptions. Retain a trace path when one exists. Keep synthetic controller policy consistent with the operations actually exposed; read-only scenario instructions must not coexist with enabled edit operations unintentionally.

Acceptance: directory/file viewing, budget display, malformed/incomplete traces, both valid Stage 2 history shapes and common learner mistakes have meaningful regressions. Existing commands and narrow core/optional-guard checks remain usable.

## Stage D — Improve one existing learning activity and align documentation

Prototype the self-directed pattern in the existing one-tool-exchange activity, not a new guide:

1. State one observable objective and prerequisite.
2. Present a fresh prediction before its answer is visible; keep the complete worked code available.
3. Run, locate the specific dispatch/result/next-request evidence, then change one factor using the existing missing-file variation.
4. Offer collapsible hints: where to look → relevant field/relationship → annotated explanation.
5. Close with key points and a changed-case explanation question. Mark automated mechanical checks separately from interpretive self-checks.

- Fix stale viewer instructions, conflicting first-code-reading directions, lesson footers leading away from the core, inaccurate supporting links and missing repo-root notes. Keep existing URLs/anchors stable; no broad renumbering.
- Replace manual trace preservation with the Stage B run location. Keep administrative/pilot details out of the immediate exercise flow where possible without creating a duplicate worksheet.
- Keep the existing authored 999-line diagnosis honestly labelled. It need not become a new CLI feature. Separate request-content observation from the architectural weights explanation; replay cannot measure weights. For the account-disable example, ask what independent read-back would verify the resulting account state.
- Preserve pilot IDs, held-out forms and original responses/grades. If instructional wording changes, record its revision; do not retroactively count a prior result as a pass.

Acceptance: the activity has a prediction, real operation, bounded variation, specific feedback, hint ladder and close-out; self-check answers are available without a facilitator and distinguish mechanics from explanation. Existing core/companion boundaries remain explicit.

## Stage E — Check advertised protections and repair validation coverage

- In actual Docker integration, seed synthetic host values for both configured provider credentials, then assert neither variable/value reaches the executor. Scope environment changes to the test and never use real secrets.
- Assert effective non-root identity, NoNewPrivs, dropped capabilities, read-only root/grader, network isolation and tmpfs options including noexec, matching the protections already advertised. Inspect runtime configuration where necessary and use bounded behavioral checks where reliable. Removing a targeted protection must make its relevant check fail; avoid relying only on an asserted command string.
- Add focused regressions for high-value missed cases such as cross-turn duplicate IDs, extra tool arguments, path/symlink confinement and trace creation/permissions. Reproduce candidate mutations before claiming coverage; do not launch a general mutation-testing project.
- Audit CI path filters for modules importing shared Track 1 code. Changes to a shared dependency must trigger the dependent suites. Do not require model downloads for every Markdown edit; retain explicit boundaries for genuine model checks.
- In the existing validation record, separate the exact revision checked, local author runs, current CI, historical Docker evidence and pending learner/hardware/provider observations. Describe fresh-worktree candidate runs as pre-commit checks, then verify the published commit/merge so readers have a reproducible revision. Correct source links beside the supported claim, including stop-reason/max_tokens guidance.

Acceptance: targeted tests catch removal of the advertised protections; dependent offline suites run when shared code changes; validation links identify actual revisions/runs and state what was not tested. Docker availability failures must not be recorded as successful validation.

## Delivery and completion

Implement in the sequence above, using reviewable PRs: A first; B/C together where run paths and viewing must change atomically; D; then E. Carry only necessary navigation/validation updates in each PR. No separate plan is required for each stage. On merge confirmation, verify checks and continue to the next authorized stage.

Use a fresh checkout/new uv environment for the final core walkthrough: stage 1/2/3, viewer, error variation, budget variation, supplied transfer and directory retention. Run relevant standard-library tests through frozen/offline uv, actual Docker checks when available and dependent module suites affected by shared changes. Check relative Markdown links, fixture hashes, artifact ignore rules and whitespace. Keep synthetic failure probes isolated. Record all unperformed checks explicitly.

Complete author implementation when Stages A–E acceptance conditions are met and published-revision checks are recorded. Then resume Plan 02's real learner walkthrough with the revised activity; collect original explanations, help, setup friction, timing and the existing delayed follow-up. New modules remain paused. A green suite, heading/schema check or AI role-play does not complete learner validation.

## Implementation checkpoints

- [x] A: credential handling and truthful failure records implemented and author-checked; published/merge CI tracked in the PR.
- [x] B: all normal learner runs retained under the ignored repo-local root; exclusive/private allocation and retention checked.
- [x] C: viewer, checker contracts and common learner errors corrected; malformed/incomplete traces and valid history variants checked.
- [x] D: one existing activity improved and navigation/evidence wording aligned.
- [ ] E: advertised protections, dependent CI and reproducible validation verified.

## Original patterns and sources

These are original project recommendations. Preserve Huntley's [inference/tool-feedback progression](https://ghuntley.com/agent/) and local [source record](../../../tracks/01-author-the-loop/SOURCES.md); do not copy upstream code. The authoring approach uses [Exercism's concept-exercise design/hints](https://exercism.org/docs/building/tracks/concept-exercises) to control scope and offer specific assistance, [The Carpentries' episode structure](https://carpentries.github.io/sandpaper-docs/episodes.html) for questions/objectives/key points, and [futurecoder's graduated assistance](https://github.com/alexmojaki/futurecoder) as a pattern rather than a platform dependency. Exercism, Carpentries and futurecoder sources opened 2026-10-19 (America/Los_Angeles); Huntley attribution/provenance remains in the existing source record. They do not validate this curriculum or establish a fixed effect size for security professionals.

Implementation must recheck official [Python tempfile](https://docs.python.org/3.12/library/tempfile.html), [Python HTTP client](https://docs.python.org/3.12/library/http.client.html) and [Docker run](https://docs.docker.com/engine/containers/run/) behavior before relying on particular APIs/options. These are implementation references to verify, not claims of tests already performed.
