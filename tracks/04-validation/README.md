# Validate outputs

Status: deferred application outline; lessons and labs are not implemented. See the [capability map](../../README.md) and [application backlog](../../docs/plans/queue/05-consulting-applications.md).

## Goal

Check results independently of model confidence or apparent task completion.

## Prerequisites

Supplied workflow outputs and synthetic ground truth; implementing Tracks 2–3 is optional.

## Proposed lessons

| Lesson | Coverage |
| --- | --- |
| 1. Outcome versus trajectory | Separate completed calls, loop termination, artifact correctness, and evidence sufficiency. |
| 2. Small repeatable checks | Five fixed tasks, reset state, independent graders, and failure categories. |
| 3. Claim review | Supported observations, unsupported assertions, contradictory evidence, and warranted abstention. |
| 4. Detection proposal | Fixed rule fixtures, unchanged baseline, held-out examples, and explicit limits of TP/FP counts. |

## Proposed exercise

Grade a timeline and finding draft containing a seeded unsupported claim. Optionally evaluate a proposed rule diff with an existing validated converter; do not assume SQLite matches production query semantics.

## Completion check

Detect seeded errors without relying on a model reviewer, preserve uncertainty, and distinguish fixture performance from operational detection effectiveness.

## Scope

Teach the necessary concepts locally. External viewing is optional. Use independent starting states, synthetic fixtures, and small visible implementations. No live client access or production deployment is required.

## Original sources and project additions

[Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) supports task/trial/grader concepts. Five tasks are a teaching scope, not a statistically sufficient model ranking.

Apply the [citation policy](../../docs/citation-policy.md) in each future lesson; this track outline is not a substitute for local attribution. See the [source register](../../reference/sources.md) for verification scope.

[Back to collection](../../README.md)
