# Plan 11: Pilot preparation and quality review

Status: approved scope for planning; implementation not started. This plan prepares assessment and instructional quality checks. It does not mark a learner pilot, independent expert review or pedagogical validation as performed.

## Outcome and scope

Produce one pilot-ready package for Python-capable security professionals: the **Track 1 core** plus **Context and state, Lesson 2: Select evidence**. Use the complete worked code. Reconstruction, optional guard extensions, Docker execution, model installation and hosted calls are outside the required pilot route. Keep their existing optional routes available.

The companion is a single 20–40-minute unit, not the whole three-lesson module; this is a project scope choice to limit burden while testing application of the context/input distinction. Track 1's core route must explicitly select request/exchange stages, repeated feedback, a finite stop and the supplied read-only transfer exercise from the existing worksheet. Record actual setup/learning times separately; estimates are not deadlines. Sessions may be split with the break recorded.

Pause new modules and application expansion until this bounded preparation pass and an initial learner walkthrough have informed the next decision. In-scope documentation, correctness and usability fixes may proceed. Pi and hosted-provider checks retain their existing plans; they do not become prerequisites for this offline pilot.

## Assessment foundation

Connect intended understanding, observable tasks and interpretation criteria, following the National Research Council's [assessment foundations](https://www.nationalacademies.org/read/10019/chapter/3). Use a performance-based baseline, rather than learner confidence alone, informed by [CMU's prior-knowledge assessment guidance](https://www.cmu.edu/teaching/assessment/priorknowledge/performancebased.html).

Worked examples followed by problems and explanatory questions are supported in the [IES practice guide](https://ies.ed.gov/ncee/wwc/PracticeGuide/1). Assess application to a changed situation using the National Research Council's [learning and transfer discussion](https://www.nationalacademies.org/read/9853/chapter/6). These sources inform the procedure; their findings do not validate this repository, its custom questions or effectiveness for adult security professionals. Timing, sample size, rubric and release criteria below are project decisions.

## Implementation sequence

### 1. Freeze a bounded route and audit alignment

- Record repository revision and exact required pages/commands. Reuse the [Track 1 worksheet](../../../tracks/01-author-the-loop/pilot-worksheet.md) and [selection lesson](../../../modules/context-and-state/02-select-evidence.md); do not build a parallel curriculum.
- Map each objective to one explanation, worked example, learner action and assessment item. Identify prerequisites, terminology and likely misconceptions. Do not assess optional material as required knowledge.
- Use these initial objectives: locate inference versus dispatch; trace matching feedback into the next request; distinguish completion from task correctness; distinguish saved files from supplied input; detect relevant evidence omitted by selection.
- Give an operational example for each misconception, such as “a tool request itself read the file,” “completed means correct,” or “a fact on disk is automatically in context.”

### 2. Perform a focused editorial and mechanical pass

- Read the selected route as a new user: remove unexplained vocabulary, circular navigation, duplicate explanations and contributor-process text. Keep a short local statement of what an exercise shows; move repeated validation history to existing validation records. Preserve original-source citations and honest limits.
- Fix the shared trace viewer's missing detail for `decision`, `effect`, `proposal` and recording-only decisions. It currently prints event names; improve useful summaries without treating decisions as executed effects or executing trace content. Raw JSONL remains authoritative.
- Clarify “offline after preparation” for downloaded tokenizer assets. Describe 360M/example as observed successes and retained failures, rather than dependable operation. Say feedback was **supplied in input**, not that trace checks prove semantic use. Preserve historical failures, exact task criteria and source provenance.
- Resolve the CI-wording ambiguity from [decision 0002](../../decisions/0002-feedback-integration-and-model-outcomes.md): distinguish changed integration requirements from unchanged exact-answer grades beside the claim. Do not silently revise the historical decision or relabel failed tasks.
- Exercise each required command from a fresh checkout and newly created uv environment, with Python 3.12 and no model/server/credentials. Record existing OS prerequisites; this is not a fresh-OS or Pi validation. Validate changed Markdown links and run only relevant tests. Add meaningful viewer regressions for denied/recorded versus executed events.

### 3. Prepare parallel assessment and transfer materials

- Author short forms A and B covering the same objectives with different values/traces. Aim for about 10 minutes before and 15 minutes after instruction. Include prediction, diagnosis and explanation, not only terminology or command recall.
- Provide all tool contracts and unfamiliar scenario facts. Use a supplied synthetic event-lookup trace for a 10–15-minute transfer exercise; require no SIEM knowledge, new API implementation or additional dependency.
- Do not reuse worked examples or the already-public transfer solution as an independent post-assessment. Check form comparability with an expert; do not claim psychometric equivalence. Alternate A/B order across learners when feasible and record order.
- Prepare a short delayed form C for roughly 3–7 days later, with no lesson/answer key during the check. The interval is a project choice. A missing delayed check remains missing, not a retention pass.
- Distinguish instruction, assessment and feedback. Record pre/post responses before giving corrections. Separate the keys from learner navigation and have the facilitator distribute them after checks; a public repository cannot guarantee that learners have not seen answers. Record prior exposure.

### 4. Define scoring and reviewer checks before observing learners

- Score each objective using anchored examples: 0 incorrect/missing, 1 partially correct, 2 correct with a sound mechanism/evidence explanation. Accept equivalent explanations; verbosity and memorized wording are not goals.
- Record assistance separately: none, navigation clarification, conceptual hint or worked explanation. Never describe an assisted answer as independent performance. Keep setup problems separate from conceptual errors.
- Prepare correct, partial and plausible-wrong sample responses. Ask a second human subject expert to score a sample without seeing the author's scores, then reconcile disagreements and clarify the rubric. Log reviewer role/date and unresolved ambiguity. Author/AI desk review does not satisfy this independent review.
- Predeclare decisions: fix a technical blocker before the pilot; revise an item if its key or contract is ambiguous; use actual learner misconceptions and assistance to prioritize later edits. Report per-objective results, not an arbitrary total-score certification. A small pre/post pilot cannot establish causal superiority over another teaching method.

### 5. Package the handoff and stop

Keep reusable materials together in `docs/pilot/`, targeting five concise Markdown files: route/protocol, alignment/review record, assessment forms, facilitator key/rubric, and blank session record. Reuse existing fixtures/pages and small labelled trace extracts; add only necessary held-out fixtures. Do not add an LMS, grading platform, model judge or another agent framework.

The session record includes anonymous learner ID, prior experience/exposure, revision, selected route, form order, actual time, setup issues, responses, per-objective scores, assistance, reviewer notes and unresolved questions. Keep credentials/customer data out. Do not prefill a simulated learner's results.

Update [Plan 02](02-track1-pilot.md), the existing checklist and plan index to point to the package. Independent expert review can be logged as pending if no reviewer is available; distinguish **author-prepared**, **independently reviewed**, and **learner-piloted**. End preparation when artifacts and author checks are complete. Do not keep polishing every module while waiting for learners.

## Acceptance checklist

- [ ] Bounded route and objective/evidence map recorded; optional material clearly excluded from assessment.
- [ ] Focused editorial fixes, viewer details and setup/capability wording implemented without changing task criteria or removing failure evidence.
- [ ] Required commands, relevant code tests and links checked; environment and limitations recorded.
- [ ] Forms A/B, unfamiliar transfer and delayed C supplied with separate facilitator key and explicit exposure rules.
- [ ] Scoring anchors, assistance categories and representative sample responses defined before the pilot.
- [ ] Independent human review procedure and record supplied; actual review status reported honestly.
- [ ] Compact reusable package linked from existing pilot materials; no duplicate instructional sequence or platform added.
- [ ] Author preparation status recorded separately from pending learner, retention, hardware and provider evidence.

## Subsequent work requiring people or observations

Plan 02 conducts the learner walkthrough and records before/after/transfer responses; delayed follow-up measures retention. Fix observed blockers, then decide whether to expand testing or revise instruction. Independent expert scoring needs a real second reviewer. Neither green CI nor an AI role-play completes these checks. Live injection observations and harder argument-manipulation exercises remain separate candidates, not part of this preparation implementation.

## Original sources

Sources opened 2026-10-17 (America/Los_Angeles): NRC, *Knowing What Students Know* (2001), assessment foundations; CMU Eberly Center, performance-based prior knowledge assessments; IES, *Organizing Instruction and Study to Improve Student Learning*; NRC, *How People Learn* (2000), learning/transfer. Direct links beside their supported concepts above. Scope, artifacts, scoring anchors and timing are original project recommendations, not a standardized or validated instrument.
