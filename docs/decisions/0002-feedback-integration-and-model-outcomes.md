# 0002: Separate feedback integration from exact model outcomes

Date: 2026-10-17. Status: adopted for this teaching lab. Revises the strict default introduced by PR #10; the exact task check itself is unchanged.

## Evidence and problem

[Merged-main run 39077441549](https://github.com/jschell/sec-lm-learning-track/actions/runs/39077441549) failed because one of three ordinary 360M/example attempts omitted `LAB-` after an actual successful read. The other two exact-answer tasks passed. The failed case completed the tool/feedback exchange and returned the correct suffix, but it did not meet the stated entire-line check. Its `task_passed` remains false.

The [retained original record](../../modules/tool-requests-and-feedback/observations/main-2026-10-17.json) includes all three cases, raw model text, matching tool results, next requests, formatted input and artifact provenance. The artifact ZIP SHA-256 was verified before extracting it. Earlier local and PR successes remain observations; they did not establish reliable copying for arbitrary fresh codes.

The teaching purpose is to understand the loop introduced by [Geoffrey Huntley](https://ghuntley.com/agent/). Correct ordering and matching feedback are explicit in [Anthropic's client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). These sources support the mechanics being inspected; the CI policy below is this project's judgment based on its own failure evidence.

## Decision

Standard real-model CI checks the API/containment assertions and three explicit ordinary/example **feedback exchanges**. For each exchange it requires:

- An actual successful `read_file(status.txt)` with the expected fresh contents and matching call/result ID.
- The call and result in the following canonical request.
- The exact returned result in the adapter's next user message and formatted model input, followed by a native response and completed loop.

This is an observable trace contract, not proof of private reasoning or correct final wording. Missing reads, mismatched IDs, dropped feedback, missing native response and incomplete loops still fail the required integration check.

The independent entire-line grade continues to compare the final answer exactly. All raw outputs, `task_passed` values and failed attempts remain visible in the artifact and a CI summary showing exact task counts separately from integration. `--require-example-task` remains an optional strict all-three task requirement; it can be combined with `--require-feedback`. A strict task failure still emits observations before exiting 1.

There is no answer normalization, prefix repair, inference retry, removal of the failed fixture or automatic larger-model fallback. The 360M/example configuration is a useful bounded demonstration with observed successes and failures, not a dependable autonomous-agent claim.

## Consequences and revisit conditions

Green standard CI means its explicit integration checks passed; read the task counts before making an accuracy claim. A legitimate imperfect model answer becomes learning evidence without being mislabeled as a controller defect. If the model stops producing the required read/feedback exchange, CI still fails and the failure must be investigated.

An application that depends on exact output needs its own documented accuracy requirement, representative tasks and enforcement; this course does not certify that application. Revisit this decision if the lesson promises a dependable exact-copy workflow or a different task makes exact accuracy central to its completion contract. [Decision 0001](0001-worked-stages-first.md) continues to govern the worked-example progression and narrow checks.
