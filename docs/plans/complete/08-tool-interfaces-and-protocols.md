# Plan 08: Tool interfaces and protocols

Status: implementation complete; two worked lessons and direct/local-MCP lab authored and checked. Independent learner/portability evidence remains open. See [module](../../../modules/tool-interfaces-and-protocols/README.md) and [validation](../../../modules/tool-interfaces-and-protocols/VALIDATION.md).
Estimated learner effort: two 30–45-minute modules, excluding setup; project estimate.
Prerequisites: understand a call/result exchange. Supply the complete function and calls; earlier learner-authored code is unnecessary.

## Learning question

How does generated text become a validated operation, and what changes when the same function is exposed through MCP?

## Worked modules

1. **Contract and dispatch.** Supply one read-only `lookup_event(event_id)` function over a tiny synthetic fixture. Trace a fixed valid proposal through argument validation, dispatch and feedback. Vary a malformed argument, an unknown event and a function failure separately. Show the difference between invalid arguments, a valid not-found result and execution failure. Keep the raw proposal, accepted call and actual function invocation visible. Explain description/schema steering using [Anthropic's original tool-interface discussion](https://www.anthropic.com/engineering/writing-tools-for-agents).
2. **Direct versus MCP.** Expose that same function through one local stdio MCP server/client pair. Inspect connection negotiation, discovery, invocation and returned result/error. The observed SDK 2.3.0 automatic path uses server/discover and protocol 2026-07-28; an initialize-handshake compatibility path is not exercised. Keep function, fixture and arguments constant; change the transport boundary. Use the [versioned MCP specification](https://modelcontextprotocol.io/specification/2026-07-28) and official Python SDK as original protocol/implementation references. Protocol requests need not be model-selected. MCP is a tool protocol; the model-facing format remains a separate adapter.

## Starting state and artifacts

Implement under `modules/tool-interfaces-and-protocols/`. Provide complete direct-call and MCP examples, fixture, fixed call inputs, annotated exchange and reset instructions. Add MCP dependencies only in an optional uv group, pinned in the lockfile after checking Python 3.12 compatibility and the exact SDK API. Record the tested negotiated protocol version; citing the current specification does not imply that the selected SDK implements every version.

Write a small side-by-side record: proposal, validation outcome, execution count, returned data/error and transport messages. Fixed calls are sufficient for protocol inspection. A later optional live observation may vary one description while holding function/schema/task constant, with actual results recorded and no promise that the tiny model can select it correctly.

## Acceptance

- [x] Runnable worked examples with prediction, one-factor variation, deliberate failure and explanation.
- [x] Both paths return equivalent fixture data; invalid calls do not execute the function.
- [x] Unknown IDs and execution failures remain distinguishable; no fabricated data fills errors.
- [x] Worked artifacts/questions separate authored proposal, validated arguments, actual invocation and illustrative model feedback; independent learner demonstration remains unperformed.
- [x] Original sources, exact SDK/runtime versions, adapted-code licenses and observable protocol boundaries documented.
- [x] Offline direct inspection and local MCP integration checked separately from any model observation.
- [x] Independent learner/portability evidence remains explicitly open when unperformed.

## Boundaries

Read-only synthetic fixture, local subprocess transport, bounded calls and outputs, no listener or credentials, no shell exposed to the model. Starting the explicitly supplied MCP server is host setup, not a model shell tool. No remote authentication, MCP fleet, new agent framework, general provider router or native function-calling survey. Reuse selected concepts from [Track 2](../../../tracks/02-security-tools/README.md); its consulting query/enrichment workflow remains deferred.

## Sources

[Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) and [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28), checked 2026-10-17 for topic/protocol scope. [Official Python SDK](https://github.com/modelcontextprotocol/python-sdk) is the implementation candidate: verify release, APIs, license and supported protocol during authoring. Exercise scope is original project design.
