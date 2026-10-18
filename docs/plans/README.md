# Implementation sequence

Implementation readiness and validation are separate. Independent learner, hosted-provider and physical Pi checks remain open in their existing records; they do not block unrelated, reversible lesson authoring. Merge confirmation means verify checks and continue to the next ready authorized plan.

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

The modules' validation records are authoritative for observations. An active validation plan does not mean its implementation must be rebuilt.

## Additional mechanics tracks

These are bounded learning units, not a mandatory sequence. Implementation status is explicit; queued plans are not runnable lessons. Estimated effort is a project planning judgment, excluding first-time runtime setup.

| Order | Plan | Readiness | Learner session |
| --- | --- | --- | --- |
| 1 | [07: Context and state](complete/07-context-and-state.md) | Implemented; independent learner check open | Three 20–40-minute modules |
| 2 | [08: Tool interfaces and protocols](complete/08-tool-interfaces-and-protocols.md) | Implemented; independent learner check open | Two 30–45-minute modules |
| 3 | [09: Output validation and uncertainty](complete/09-output-validation-and-uncertainty.md) | Implemented; independent learner check open | Two 30–45-minute modules |
| 4 | [10: Untrusted input and execution authority](queue/10-untrusted-input-and-authority.md) | Queued; next ready implementation | Two 30–45-minute modules |

Order supports authoring and reuse; supplied starting snapshots keep each track independently usable. Plan 10 is the next authorized implementation candidate. Keep each bounded track reviewable in its own PR. Resolve observed blockers before adding machinery.

[05: Consulting applications](queue/05-consulting-applications.md) remains deferred. Existing Tracks 2–5 contribute concepts to the mechanics plans; engagement management, client integrations and Track 6 delivery remain later applications. Preserve existing track URLs and use their outlines as navigation pointers rather than creating duplicate lessons.

[Design maintenance](active/00-curriculum-design.md) follows the [current design](../design.md). Original foundations and attribution are in each plan and the [source register](../../reference/sources.md).
