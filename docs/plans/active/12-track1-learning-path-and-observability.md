# Plan 12: Make Track 1 clear, observable and trackable

Status: planned; implementation not started. This is one bounded usability pass over existing material, following the owner's review of PR #18. It does not reopen module expansion or claim independent learner validation.

## Outcome and limits

A Python-capable security professional can identify why to take Track 1, follow one recommended route, see the inference → dispatch → feedback mechanism in its trace, and record evidence for each learning objective. Keep complete worked code first, with reconstruction optional, following [decision 0001](../../decisions/0001-worked-stages-first.md).

Reuse the current README, worksheet, lessons and [pilot package](../../pilot/README.md). Do not add another learner guide, progress application, curriculum framework or mandatory model setup. Preserve existing URLs, CLI commands, reference guards and original-source attribution. No new model, hosted call or platform certification is required.

## Verified starting gaps

Reviewed at main `1c2403d8a7da8ade662b66e6a2fd71a8967ce48c`:

- [Track entry](../../../tracks/01-author-the-loop/README.md) has a broad purpose and modes but no explicit learner-facing objective list. Its lesson ordering differs from the worksheet and selected pilot route.
- [Worksheet](../../../tracks/01-author-the-loop/pilot-worksheet.md) captures observations but lacks a compact objective/evidence progress record. Printed traces are temporary, without preservation instructions.
- [Viewer](../../../tracks/01-author-the-loop/lab/inspect_trace.py) now explains authority events, but Stage 2 request/response/history summaries hide tool requests, matching result IDs and feedback input.
- [Entry command](../../../learn.py) routes top-level help to scenario-only help, hiding stage, trace, transfer, check and guards.
- Setup assumes an existing checkout. Platform scope is unclear. The 2–4-hour headline and lesson 1–5 estimates (4–7¼ hours combined) cover different, unspecified activity sets.

