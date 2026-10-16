# 2. One tool exchange

Status: authored; offline reference checked. Estimated effort: 45–60 minutes.
Prerequisites: Lesson 1 concepts; supplied starter is independently usable.

## Goal

Return a tool result that matches a model-requested call, with correct message ordering.

## Explanation

A tool definition describes an available operation. A tool call is a request to perform it. Your registry and dispatch code turn that request into execution; the description grants no machine access by itself. The host program retains responsibility for validation and boundaries.

[Huntley](https://ghuntley.com/agent/) introduces read_file to expose this exchange. Anthropic's [client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) represents the call as tool_use in assistant content and the matching tool_result in the next user message. Other providers have different wire formats.

## Worked example

A definition includes a name, description, and input_schema. Our read_file schema requires exactly one string argument, path. The same rule is enforced in Python; the schema alone is not our enforcement.

```json
{"role":"assistant","content":[
  {"type":"tool_use","id":"read-1","name":"read_file","input":{"path":"notes.txt"}}
]}
```

The controller dispatches read_file and appends:

```json
{"role":"user","content":[
  {"type":"tool_result","tool_use_id":"read-1","content":"Synthetic exercise...","is_error":false}
]}
```

The content above is abbreviated for teaching. In an actual lab trace, the content is the bounded text returned by Tools.result. The ID ties this result to that call; the function name alone cannot distinguish repeated calls.

```bash
uv run --frozen --offline python tracks/01-author-the-loop/lab/check_authoring.py --file tracks/01-author-the-loop/lab/solutions/stages.py --stage 2
uv run --frozen --offline python tracks/01-author-the-loop/lab/cli.py --scenario read
```

Expected: PASS lesson 2; completed with one tool call. The second inference request contains user → assistant call → user result. The response after that is the assistant's answer.

## Authoring exercise

Implement exchange in [starter/stages.py](lab/starter/stages.py). Make one inference request, append its assistant content, dispatch tool_use blocks, append the results as one user message, then infer again with that history. Return the final response and history.

```bash
uv run --frozen --offline python tracks/01-author-the-loop/lab/check_authoring.py --file tracks/01-author-the-loop/lab/starter/stages.py --stage 2
```

This bounded two-request exercise assumes the first response requests tools and the second ends. Lesson 3 removes that assumption. Use the supplied stages solution as your independent starting point if needed.

## Observe and vary

In your own copy of replay/read.json, change the first path to missing.txt and remove that turn's expected-success checks. Run Replay against that file using your exchange function. The result should set is_error=true. The unchanged scripted final answer may now be false: replay responses do not adapt. This is a useful demonstration of why output needs independent checking.

## Completion check

Identify the call ID in the assistant message and matching result. Explain why results must follow the calls before the next inference, where schema validation happens, and which code actually reads the file.

## Troubleshooting and boundaries

Do not append only the tool result while omitting the assistant call. Do not put tool text into system instructions. File paths must be relative, with no '..' or symlinks. Reads are confined to a disposable synthetic workspace; command execution is disabled in this exercise.

## Original sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| File tool progression | [Huntley workshop](https://ghuntley.com/agent/); pinned read.go in [source record](SOURCES.md) | Conceptual inspiration; original fixtures/code |
| Schemas | [Anthropic: Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) | Checked 2026-10-16 |
| IDs, message ordering, errors | [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Checked 2026-10-16; no live API validation |

[Next: author the loop](03-author-the-loop.md).
