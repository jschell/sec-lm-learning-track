# From generated text to tools and feedback

Status: runnable lesson; actual baseline failures recorded in [validation](VALIDATION.md).
Estimated effort: 30–45 minutes after runtime setup (project estimate).
Prerequisites: Python 3.12+, uv, and [the loop on one page](../../tracks/01-author-the-loop/core-loop.md). Complete reference code is supplied; no learner-authored loop is required.

## Goal

Trace where generated text becomes a requested action, where Python actually reads a file, and where that result enters the next inference. Distinguish valid output format, valid dispatch, use of feedback, and task success.

This continues [Geoffrey Huntley's inference/tool-feedback progression](https://ghuntley.com/agent/). The local wire format and exercise below are project designs, not Huntley's implementation or a standard provider protocol.

## What the bridge does

The model sees a description of `read_file` and a request to read `status.txt`. It generates text. Our adapter accepts exactly one of these shapes:

```json
{"tool":"read_file","path":"status.txt"}
```

```json
{"answer":"LAB-example"}
```

`LAB-example` is an illustration. Each exercise creates a different synthetic code in a new file; the initial model request does not contain the answer.

In [bridge.py](lab/bridge.py), `decode_wire` translates the first shape into the existing loop's `tool_use` block and assigns a fresh call ID. The unchanged [Track 1 run_loop](../../tracks/01-author-the-loop/lab/loop.py) dispatches the call through `Tools`, appends a result with the matching ID, and requests inference again. `wire_messages` exposes that result as labeled user-role data in the model's next formatted input. The final JSON shape becomes an ordinary text block. Client execution and matching tool results are also the separation used in [Anthropic's client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls); our text projection is an explicit teaching simplification.

The bridge uses native llama.cpp `/apply-template`, `/tokenize` and `/completion` endpoints. It does **not** implement or test llama.cpp's [native function-calling API](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/docs/function-calling.md). Tool definitions, action text, call IDs and feedback are all visible in the trace. No code executes merely because the generated text mentions a file.

## Run the complete comparison first

From the repository root, install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed, then:

```bash
uv python install 3.12
uv sync --frozen
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --output .cache/feedback-replay
```

This scripted comparison makes no model/network call. It requests the file and then constructs an answer from the **actual returned contents**. Expect `successful_reads: 1`, `loop_status: completed`, and `task_passed: true`. The code is fresh each run. Use a new output directory for every command; existing directories are never overwritten.

Inspect `.cache/feedback-replay/trace.jsonl`. Find the initial `request`, `response` requesting `read_file`, the `tool` event, and the following `request`. Match the call/result IDs and locate the new code in that second request. Read the small `ScriptedExchange.complete` implementation: its fixed progression explains why this is a loop/feedback comparison rather than evidence about a model.

## Start local inference from a blank slate

No existing model or server is assumed. These are the same pinned CPU assets used by [generation and sampling](../generation-and-sampling/README.md); reuse that cache if already prepared. On Debian/Ubuntu or 64-bit Raspberry Pi OS, install prerequisites and prepare:

```bash
sudo apt update
sudo apt install -y build-essential git curl ca-certificates
uv sync --frozen --group generation-setup
uv run --frozen --group generation-setup python modules/generation-and-sampling/lab/prepare.py --jobs 1
```

Preparation builds pinned llama.cpp and downloads/hash-checks the roughly 145 MB SmolLM2-135M-Instruct Q8 model, retaining notices. It requires network access and additional build space. The original [setup manifest](../generation-and-sampling/lab/setup.json) and [source record](../generation-and-sampling/SOURCES.md) identify every asset. Physical Pi 4 operation remains unvalidated.

In terminal A, start the foreground server:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/serve.py --threads 2
```

In terminal B, run ordinary generation and then constrain only the output syntax:

```bash
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --mode live --output .cache/feedback-live
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --mode live --constrain --output .cache/feedback-json
```

If port 8080 is occupied, start the server with `--port 8091` and add `--base-url http://127.0.0.1:8091` to each live command. Ctrl-C in terminal A stops the server. Initial setup needs network access; prepared inference stays on loopback and needs no API key.

## Predict, inspect and vary

Before opening the live traces, predict whether a valid JSON reply will also produce a correct answer. Look for `local_request` (formatted input and native parameters), `local_response` (unmodified native response), normalized `response`, actual `tool`, and final `stop` events. A raw response is retained even when parsing fails. No prose stripping, argument guessing or automatic retry hides the model's output.

`--constrain` sends `json_schema` to llama.cpp. The runtime masks output choices to fit its supported schema grammar; the schema is not automatically part of the prompt, so the adapter also describes the format in text. This follows the pinned [llama.cpp grammar guide](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/grammars/README.md#json-schemas--gbnf). A grammar can restrict shape while the model still chooses the wrong action, path or answer.

Actual recorded baseline: ordinary output repeated formatting instructions until the output cap. Constrained output requested `status.txt` and the tool read it, but subsequent generations requested it again instead of using the returned code. The loop stopped at its two-call budget. Both runs failed the task. These are observations of this model, prompt, quantization and runtime—not a general claim about all small models. See [the captured record](observations/x86-smoke.json).

Vary one condition at a time:

```bash
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --mode live --constrain --without-tool --output .cache/feedback-no-tool
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --mode live --constrain --max-tokens 1 --output .cache/feedback-limit
```

Omitting the tool removes it from both advertised definitions and dispatch permissions. For this experiment the output grammar still permits a read-shaped proposal: observe whether one is generated and how dispatch rejects it. This demonstrates why tool advertisement and output grammar are not authorization. The one-token run should preserve partial text in `local_response`, stop as `model_stop:max_tokens`, and perform no read.

Optional modification: shorten or reword `PROTOCOL` in a separate copy/branch and compare the traces. Preserve the original failed runs; report a prompt change separately from a model change. A stronger model comparison is a subsequent validation item, not a silent replacement of this baseline.

## Completion check and diagnosis

You can finish this lesson even if the live model fails. Explain, with trace events, whether it failed at formatting, argument/path validation, dispatch, using feedback, or final accuracy. Show the returned code in the next formatted input; identify which component assigned the call ID. Demonstrate a successful scripted exchange and a bounded live attempt. Explain why `completed`, schema-valid output, and `task_passed` differ. Human explanation is not graded by the automated tests.

The CLI exits 0 for a passed task, 1 for a recorded failed attempt, and 2 for setup/argument failure. An ordinary live failure is expected in the captured baseline. `report.json` contains the independent check: a successful actual read **and** the exact final code, with the loop completed. No final answer means `null`; a tool request is not a final answer.

Connection errors: start the prepared server and match ports. Protocol errors: inspect `local_response` and the subsequent `error`. Input beyond 768 tokens or server-reported context truncation is rejected explicitly. Output caps are normalized before parsing, so partial proposals never dispatch. A schema error from the server calls for checking the pinned build, not pretending that inference succeeded.

## Boundaries and optional depth

Only a freshly created synthetic workspace is exposed, with `read_file` as the sole permitted action. No shell, edits, hosted credentials, customer data or external tool destinations. Each attempt has at most three inference turns, two tool dispatch attempts and 128 generated tokens per turn. Traces include full bounded requests for inspection and can grow with conversation length; this is not a production logging design.

> **What this proves:** the scripted path checks a concrete feedback exchange, and actual observations show this baseline's behavior through an explicit text adapter. Neither demonstrates native function-calling competence, prompt-injection resistance, Pi 4 performance or learner understanding.

> **Optional original resource:** [Huntley's coding-agent workshop](https://ghuntley.com/agent/) explains the small inference loop. [llama.cpp's function-calling documentation](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/docs/function-calling.md) provides a later comparison with trained/tool-template integration. This lesson does not require either external reading to run.

[Sources and adaptations](SOURCES.md) · [Validation](VALIDATION.md)
