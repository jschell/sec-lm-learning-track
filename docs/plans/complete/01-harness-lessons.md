# Plan 01: Author the compact harness track

Status: authoring complete; verification scope is explicit in the [validation record](../../../tracks/01-author-the-loop/VALIDATION.md).

## Delivered

- Five self-contained lessons, learner starters, worked solutions, source record, and trace guide.
- Python 3.12+ standard-library implementation: Anthropic-format Messages REST transport for direct Anthropic or OpenRouter, no framework or SDK dependency; uv lockfile included.
- Seven authored synthetic replay scenarios and actual bounded file operations.
- Deliberately broken FizzBuzz fixture, reference repair, and fixed read-only external grader.
- Docker-only execution with no host fallback; integration verification script and CI job.
- Limits, IDs, error results, stop reasons, bounded output, and JSONL traces.
- Original-source citations and pinned upstream comparison; no upstream code copied.

## Acceptance and limits

Offline functional tests and documented replay/reference commands pass locally. Docker is unavailable in the authoring environment; the genuine integration check passed in hosted CI, including actual FAIL→edit→PASS and execution controls. It is not represented as locally verified. Live-model behavior and a separate human learner walkthrough are not performed; these do not prevent using the authored offline lessons, but remain distinct validation activities. See the validation record for current CI evidence.

The compact learning target remains 4–8 hours. No model leaderboard, MCP, or framework comparison is required.

## Sources

[Huntley workshop](https://ghuntley.com/agent/), [pinned source details](../../../tracks/01-author-the-loop/SOURCES.md), [Anthropic protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls), and [Docker run reference](https://docs.docker.com/engine/containers/run/). Python implementation and lab material are original project work.