These are author observations, not findings from an independent learner session. The original loop progression remains [Geoffrey Huntley's workshop](https://ghuntley.com/agent/); the changes below are project-specific instructional and interface choices.

## 1. Establish the learner contract and one route

Rewrite the entry page's opening around the practical security use: read an agent trace and distinguish a model's proposal, actual code execution, returned evidence and stopping decision. Use a familiarity-first display title; retain the existing directory and lesson links.

State six observable core outcomes near the top:

1. Locate the model response and distinguish a proposed tool call from actual dispatch.
2. Match a call/result ID and locate that feedback in subsequent inference input.
3. Explain repeated feedback after a tool error, separating scripted recovery from model observation.
4. Change a controller budget and explain which operations ran and why the loop stopped.
5. Check the task outcome separately from conversation completion.
6. Distinguish files, conversation history and supplied input, and explain why ordinary tool feedback does not update model weights.

Use these same statements in the worksheet's progress rows; avoid a second competing objective list. Keep pilot IDs O1–O5 stable: O1/O2/O3/O4 overlap core concepts; O5 selection loss belongs to the explicitly named companion. Error recovery and budget variation receive direct worksheet evidence checks rather than a new scored assessment battery. Update the pilot alignment map to expose this distinction; do not renumber forms, retrofit scores or imply every core action has its own pre/post item.

Provide one numbered path: prepare → one-page loop → worksheet sections 1, 2, 4 and 5 → record completion. Link the exact worksheet section anchors and associated lesson references. The worksheet is the step-by-step route; the lesson pages explain those steps. Explain the differing numbering once rather than renumbering existing URLs. The facilitator pilot uses that same core plus the separately labelled selection companion.

Move other activities and modes below a Going further heading. Describe reconstruction, repair/Docker, untrusted-input/guards and local/hosted observation as choices after the core. Do not make missing-guard implementation a new core gate. Give lessons 6 and 8 a short explicit goal using their existing completion expectations; preserve their place as reference/extension material.

## 2. Track evidence in the existing worksheet

Add one table mapping each of the six outcomes to its exercise, evidence location, initial explanation, status and assistance. Use statuses such as not attempted / partial / demonstrated and N/V/H/W assistance as defined in the existing pilot key. An assisted explanation remains labelled assisted. Neither a command exit code nor VERIFIED alone establishes understanding.

Explain how to preserve a run: copy the relevant printed workspace/trace into an ignored local evidence directory before temporary cleanup, record repository revision and link it from the worksheet. Give a small Python/pathlib or shutil example that avoids shell-specific path syntax, preserves raw JSONL and refuses an existing destination. Generated synthetic material stays local; no credentials or client information enter notes. Do not add a persistence service or automatic scoring system.

## 3. Make the exchange visible without inventing events

Extend the existing viewer, leaving JSONL as the authoritative record and preserving proposal/permission/simulation/effect distinctions:

- Response summary: proposed tool name, call ID and bounded arguments, alongside the existing text summary.
- Request summary: inspect nested messages to show matching tool-result ID, error state and bounded result excerpt supplied in that request. Distinguish the newly appended feedback from older repeated history, or explicitly label a cumulative input snapshot; do not count repeated history as new dispatches.
- History summary: identify captured calls/results as history, not independent execution observations.
- For Stage 2, display the chain: proposed read → matching result supplied in request 2 → final response. Its existing result/history is not a standalone tool execution event. Point learners to the actual dispatch statement and returned fixture bytes when verifying the read; do not fabricate an execution event from message presence.

Keep summaries escaped, bounded and readable for multi-call/error cases. Display unknown event names and keep the existing raw-record inspection as a focused follow-up. Do not evaluate trace content or introduce a generic trace-analysis platform.

Add meaningful regressions: Stage 2 call/result IDs and next-input visibility; error feedback; repeated history not portrayed as fresh execution; multiple calls; bounded/untrusted payload rendering; existing authority labels preserved. Prefer existing fixtures and complete worked code over new duplicated traces.

## 4. Fix discovery, setup and estimate scope

- Top-level `learn.py --help` and `-h` list stage, trace, transfer, check and guards, plus the existing scenario route. Keep current invocations working and command-specific help delegated. No wholesale CLI migration is required. Test actual help behavior and one existing scenario invocation.
- Add git clone and change-directory instructions, Git/terminal/Python prerequisites and the official [uv installation reference](https://docs.astral.sh/uv/getting-started/installation/). Keep Python 3.12+ and the [uv frozen project workflow](https://docs.astral.sh/uv/guides/projects/).
- Label tested OS/shell environments from the validation record. Explain that printed temporary paths vary by OS; never require a literal /tmp path. Offer Windows/WSL guidance with an explicit tested/untested distinction. Do not imply uv's platform availability proves this repository works on that platform.
- Separate setup time, core familiarity and additional exercises. Reconcile each lesson estimate with the activities it includes, particularly reconstruction/Docker. Keep estimates explicitly provisional until learner timings exist; do not substitute an unsupported three-hour promise.

## 5. Verify, hand off and stop

From a fresh checkout/new uv environment with existing host prerequisites recorded, follow the revised entry instructions and required route without model/server/credentials/Docker. Exercise top-level/command help, Stage 2 viewer, error feedback, budget variation, supplied transfer and evidence preservation. Verify copied raw trace contents against the originals. Inspect the displayed chain against raw JSONL and the actual dispatch implementation.

Run relevant Track 1 tests and required existing CI checks. Run context tests only if companion behavior changes; no broad model benchmark is needed for documentation/help/viewer edits. Validate changed Markdown links, section anchors, source coverage and git diff whitespace. Record actual commands, environment, results and limits in the existing [Track 1 validation record](../../../tracks/01-author-the-loop/VALIDATION.md); do not fabricate learner/platform observations.

Keep the [pilot protocol](../../pilot/README.md), objective alignment, session record and Plan 02 consistent with the same route. Plan 11 remains completed preparation; Plan 02 stays open for independent human review, actual responses and delayed follow-up. End this pass after the acceptance checks below. New modules remain paused until the first learner walkthrough informs the next decision.

## Acceptance

- [ ] Entry page states practical purpose, six observable core outcomes, prerequisites and one required route before additional modes.
- [ ] Worksheet maps outcomes to evidence, explanation, assistance and progress; preservation instructions work without a hard-coded OS path.
- [ ] Stage 2 viewer reveals the call/result/next-input chain without claiming history proves execution; repeated input and authority events remain distinct.
- [ ] Top-level help exposes existing commands; old commands and command-specific help still work.
- [ ] Clone/setup/platform guidance and scoped provisional estimates are consistent; lessons 6/8 state goals.
- [ ] Relevant regressions, fresh-environment route, evidence copy and changed links pass; actual limits are recorded.
- [ ] Pilot materials retain stable objective IDs and the companion boundary; no historical grades or missing human observations are relabelled.

## Sources and decision boundaries

Original sources opened 2026-10-17 (America/Los_Angeles): Geoffrey Huntley, *how to build a coding agent: free workshop* (24 Aug 2025), supports the chat/tool-feedback progression; Astral's official uv installation and project workflow pages support setup references. Links appear beside their uses above. Existing lesson protocol citations remain authoritative for message formats. Route, objective wording, viewer design, tracking choices and estimates are original project recommendations; they are not upstream requirements or evidence of validated learning effectiveness.
