# Tool interfaces and protocols

Status: two runnable worked lessons; direct calls and actual local MCP integration checked. Independent learner walkthrough pending.
Estimated effort: two 30–45-minute sessions, excluding setup; project estimate.
Prerequisites: Track 1 base understanding of the loop ([Part 0](../../tracks/01-author-the-loop/00-the-loop.md) at minimum; [decision 0003](../../docs/decisions/0003-base-understanding-first.md)); Python dictionaries and a call/result exchange. Complete starting code and synthetic fixtures are supplied; no previous learner edits, model, API key or existing server required.

> **Recall before you start:** What does the model receive about a tool, and what decides which function runs?

<details><summary>Check your recall</summary>

Only the definition: name, description and input schema. The program looks the function up by name when a call arrives; the description grants nothing. This module compares ways of exposing tools.

</details>

Trace how a proposed call becomes validated arguments, actual execution, a result, and potential model feedback. Compare the same read-only function directly and through MCP:

| Lesson | Worked example | Deliberate failure |
| --- | --- | --- |
| [1. Contract and dispatch](01-contract-and-dispatch.md) | Fixed proposals against one event lookup | Wrong argument type, missing/extra fields, absent event and seeded backend fault |
| [2. Direct versus MCP](02-direct-versus-mcp.md) | Same function and proposals through a local stdio subprocess | Separate invalid arguments from a function that entered and then failed |

Tool interface design draws on [Anthropic's original article](https://www.anthropic.com/engineering/writing-tools-for-agents). The transport follows the [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) using the [official Python SDK](https://github.com/modelcontextprotocol/python-sdk/tree/2118f14f8a19bc158d8a1cf90af58d85d187f849). Fixtures, explicit validation and adapters are original project work.

## Setup and first run

Install [uv](../../docs/python-development.md), then from the repository root:

```bash
uv python install 3.12
uv sync --frozen
uv run --frozen --offline python modules/tool-interfaces-and-protocols/lab/direct.py --output .cache/tools-direct-1
```

The direct lesson uses only the standard library. For the MCP lesson, prepare the separate dependency group once:

```bash
uv sync --frozen --group mcp
uv run --frozen --offline --group mcp python modules/tool-interfaces-and-protocols/lab/mcp_demo.py --output .cache/tools-mcp-1
```

Initial interpreter/dependency setup may need network access. The experiments then use local files and a subprocess, with no HTTP listener or inference. The client launches the supplied server using the same Python interpreter and closes it on exit. Do not start a server separately. Each output directory must be new; use a different name to repeat.

## Why the SDK is pinned

The optional `mcp` group targets SDK **2.3.0**, with transitive versions/hashes in `uv.lock`. This preserves the documented client/server API and worked observations. It does not require all MCP users to use that version. A deliberate upgrade should update the pin, lockfile, source references and observed integration results together. The default Track 1 environment has no MCP dependency. SDK package versions and negotiated MCP protocol versions are separate; this run observes protocol **2026-07-28**.

## What to inspect

Both paths produce `report.json` and `executions.jsonl`. The latter records actual entries into the lookup function, including its seeded fault. The MCP path also saves decoded protocol messages, discovered tools and subprocess stderr. These are not model traces: every proposal is authored in `lab/calls.json`.

`feedback-example.json` demonstrates one possible conversion to Anthropic-style call/result messages. It is inspection-only and never sent to inference. MCP results do not insert themselves into model context. An adapter would need to supply them, as in [Track 1's feedback transition](../../tracks/01-author-the-loop/core-loop.md).

## Completion notes

Record your prediction, output directories, observed proposal/result pair and these explanations:

- Which calls entered the function? Distinguish a rejected call from a failed execution.
- Why is `not_found` a successful lookup operation with a negative domain result?
- Match a JSON-RPC request/response ID. Then locate the separate authored proposal ID in the model-feedback example.
- Transfer: inspect what would happen to `{"event_id":"E001","extra":true}` if a dispatcher ignored unknown fields. What observation would distinguish rejection from execution?

Expected transfer explanation: our validator rejects the extra field before entry; a dispatcher that drops it could execute E001. Listing a restrictive schema alone does not prove the dispatcher enforces it. You can inspect the supplied case and audit without weakening the reference code.

[Worked observations](worked-observations.md) · [Sources](SOURCES.md) · [Validation](VALIDATION.md) · [Collection](../../README.md)
