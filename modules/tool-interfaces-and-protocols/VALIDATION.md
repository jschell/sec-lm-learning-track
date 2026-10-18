# Validation record

Observed locally 2026-10-17 (America/Los_Angeles): Python 3.12.15, uv 0.12.23, MCP SDK 2.3.0. Reproduce after [setup](README.md#setup-and-first-run).

```bash
uv run --frozen --offline python -m unittest discover -s modules/tool-interfaces-and-protocols/lab/tests -v
uv run --frozen --offline --group mcp python -m unittest discover -s modules/tool-interfaces-and-protocols/lab/mcp_tests -v
```

## Performed

- Four standard-library contract tests: invalid types/fields/names cause zero function entries; not-found differs from execution failure; illustrative feedback retains proposal IDs/error flag; complete direct run and overwrite refusal.
- One real SDK/stdin/stdout subprocess integration test with six calls: direct outcomes equal MCP structured outcomes, discovered schemas match, actual function audit contains only E001/E999/E500, request/response IDs match, and protocol 2026-07-28 plus result error flags are observed.
- Both documented entry points run successfully. The MCP client itself starts/closes the supplied server; no existing server is assumed. [Worked observations](worked-observations.md) records the outcomes.
- Existing Track 1 tests: 43 pass. Context tests: seven pass. No loop or context runtime code changed.
- Initial interpreter/dependency setup was performed in this workspace, not a fresh OS or physical Pi. Required dependencies were prepared before the offline commands.

[Tool protocol CI](../../.github/workflows/tools.yml) runs direct and MCP checks plus both entry points on Python 3.12/3.13. A configured workflow is not by itself evidence of a successful run; inspect actual CI results separately.

## What this establishes

The supplied dispatcher enforces its narrow displayed contract; a real local MCP subprocess exposes the same outcomes through actual protocol messages. Function entry, negative domain result and execution failure remain distinguishable. This does not establish model choice, model understanding, production authorization or MCP-wide conformance.

| Evidence | State |
| --- | --- |
| Fixed direct calls | Locally observed |
| Real SDK/stdin/stdout protocol exchange | Locally observed; protocol 2026-07-28 |
| Older initialize handshake, remote transports and authentication | Not exercised |
| Actual model-selected tools or subsequent inference | Not performed; authored proposals and feedback examples only |
| Independent learner explanation/transfer | Pending |
| Physical Pi / fresh-OS portability | Not performed |

[Original sources and fixture provenance](SOURCES.md). No fabricated or repaired outcomes are used.
