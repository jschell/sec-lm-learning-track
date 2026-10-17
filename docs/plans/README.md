# Implementation sequence

Implementation readiness and validation are separate. Independent learner, hosted-provider and physical Pi checks remain open in their existing records; they do not block unrelated, reversible lesson authoring. Merge confirmation means verify checks and continue to the next ready authorized plan.

## Existing material and validation

| Plan | Implementation | Outstanding evidence |
| --- | --- | --- |
| [01: Huntley loop](complete/01-harness-lessons.md) | Complete worked stages and worksheet | [Independent learner pilot](active/02-track1-pilot.md); hosted observations |
| [03: Messages and model input](complete/03-messages-and-model-input.md) | Tokenizer/template lab and state companion implemented | Independent learner understanding |
| [04: Generation and sampling](active/04-generation-and-sampling.md) | CPU setup and generation/sampling lab implemented | Model suitability limits, physical Pi resources/setup, learner observations |
| [06: Local tool feedback](active/06-local-tool-feedback.md) | Explicit model/prompt comparison and feedback lab implemented | Physical Pi and learner explanation; exact task failures remain visible |

The modules' validation records are authoritative for observations. An active validation plan does not mean its implementation must be rebuilt.

## Additional mechanics tracks

These are bounded learning plans, not implemented lessons or a mandatory sequence. Estimated effort is a project planning judgment, excluding first-time runtime setup.

| Order | Plan | Readiness | Learner session |
| --- | --- | --- | --- |
| 1 | [07: Context and state](active/07-context-and-state.md) | Active; next implementation | Three 20–40-minute modules |
| 2 | [08: Tool interfaces and protocols](queue/08-tool-interfaces-and-protocols.md) | Queued; implement after 07 | Two 30–45-minute modules |
| 3 | [09: Output validation and uncertainty](queue/09-output-validation-and-uncertainty.md) | Queued; implement after 08 | Two 30–45-minute modules |
| 4 | [10: Untrusted input and execution authority](queue/10-untrusted-input-and-authority.md) | Queued; implement after 09 | Two 30–45-minute modules |

Order supports authoring and reuse; supplied starting snapshots keep each track independently usable. Plans 08–10 are authorized planning scope and next-stage candidates, not a reason to implement every track in one PR. Resolve observed blockers before adding machinery.

[05: Consulting applications](queue/05-consulting-applications.md) remains deferred. Existing Tracks 2–5 contribute concepts to the mechanics plans; engagement management, client integrations and Track 6 delivery remain later applications. Preserve existing track URLs and use their outlines as navigation pointers rather than creating duplicate lessons.

[Design maintenance](active/00-curriculum-design.md) follows the [current design](../design.md). Original foundations and attribution are in each plan and the [source register](../../reference/sources.md).
