# Plan 01: Author the compact harness track

Status: queued.

## Work

Choose SDK/provider, supported Python version, replay format, and execution launcher. Author the five Track 1 lessons in order with independent starter states and worked solutions. Preserve a 4–8-hour target for familiarity; do not require benchmarks, MCP, local-model setup, or framework comparison.

## Acceptance

- Synthetic offline replay and explicitly separate live-inference path.
- Deliberate broken-program repair with immutable external grader.
- Timeouts, output/iteration limits, tool-result IDs, errors, and stopping status visible.
- Model credentials outside contained tool execution.
- Original upstream code paths, commit/license metadata for any adaptation.
- Another learner can follow commands and explain every transition.

## Sources

[Huntley workshop](https://ghuntley.com/agent/) and [Go code](https://github.com/ghuntley/how-to-build-a-coding-agent); [Docker security](https://docs.docker.com/engine/security/). Python fixture and grading design are original project work.
