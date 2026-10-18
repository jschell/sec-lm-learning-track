# Original sources and fixture provenance

Checked 2026-10-17 (America/Los_Angeles). Lessons, synthetic fixtures, dispatcher comparison and scripts are original project work under MIT. No real credentials, client telemetry, external destination or attack dataset is used.

| Original source | Concept used | Verification scope |
| --- | --- | --- |
| Simon Willison, [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), 2025-06-16 | Risk from untrusted content, private data and externally communicating actions | Original article reopened; our offline read-only fixture isolates only selected boundaries, not a complete exfiltration experiment |
| Geoffrey Huntley, [how to build a coding agent: free workshop](https://ghuntley.com/agent/), 2025-08-24 | Inference/tool dispatch/feedback loop | Original article reopened; existing [Track 1 provenance](../../tracks/01-author-the-loop/SOURCES.md) pins upstream code; no Go copied |
| Anthropic, [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Matching call/result IDs and returned error feedback | Official documentation inspected in this collection's source checks; actual message structure exercised here with authored responses, not hosted inference |

## Existing project material

The injected note is the original synthetic [Track 1 fixture](../../tracks/01-author-the-loop/lab/fixtures/injected-note.txt), reused from [immutable repository commit 189cb694](https://github.com/jschell/sec-lm-learning-track/blob/189cb694b13725fe420d97a9a010675da30f8fd7/tracks/01-author-the-loop/lab/fixtures/injected-note.txt). The benign version retains its fictional factual sentence without the added instruction. These are project-owned MIT fixtures, not copied customer data.

The script imports the existing unchanged `run_loop`, `Trace`, `Workspace`, `schema` and task-specific system text. The [recording-only missing-controls lesson](../../tracks/01-author-the-loop/08-learn-from-missing-guards.md) supplies this project's accepted teaching approach: expose the implementation mistake through bounded proposals, then inspect independent controls. Execution-enabled reference guards remain intact.

## New project artifacts and limits

- `proposals.json`: three authored operations with misleading approval descriptions. They are not captured model choices.
- `AuthoredResponses`: fixed read/end sequence or fixed read/edit/end sequence selected by the program. It does not infer an action from file content.
- `description_only_recording`: intentionally incorrect substring-based permission idea; its only result is a recording label. No operation callback exists on that path.
- `ReadOnlyTools`: explicit exact operation/argument check before the sole real operation, `Workspace.read(note.txt)`. It contains no edit/shell/network implementation. A source instruction or claimed approval is not consulted by its enforcing condition.
- `private.txt`: setup-generated literal `SYNTHETIC-NOT-A-SECRET`, present solely to distinguish an unauthorized path from a missing file.
- `effect`: logged after a completed real read; not inferred from a model's words. Setup and host-side reporting are separate file operations outside tool dispatch.

The policy, fixture cases, labels, flow diagram, learner questions and expected outcomes are original teaching choices. Passing a fixed read-only test does not establish arbitrary tool safety, model injection resistance or an OS isolation boundary. No upstream article prose or source implementation is reproduced.
