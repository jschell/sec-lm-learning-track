# 1. Contract and dispatch

Goal: separate proposed arguments, accepted arguments, function entry and result semantics.

A useful tool definition states its name, purpose, inputs and result behavior. Descriptions help a model choose; they do not execute the operation or establish its permissions. See [Anthropic's original tool-design discussion](https://www.anthropic.com/engineering/writing-tools-for-agents). Here the calls are authored so you can inspect the contract without attributing a choice to a model.

## Predict and run

Open [the six proposals](lab/calls.json). Predict which enter `lookup_event`, and which return an error. Then, from the repository root after [setup](README.md#setup-and-first-run):

```bash
uv run --frozen --offline python modules/tool-interfaces-and-protocols/lab/direct.py --output .cache/tools-direct-1
```

Open `report.json` and `executions.jsonl` in the output directory. A valid input is exactly one `event_id` string matching `E` plus three ASCII digits. No extra fields are allowed. The schema and explicit enforcing code are together in [contract.py](lab/contract.py). This small validator implements only that displayed contract, not arbitrary JSON Schema.

The transition is visible in `dispatch`:

```python
# After the explicit name/type/field/pattern checks:
accepted = {'event_id': arguments['event_id']}
data = lookup.lookup_event(**accepted)
```

Actual function entry writes an audit record. A schema is descriptive data until some code enforces it. `accepted_arguments` is recorded only after validation. Source data in [events.json](lab/events.json) is original synthetic fixture data; no live audit service is queried.

## Vary and inspect failures

The first proposal is the baseline. Compare each later proposal separately with it: change the argument type, omit the field, choose an unknown ID, choose the seeded fault ID, or add an extra field. The table is supplied by the same command; no learner implementation is required.

| Input | Result | Function entered? |
| --- | --- | --- |
| E001 | `found`, synthetic event returned | Yes |
| Numeric ID | `invalid_arguments` | No |
| Missing ID | `invalid_arguments` | No |
| E999 | `not_found`, no invented event | Yes |
| E500 | `execution_error`, seeded backend unavailable | Yes |
| E001 plus extra field | `invalid_arguments` | No |

E999 is syntactically valid. The function must run to discover that the fixture has no such event. E500 is also valid but deliberately raises a named exception after entry; it simulates a failure, not an actual unavailable backend. Neither is equivalent to invalid input. The full run has six proposals and three entries. No retry, fallback or result repair occurs.

## Prepare feedback

Open `feedback-example.json`. It contains an assistant `tool_use` and user `tool_result` sharing an authored proposal ID. The adapter serializes the actual outcome as result content. Matching IDs and tool-result ordering follow [Anthropic's original protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls); this file is an illustrative conversion, never a real model exchange.

## Explain and check

1. Locate the validation branch that prevents the numeric call from reaching the function.
2. Explain why the audit contains E500 even though that call returned an error.
3. Why does a negative domain answer differ from a failed operation?
4. What extra evidence would establish that a model selected a tool or used its result?

Expected: numeric/missing/extra inputs are rejected before entry. Only E001, E999 and E500 appear in the audit. No model runs here, so the proposals and feedback example do not establish model behavior. Continue with the same implementation over MCP.

[Next: MCP](02-direct-versus-mcp.md) · [Sources](SOURCES.md)
