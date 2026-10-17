# Understand and author the loop

Status: design sketch; lessons and labs are not implemented.

## Goal

Build and explain a small Python harness. This is the complete Geoffrey Huntley-inspired starting track, approximately 4–8 focused hours as a project estimate.

## Prerequisites

Python and ordinary command-line use. No prior neural-network training or other track required.

## Proposed lessons

| Lesson | Coverage |
| --- | --- |
| 1. Minimal inference | One SDK request, response, visible message history, and a replayed response. |
| 2. One tool exchange | Schema, model-requested arguments, call IDs, validation, dispatch, and returned results. |
| 3. Author the loop | Repeated inference → tool execution → feedback; multiple calls handled sequentially; explicit stop reasons. |
| 4. Complete a task | Read/list/search/edit/execute primitives; deliberate broken program and independent test. |
| 5. Control and inspect | Malformed arguments, failed edits, command timeout, bounded output, turn limits, and JSONL trace. |

## Proposed exercise

Repair a deliberately broken toy program in a disposable workspace. Provide independent starter files and a grader outside agent write access. Keep controller credentials outside the tool executor; establish no-network, restricted mounts and resource limits before the first generated command executes.

## Completion check

Explain each transition from the saved messages, distinguish termination from correctness, and change one aspect of the loop intentionally.

## Scope

Teach the necessary concepts locally. External viewing is optional. Use independent starting states, synthetic fixtures, and small visible implementations. No live client access or production deployment is required.

## Original sources and project additions

[Geoffrey Huntley's workshop](https://ghuntley.com/agent/) and [original Go source](https://github.com/ghuntley/how-to-build-a-coding-agent) supply the progression. [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) is an optional alternate harness; [Docker security](https://docs.docker.com/engine/security/) informs containment. Python exercises are project adaptations/original work; pin upstream commits and licenses before copying code.

Apply the [citation policy](../../docs/citation-policy.md) in each future lesson; this track outline is not a substitute for local attribution. See the [source register](../../reference/sources.md) for verification scope.

[Back to collection](../../README.md)
