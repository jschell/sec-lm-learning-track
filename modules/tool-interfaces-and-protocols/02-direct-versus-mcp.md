# 2. Direct versus MCP

Goal: locate the protocol boundary while holding the function, fixture and arguments constant.

MCP defines tool discovery and calls between a client and server. Our [server](lab/server.py) registers one definition and passes call arguments to exactly the same `dispatch` function as the direct path. Its `CallToolResult` carries text, structured outcome data and `isError`; see the [original tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). Model-facing formats remain a separate adapter.

## Predict and run

Predict whether putting the same invalid call through a protocol will make it valid, and whether a JSON-RPC response guarantees that the task succeeded. Prepare the [optional MCP group](README.md#setup-and-first-run), then:

```bash
uv run --frozen --offline --group mcp python modules/tool-interfaces-and-protocols/lab/mcp_demo.py --output .cache/tools-mcp-1
```

The client launches the fixed supplied server with `StdioServerParameters`, using stdin/stdout pipes. There is no separately configured endpoint. Read [the pinned SDK transport documentation](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/docs/client/transports.md) for optional depth. The subprocess runs with host permissions; stdio is communication, not a sandbox. This supplied program exposes only the synthetic lookup and writes its dedicated audit.

## Inspect the actual exchange

Open these artifacts in your editor:

1. `messages.jsonl`: the client sends `server/discover`, then `tools/list`, then six `tools/call` requests. Match each response to a request by JSON-RPC ID. These messages were copied at the SDK's decoded stream boundary; they are not reconstructed from the report and do not record raw byte framing. An outgoing record alone does not prove execution.
2. `discovered-tools.json`: one tool and its input schema. Compare it with the direct report's definition.
3. `report.json`: negotiated protocol/version and each returned outcome, including the complete MCP result.
4. `executions.jsonl`: written inside the separate server at actual function entry. Match its three event IDs with the direct audit.

In the observed SDK 2.3.0 run, automatic connection discovery selects protocol **2026-07-28**. There is no `initialize` message in this run. The SDK documents its older initialize-handshake compatibility path separately in [Protocol versions](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/docs/protocol-versions.md); that path is not exercised here. Do not confuse SDK version 2.3.0 with protocol revision 2026-07-28.

## Compare results and inspect failures

The six `structuredContent` outcomes match the direct path. Invalid arguments and the seeded function failure return `isError: true`; E999 returns `not_found` with `isError: false`. All are replies to successfully exchanged protocol requests. A protocol reply, domain result and task grade answer different questions.

The server explicitly invokes our validator before the lookup. It does not infer permission from the description or silently coerce the wrong type. Listing the tool does not execute it. A call entering the server handler also does not by itself prove the domain function ran; use the entry audit.

Finally, open `feedback-example.json`. Its `proposal-1` ID links the illustrative model call to its result. The JSON-RPC request ID in `messages.jsonl` links client/server messages instead. They are separate namespaces; the host must perform any mapping and supply returned data to a subsequent model request. This lab does not do inference.

## Explain and check

- Match a rejected call's request/response, then explain why it has no function-entry audit record.
- Match E500's request/response and audit entry. What failed after validation?
- Which code changes a domain outcome into MCP content? Which changes it into illustrative model feedback?
- Does green transport integration establish useful model tool selection? What observation is missing?

Expected: the same three function entries and unchanged outcomes as the direct path. Actual model-selected actions and subsequent inference are absent. The [worked table](worked-observations.md) gives the author run; use your own artifacts for an explanation.

## Troubleshooting

A missing `mcp` import means the optional group is not prepared or the command omitted `--group mcp`. Initial sync may need network access. An existing output directory is refused; choose a new name. Protocol/runtime failures exit 2 and retain created artifacts. Inspect `server-stderr.txt` and the last decoded message; do not write debug prints to server stdout, which carries protocol traffic. The runner bounds requests to five seconds and the whole session to twenty seconds, with SDK subprocess cleanup.

[Session notes](README.md#completion-notes) · [Sources](SOURCES.md)
