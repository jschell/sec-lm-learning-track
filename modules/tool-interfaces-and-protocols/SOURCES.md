# Original sources and provenance

Checked 2026-10-17 (America/Los_Angeles). Original explanations, fixture records, dispatcher, adapters and stream recorder are project-authored under MIT. The SDK is an installed dependency, not vendored or relicensed by this repository.

## Concept sources

| Original source | Use | Verification scope |
| --- | --- | --- |
| Anthropic, [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents), 2025-09-11 | Description/schema/result design | Article opened; no claim that our fixed calls measure model selection |
| MCP, [Tools, protocol 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) | Discovery, calls, structured results and error distinction | Official page opened; our actual local protocol observed separately |
| Anthropic, [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Illustrative model-facing call/result ID relationship | Existing Track 1 source record plus reopened official documentation; model-feedback files are not inference observations |

## Pinned implementation reference

[MCP Python SDK v2.3.0](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0), immutable source commit **2118f14f8a19bc158d8a1cf90af58d85d187f849**. The release/tag, source files below and [MIT license](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/LICENSE) were inspected. Copyright is Anthropic, PBC; installed package notices remain with that distribution. No substantial upstream implementation or tutorial excerpt is copied here; the examples use documented API entry points.

| Upstream file at that commit | Local use |
| --- | --- |
| [docs/client/index.md](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/docs/client/index.md) | Client lifecycle, discovery, tool invocation and result fields |
| [docs/client/transports.md](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/docs/client/transports.md) | Local stdio subprocess and custom transport context |
| [docs/protocol-versions.md](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/docs/protocol-versions.md) | Automatic discovery versus older initialize handshake; package/protocol versions distinguished |
| [src/mcp/server/lowlevel/server.py](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/src/mcp/server/lowlevel/server.py) | Server constructor handler interfaces and stdio runner |
| [src/mcp/client/stdio.py](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/src/mcp/client/stdio.py), [stream protocols](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/src/mcp/shared/_stream_protocols.py) | Decode-boundary observation around the SDK transport; no raw byte capture |
| [pyproject.toml](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/pyproject.toml) | Release metadata inspected; actual install and API checks on Python 3.12.15 recorded in validation |

The optional `mcp` uv group pins 2.3.0; `uv.lock` records distribution hashes/transitive versions. This is a reproducible teaching configuration, not a universal MCP version requirement. Recheck APIs, source commit and observed protocol when upgrading.

## Original fixtures and observations

`lab/events.json` contains two invented events. `lab/calls.json` contains six authored proposals; E999 is an absent fixture ID and E500 is a seeded exception. No private data, external service, copied event dataset or model-generated proposal is present. Fixture revisions are versioned in git, not downloaded at runtime.

Both adapters import the same `contract.py`. Domain entry audits are actual writes in the process executing the function. MCP messages are copied from SDK stream objects; outgoing capture alone does not prove remote dispatch. The separate server audit and matching returned messages provide the integration evidence. `feedback-example.json` is a project-designed illustrative adapter, never passed to inference.
