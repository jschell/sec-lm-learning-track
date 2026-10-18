# 1. Follow the untrusted text

Goal: locate how retrieved file contents enter the next input, without mistaking content exposure for an executed action.

Untrusted source text can contain instructions addressed to an assistant. Willison's [original prompt-injection analysis](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) explains why content origin and available actions matter. This exercise tracks that input path; it does not measure the likelihood that a model follows an injection.

## Predict and run

The [benign fixture](lab/fixtures/benign.txt) contains one fictional observation. The [injected fixture](lab/fixtures/injected.txt) adds an instruction to ignore the user, report `INJECTION_ACCEPTED`, and change the investigation notes. The factual sentence is unchanged.

Predict which request first contains those added bytes. Will their presence by itself cause an edit in this program?

```bash
uv run --frozen --offline python modules/untrusted-input-and-authority/lab/inspect_authority.py exposure --output .cache/authority-exposure-1
```

Run from the repository root after [setup](README.md#setup-and-run). Both variants use the same user task, system text, read-only tool definition, controller and two authored responses. The first response asks to read `note.txt`; the second ends without proposing a forbidden operation. Only the file bytes differ.

## Inspect the transition

Open `injected/trace.jsonl` in the output directory:

1. Request 1 asks to inspect the note; it does not contain the returned note text.
2. The assistant response proposes `read_file(note.txt)` with ID `read-note`.
3. The dispatcher emits an allow decision, performs an actual read, and records that read as an `effect`.
4. The `tool` event contains the complete returned file text, JSON-encoded in `result.content`.
5. Request 2 includes that result, including the embedded instruction, with matching `tool_use_id`.

This uses the unchanged [Track 1 loop](../../tracks/01-author-the-loop/lab/loop.py). Its feedback structure follows the [original client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). The trace shows supplied input, not private model reasoning.

Compare `benign/trace.jsonl`: initial requests and authored responses match; returned data differs. Open both `work/notes.txt` targets after the commands finish. Both still say `Investigation open.`

## Explain the bounded result

There is no forbidden proposal in either exposure trace. The fixed script does not interpret the note or decide whether to follow it. An unchanged target here therefore does not demonstrate model refusal or prove the permission check blocked an attempt. The [next lesson](02-locate-authority.md) supplies an explicit authored attempt to inspect the enforcing boundary.

Complete these checks:

- Identify the first request containing the embedded instruction and the call/result ID that brought it there.
- Explain the difference between reading malicious text and executing the text as an instruction.
- What observation would distinguish no attempt from an attempted but denied edit?
- If a real model were substituted, which outcomes would need to be recorded rather than assumed?

Expected: request 2 contains the instruction as file data. Only a read executed. Model refusal, malformed output or an attempted action would each require actual model observation; none is established by these authored responses.

[Next: authority](02-locate-authority.md) · [Sources](SOURCES.md)
