# Package a repeatable workflow

Status: design sketch; lessons and labs are not implemented.

## Goal

Deliver a small workflow another consultant can run, inspect, and maintain.

## Prerequisites

Track 1 and supplied versions of tools, fixture, grader, and controls; advanced tracks need not be reimplemented.

## Proposed lessons

| Lesson | Coverage |
| --- | --- |
| 1. Choose control flow | Fixed pipeline, bounded model step, or autonomous loop; locate where decisions belong. |
| 2. Package and configure | Locked dependencies, versioned prompt/tool definitions, explicit configuration, and secret references. |
| 3. Run record and handoff | Evidence references, configuration hashes, model/runtime IDs, versions, coverage, cost/latency where available, and known limits. |
| 4. Framework comparison | Optional same-task Pydantic AI implementation, reusing tools, containment, fixture, and grader. |
| 5. Peer review | Second consultant reruns the task, finds one seeded failure, and challenges an unsupported claim. |

## Proposed exercise

Package a read-only synthetic investigation workflow and its reviewable output. Compare fixed control flow with the raw loop. Add framework comparison only if it answers a concrete maintenance question.

## Completion check

A second consultant reproduces the deterministic checks, traces conclusions to evidence, and diagnoses an incomplete run. Live model text need not be byte-identical; state which parts are reproducible.

## Scope

Teach the necessary concepts locally. External viewing is optional. Use independent starting states, synthetic fixtures, and small visible implementations. No live client access or production deployment is required.

## Original sources and project additions

[Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) supports workflow/agent distinctions. [Pydantic AI agents](https://ai.pydantic.dev/agents/) and [advanced tools](https://ai.pydantic.dev/tools-advanced/) support optional framework exploration. Packaging and peer-review criteria are project recommendations.

Apply the [citation policy](../../docs/citation-policy.md) in each future lesson; this track outline is not a substitute for local attribution. See the [source register](../../reference/sources.md) for verification scope.

[Back to collection](../../README.md)
