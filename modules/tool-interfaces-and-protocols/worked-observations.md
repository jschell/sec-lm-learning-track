# Worked observations

Observed 2026-10-17 (America/Los_Angeles) on Python 3.12.15, uv 0.12.23 and MCP Python SDK 2.3.0. These are actual local direct/subprocess calls with authored proposals; no model ran. Predict before inspecting this table.

| Authored proposal | Domain outcome on both paths | Function entry | MCP `isError` |
| --- | --- | --- | --- |
| proposal-1: E001 | `found`, blocked synthetic event | Yes | false |
| proposal-2: numeric ID | `invalid_arguments` | No | true |
| proposal-3: missing ID | `invalid_arguments` | No | true |
| proposal-4: E999 | `not_found` | Yes | false |
| proposal-5: E500 | `execution_error` | Yes | true |
| proposal-6: extra field | `invalid_arguments` | No | true |

Both reports contain six proposals, identical domain outcomes and three function entries. Both entry audits contain E001, E999, E500 in that order. E500 is a deliberate in-process exception fixture, not a tested connection to a failed external backend.

The decoded MCP message capture contains eight request/response pairs: `server/discover`, `tools/list` and six `tools/call`. Corresponding JSON-RPC IDs match. SDK automatic discovery selected **2026-07-28**. The older `initialize` compatibility path was not used; [pinned SDK documentation](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/docs/protocol-versions.md) explains the distinction.

The first tool result's `structuredContent` equals the first direct outcome. Its corresponding model-feedback example instead uses authored `proposal-1` as `tool_use_id`; this is not the transport request ID. That illustrative file was never sent to a model.

Reproduce using [the lesson commands](README.md#setup-and-first-run). Outputs and audit files are created per run; this page is the author's summary, not an independent learner walkthrough. Original [source/provenance details](SOURCES.md) and [validation boundaries](VALIDATION.md) are separate.
