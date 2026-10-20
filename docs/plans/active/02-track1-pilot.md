# Plan 02: Pilot Track 1

Status: bounded assessment package and author desk check prepared; independent learner walkthrough and hosted-model observation remain unperformed. A separate local model/prompt configuration has been observed; it does not complete the learner pilot.

## Preparation dependency

Use the author-prepared [pilot package](../../pilot/README.md), implemented by [Plan 11](../complete/11-pilot-preparation-and-quality-review.md): Track 1 core plus one evidence-selection companion, aligned assessment forms and scoring/assistance guidance. Reuse this plan's existing worksheet/checklist. Preparation, independent expert review, learner performance and delayed retention are separate evidence states; do not mark this pilot complete when the package is ready.

[Plan 12](../complete/12-track1-learning-path-and-observability.md) has consolidated the learner route and fixed exchange visibility/help. Use its six-outcome worksheet progress record alongside the stable pilot forms; author verification does not replace this plan's human observations.

[Plan 13](../complete/13-track1-feedback-corrections.md) addresses the owner's first-attempt technical feedback before the next walkthrough. Stages A–C now cover credential handling, artifact location and viewer/checker corrections; D/E author implementation and published-revision Docker/dependent checks passed in PR 25. Use the revised exchange activity and record its revision in the next actual learner session. Screenshots of tool-assisted review are readiness evidence, not a substitute for original learner responses/timing. Keep that distinction in the session record.

A 2026-10-20 navigation pass makes the worksheet the single core spine: each core page ends with a Next-in-core link, sections 3 and 6 carry optional banners, and [the one-page loop](../../../tracks/01-author-the-loop/core-loop.md) moves from the first step to a recap after section 2. Section numbers, anchors and assessment items are unchanged. Record the navigation revision alongside the Plan 13 D instruction revision; it is author preparation, not learner evidence.

[Plan 14](../complete/14-track1-targeted-feedback-and-fix-exercises.md) adds targeted checker messages, stated choices for the section 4 prediction and optional `learn.py fix` practice. The fix exercises are outside the pilot assessment. Record the Plan 14 feedback revision in the session record, and note whether the learner used the optional exercises or saw a targeted message.

[Plan 15](../complete/15-track1-section1-focus.md) plans a focused rewrite of worksheet section 1 from an AI-subagent review. That review is author preparation, not learner evidence. Plan 15 is implemented before the walkthrough: record the worksheet's "Section 1 revision" line in the session record, and note whether the learner opened the collapsible checkpoints. Further section 1 changes wait for this plan's learner observations.

[Plan 16](16-track1-review-fixes.md) plans fixes from an AI-subagent review of tests, CI and validation claims. It is implemented before the walkthrough and leaves section 1 unchanged; record the worksheet's "Review-fix revision" line in the session record. After it, Track 1 tuning stops and this plan's human evidence comes next.

## Work and acceptance

Use [the pilot checklist](../../../tracks/01-author-the-loop/pilot-checklist.md) and [learner worksheet](../../../tracks/01-author-the-loop/pilot-worksheet.md). Use the package's selected route and separate baseline/post/transfer/delayed forms; record fresh-learner setup, clarifications, time, original responses, per-objective scores and assistance. Independent reviewer scoring remains pending. Correct instruction blockers. For optional model observations, choose local CPU or hosted read-only explicitly; record its setup and unsupported behavior. Keep API credentials out of evidence. The [author desk check](../../validation/2026-10-17-learner-handoff.md) records command/navigation verification, not an independent pilot.

- [x] Complete worked code and a fillable run/inspect/explain worksheet.
- [x] Link the observed local-model route without requiring a hosted key.
- [x] Clarify full-trace inspection, Stage 2 history and deliberate stop statuses.
- [x] Bounded pilot protocol, aligned forms, scoring anchors and blank review/session records authored.
- [ ] Independent human reviewer checks items and scores the supplied calibration sample.
- [ ] Independent learner completes the selected worksheet route; record help, time and demonstrated understanding.
- [ ] Correct blockers revealed by that learner and record their resolution.
- [ ] Perform/record hosted-provider experiments when credentials are available; local results are separate evidence.

Automated CLI/controller checks support implementation confidence but do not satisfy the independent-learner check. New modules remain paused until the initial walkthrough informs the next decision; do not invent a completed pilot.

## Original source

[Huntley's loop workshop](https://ghuntley.com/agent/) is the teaching starting point. Pilot method and acceptance criteria are original project design.
