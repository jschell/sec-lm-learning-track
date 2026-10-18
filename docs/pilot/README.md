# Pilot: the loop plus evidence selection

Status: author-prepared; independent expert review, learner pilot and retention follow-up pending. Use this route for the first structured pilot. This is a research-informed procedure, not a validated assessment instrument.

Audience: a security professional comfortable with Python lists/dictionaries who did not author these lessons. Supply the complete worked code. No model, API key, Docker or tokenizer download is required.

## Facilitator protocol

Record the repository revision and any uncommitted changes in a copy of `session-record.md`. Set up the environment first, then administer the baseline **before** the learner reads the conceptual pages. Log setup assistance separately. Use [Track 1 preparation](../../tracks/01-author-the-loop/README.md#prepare-once):

```bash
uv python install 3.12
uv sync --frozen
```

Initial interpreter/environment preparation may use the network; the required learning commands below run offline. Every `learn.py` invocation creates fresh temporary files. The context commands need new output directories.

| Phase | What to provide | Record |
| --- | --- | --- |
| Baseline, about 10 min | Only assigned Form A or B from `assessment-forms.md` | Original answers, prior exposure, assistance |
| Instruction | Required route below and existing worksheet | Predictions, actual time, setup versus conceptual blockers |
| Immediate check, about 15 min | The other form, without lessons or key | Original answers before corrections |
| Transfer, 10–15 min | Only the unfamiliar event-lookup case | Answers and help; do not substitute the public worked transfer |
| Feedback | Discuss answers after the immediate and transfer responses are captured | Feedback supplied and time |
| Delayed check, 3–7 days later, about 10 min | Form C, without lessons or key | Actual interval, practice since lesson, answers/help, or not attempted |

Timing and sequence are project choices. Learning can span sessions; record breaks and outside practice. If feasible alternate A→B and B→A across learners. The forms target the same objectives but have not been demonstrated equivalent. One participant gives formative evidence, not comparative efficacy or a population success rate.

Distribute only the assigned form as a copy. Keep the facilitator key and worked example answers out of the assessment handout; the public repository cannot enforce secrecy. Ask about previous exposure and record it. Do not treat exposed answers as independent performance. During checks, capture the first response before hints, then log any assistance and revised response. No need to withhold explanations during instruction.

## Required learning route

Follow [the Track 1 core route](../../tracks/01-author-the-loop/README.md#one-core-route), including its six-outcome worksheet progress record. Read [the one-page loop](../../tracks/01-author-the-loop/core-loop.md), then use **sections 1, 2, 4 and 5** of the [existing worksheet](../../tracks/01-author-the-loop/pilot-worksheet.md). Run and inspect these commands, predicting the variation before running it:

```bash
uv run --frozen --offline python learn.py stage 1
uv run --frozen --offline python learn.py stage 2
uv run --frozen --offline python learn.py trace TRACE_PATH
uv run --frozen --offline python learn.py stage 3
uv run --frozen --offline python learn.py --scenario multi
uv run --frozen --offline python learn.py --scenario multi --max-calls 1
uv run --frozen --offline python learn.py transfer
```

Replace `TRACE_PATH` with the Stage 2 path printed by your run. Open raw JSONL in an editor for complete requests/history. Stage 2 has feedback in its second request/history, not a standalone tool event. The viewer shows proposed calls and matching results in cumulative input snapshots; repeated history is not fresh execution. It bounds excerpts rather than printing complete payloads. Preserve workspaces using the worksheet instructions.

Explain who builds requests, proposes calls, performs the read, appends results and enforces the finite stop. Compare the real count observed by the transfer check with a merely completed conversation. Read the short worked functions when necessary; no reconstruction is required.

Then complete **only [Select evidence](../../modules/context-and-state/02-select-evidence.md)**, including its prediction and query variation:

```bash
uv run --frozen --offline python modules/context-and-state/lab/inspect_context.py select --output .cache/pilot-select-1
uv run --frozen --offline python modules/context-and-state/lab/inspect_context.py select --query 'collection gap' --output .cache/pilot-select-gap-1
```

The worksheet's repair, injection, optional reconstruction, guard extensions and all model/Docker routes are excluded from this pilot's required assessment. The companion's preceding/following lessons are optional. Learners can read them later; do not expand the session silently.

## Evidence and handoff

Use the five objectives in `alignment-and-review.md`; interpret answers with `facilitator-key.md` only after collecting them. Report per-objective correctness and assistance, not a certification score. Preserve initial answers and reviewer disagreements. Do not fill the session record with simulated learner results.

A second human reviewer can assess technical/item clarity and independently score the supplied sample responses before the pilot. If unavailable, report **author-prepared; independent review pending**. An author/AI desk check cannot supply that review or learner evidence. The current preparation audit is in [alignment and review](alignment-and-review.md).

[Sources and limits](alignment-and-review.md#original-foundations) · [Existing learner checklist](../../tracks/01-author-the-loop/pilot-checklist.md)
