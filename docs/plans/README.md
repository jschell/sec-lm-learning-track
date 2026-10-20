# Implementation sequence

Implementation readiness and validation are separate. Independent learner, hosted-provider and physical Pi checks remain open in their existing records. New modules are currently paused until the initial learner walkthrough informs the next decision; hardware/provider availability does not block that work. Merge confirmation means verify checks and continue to the next ready authorized plan.

## Implemented: review fixes and CI hygiene

[Plan 16](active/16-track1-review-fixes.md), requested by the owner on 2026-10-20, fixes the findings of an author-side review of Track 1 tests, CI and validation claims: a duplicate-ID check in the worked code, stale or inaccurate documentation, consistent command output, two learner-text spoilers, test gaps, and CI timeouts, concurrency and immutable action/image pins. Implemented in a reviewable change; published-revision checks follow merge. Section 1 stays frozen. After it, Track 1 tuning stops in favour of Plan 02's human evidence.

## Implemented: focus worksheet section 1

[Plan 15](complete/15-track1-section1-focus.md), requested by the owner on 2026-10-20 and merged in PR 30, splits Track 1 worksheet section 1 into short single-idea steps, stops `learn.py stage` output from revealing the answer before inspection, adds a one-command missing-file variation, and moves the weights note and account-disable question to the recap and completion steps. Published-revision checks passed. After it, section 1 revisions wait for Plan 02 learner evidence.

## Targeted feedback and fix exercises implemented

[Plan 14](complete/14-track1-targeted-feedback-and-fix-exercises.md), requested by the owner on 2026-10-20 and merged in PR 27, adds targeted checker diagnoses for common wrong exchange/loop implementations and three optional `learn.py fix` exercises beside Track 1 sections 1 and 2. The core route, outcomes, worksheet numbering and pilot items are unchanged. It does not reopen module expansion or substitute for Plan 02's human evidence.

## Next implementation: first-attempt corrections

[Plan 13](complete/13-track1-feedback-corrections.md) A–C are merged; D/E author implementation and published-revision Docker/dependent checks passed in PR 25. Human review and learner evidence remain under Plan 02. Correct credential/error handling, consolidate learner artifacts in ignored repo-local run directories, repair viewer/checker usability, improve one existing self-directed activity, and validate advertised protections/shared CI dependencies. This bounded correction precedes the next walkthrough; it does not reopen module expansion or mark learner validation complete.

## Track 1 usability implemented

[Plan 12: Learning path and observability](complete/12-track1-learning-path-and-observability.md) is implemented: the entry page states six outcomes and one core route; the worksheet records progress/evidence; the viewer exposes cumulative call/result input; CLI help and setup/platform/estimate guidance are clarified. Fresh-environment author checks are recorded in Track 1 validation. Independent expert review and the learner pilot remain the next evidence work below; no further module implementation is queued.

## Next evidence: independent review and learner pilot

[Plan 11: Pilot preparation and quality review](complete/11-pilot-preparation-and-quality-review.md) is implemented. [The author-prepared package](../pilot/README.md) supplies a bounded route, alignment audit, before/after/transfer/delayed checks, scoring key and blank records. Required commands and relevant tests passed in a fresh worktree/environment; named viewer/setup/capability wording gaps are addressed. Independent human expert review, learner performance and retention remain pending. Pause new modules until the first walkthrough informs the next decision.

[Plan 02](active/02-track1-pilot.md) remains responsible for actual learner observations and resulting fixes. No author/AI check substitutes for that evidence. Existing hardware/provider validation stays separate.

## Existing material and validation

| Plan | Implementation | Outstanding evidence |
| --- | --- | --- |
| [01: Huntley loop](complete/01-harness-lessons.md) | Complete worked stages and worksheet | [Independent learner pilot](active/02-track1-pilot.md); hosted observations |
| [03: Messages and model input](complete/03-messages-and-model-input.md) | Tokenizer/template lab and state companion implemented | Independent learner understanding |
| [04: Generation and sampling](active/04-generation-and-sampling.md) | CPU setup and generation/sampling lab implemented | Model suitability limits, physical Pi resources/setup, learner observations |
| [06: Local tool feedback](active/06-local-tool-feedback.md) | Explicit model/prompt comparison and feedback lab implemented | Physical Pi and learner explanation; exact task failures remain visible |
| [07: Context and state](complete/07-context-and-state.md) | Three offline inspection lessons implemented | Independent learner explanation/transfer; no model or Pi claim |
| [08: Tool interfaces and protocols](complete/08-tool-interfaces-and-protocols.md) | Direct calls and real local MCP exchange implemented | Independent learner explanation/transfer; no model or Pi claim |
| [09: Output validation and uncertainty](complete/09-output-validation-and-uncertainty.md) | Recorded-outcome inspection and claim-review lessons implemented | Independent learner judgment/revision; no fresh inference claim |
| [10: Untrusted input and authority](complete/10-untrusted-input-and-authority.md) | Offline data-flow, policy comparison and denial-feedback lessons implemented | Independent learner explanation; no real-model susceptibility claim |

The modules' validation records are authoritative for observations. An active validation plan does not mean its implementation must be rebuilt.

## Additional mechanics tracks

These are bounded learning units, not a mandatory sequence. Implementation status is explicit; queued plans are not runnable lessons. Estimated effort is a project planning judgment, excluding first-time runtime setup.

| Order | Plan | Readiness | Learner session |
| --- | --- | --- | --- |
| 1 | [07: Context and state](complete/07-context-and-state.md) | Implemented; independent learner check open | Three 20–40-minute modules |
| 2 | [08: Tool interfaces and protocols](complete/08-tool-interfaces-and-protocols.md) | Implemented; independent learner check open | Two 30–45-minute modules |
| 3 | [09: Output validation and uncertainty](complete/09-output-validation-and-uncertainty.md) | Implemented; independent learner check open | Two 30–45-minute modules |
| 4 | [10: Untrusted input and execution authority](complete/10-untrusted-input-and-authority.md) | Implemented; independent learner check open | Two 30–45-minute modules |

Order supports authoring and reuse; supplied starting snapshots keep each track independently usable. Plans 07–10 now have runnable implementations. Remaining work is to collect independent learner observations, perform the already specified hardware/provider checks, and correct observed blockers. No additional mechanics track is queued; Plan 11 has prepared the existing-material pilot package. Keep each bounded change reviewable; select any further track for a concrete learning question before adding machinery.

[05: Consulting applications](queue/05-consulting-applications.md) remains deferred. Existing Tracks 2–5 contribute concepts to the mechanics plans; engagement management, client integrations and Track 6 delivery remain later applications. Preserve existing track URLs and use their outlines as navigation pointers rather than creating duplicate lessons.

[Design maintenance](active/00-curriculum-design.md) follows the [current design](../design.md). Original foundations and attribution are in each plan and the [source register](../../reference/sources.md).
