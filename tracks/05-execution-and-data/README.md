# Control execution and data

Status: deferred application outline; lessons and labs are not implemented. See the [capability map](../../README.md) and [application backlog](../../docs/plans/queue/05-consulting-applications.md).

## Goal

Enforce boundaries independently of model behavior and explain how data moves through the workflow.

## Prerequisites

A working contained loop or supplied executor starting point. Baseline containment is already required in Track 1.

## Proposed lessons

| Lesson | Coverage |
| --- | --- |
| 1. Data flow and authority | Client sources, controller, model destination, executor, outputs, credentials, and logs. |
| 2. Isolation | Two engagements, restricted paths, symlinks, read-only access, network destinations, and resource limits. |
| 3. Prompt injection | Synthetic untrusted instructions; distinguish refusal, blocked attempt, and successful unauthorized effect. |
| 4. Review and resumption | Approval tied to exact operation/arguments and artifact; denial, expiry, and revalidation. |
| 5. Retention and disclosure | Trace minimization, redaction, authorized destinations, and engagement handling rules. |

## Proposed exercise

Try cross-engagement reads and synthetic-secret exfiltration against disposable targets. Return a partial query result and verify that the final output does not claim full coverage. No real secrets or customer endpoints.

## Completion check

Show the independent control that blocked each prohibited action. Document residual limits; a passed test does not establish general security.

## Scope

Teach the necessary concepts locally. External viewing is optional. Use independent starting states, synthetic fixtures, and small visible implementations. No live client access or production deployment is required.

## Original sources and project additions

[Simon Willison: The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) supports the injection/data-flow model; [Docker security](https://docs.docker.com/engine/security/) supports execution-boundary discussion. Project SIEM policy: routine raw telemetry stays in the SIEM; local stores hold derived behavior, while scoped investigation artifacts follow explicit handling rules.

Apply the [citation policy](../../docs/citation-policy.md) in each future lesson; this track outline is not a substitute for local attribution. See the [source register](../../reference/sources.md) for verification scope.

[Back to collection](../../README.md)
