# Observe a hosted model: read-only experiments

Status: hosted exercise authored and controller checks tested; these Anthropic/OpenRouter runs have not been observed by the authors. Estimated effort: 20–40 minutes after provider setup. No Docker is needed.

For an actual model run without provider credentials, use the separately validated [local CPU route](../../modules/tool-requests-and-feedback/README.md). It reuses the reference loop through a teaching JSON text adapter, with its own model/runtime setup. It does not exercise the hosted Messages endpoint described here. [Local evidence and limits](../../modules/tool-requests-and-feedback/VALIDATION.md).

Provider credentials are trimmed around their edges and must be single printable ASCII tokens without internal whitespace. Configuration/transport diagnostics do not echo the credential. Short stages 1/2 are replay-only; the live routes here use the guarded reference, as does `stage 3 --live`.

## Goal and prerequisites

Compare your prediction with a real model's tool selection and response to missing information. Understand [the core loop](core-loop.md) first. Complete the Python/uv setup in the [track entry](README.md).

The tool-feedback protocol is documented by [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). OpenRouter supplies a documented [compatible Messages endpoint](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message). The experiments and observation worksheet below are original project teaching design.

## Provider setup

Choose one provider and set its key using your normal terminal secret handling. Do not paste keys into files or commit them.

| Provider | Credential variable | Model selection |
| --- | --- | --- |
| anthropic | ANTHROPIC_API_KEY | Account-accessible tool-capable Anthropic model ID |
| openrouter | OPENROUTER_API_KEY | OpenRouter model ID with documented tool support |

For the commands below, set LAB_PROVIDER to anthropic or openrouter and LAB_MODEL to your selected model ID. These are non-secret selectors. The CLI reads only the selected provider's key; it never falls back to the other key.

Live inference sends the synthetic prompt, tool definitions, and results to that provider (and its downstream provider for OpenRouter) and may incur charges. `uv --offline` prevents uv downloads, not the Python program's HTTP calls. Fixed endpoints reject redirects; keys are excluded from traces and tools. This text/client-tool lab stops on unsupported blocks, including thinking blocks. Select a model/response mode that returns ordinary text and client-tool blocks; unsupported blocks are not silently removed.

## Predict, run, inspect

Write a prediction before each run. Every invocation starts with fresh synthetic fixtures; changing settings between runs does not preserve conversation history.

```bash
uv run --frozen --offline python learn.py --live --provider "$LAB_PROVIDER" --model "$LAB_MODEL" --read-only --task inspect --max-turns 4 --max-calls 6
```

Predict which tool will read notes.txt. Inspect the printed trace path using `learn.py trace PATH`. Check whether the answer identifies the file and reports FizzBuzz. A model may answer without a tool; that is an observation, not proof it read the evidence.

```bash
uv run --frozen --offline python learn.py --live --provider "$LAB_PROVIDER" --model "$LAB_MODEL" --read-only --task inspect --omit-tool read_file --max-turns 4 --max-calls 6
```

Predict whether it will use code_search, call a removed tool, or report insufficient access. The omitted tool is removed from both discovery and dispatch. Valid alternatives are allowed; the result is not a leaderboard score.

```bash
uv run --frozen --offline python learn.py --live --provider "$LAB_PROVIDER" --model "$LAB_MODEL" --read-only --task missing-file --max-turns 4 --max-calls 6
```

Find any failed read and its is_error result in the next request. Does the model disclose the failure, try another tool, or invent content? It need not choose the same path across runs.

## Observation worksheet

| Run | Prediction | Calls actually requested | Result / error supplied | Answer supported by evidence? |
| --- | --- | --- | --- | --- |
| Full read-only tools | | | | |
| read_file omitted | | | | |
| Missing file | | | | |

Record provider/model, trace path, stop status, and uncertainties. Trace data shows observable messages, not private reasoning. Do not infer general model reliability from these three experiments.

## Completion levels

- **Controller familiarity:** offline worked stages/replay, error and limit checks, and explanation of a trace. No API credentials required.
- **Observed hosted-model behavior:** run the experiments above and complete the worksheet. The separate local route provides local-model evidence; neither route is a prerequisite for using the offline lessons.

## Optional live repair

Only after checking the Docker path described in the [execution lesson](04-complete-a-task.md):

```bash
uv run --frozen --offline python learn.py --live --provider "$LAB_PROVIDER" --model "$LAB_MODEL" --task repair --execute
```

This enables writes and contained commands; it cannot be combined with --read-only. The default controller limit is 12 requests, each with max_tokens=1024; it is not a hard dollar budget. No automatic inference retry occurs.

## Troubleshooting

A missing-key message names the expected environment variable. HTTP errors report the status/category, bounded JSON error fields and a request ID when available. The selected credential and bearer/key patterns are redacted; non-JSON or oversized bodies are not printed. Treat diagnostics as synthetic lab data, not a production redaction guarantee. A model_stop/error status may indicate an unsupported response feature, not a defect in your tool. Inspect the trace and report the limitation rather than bypassing controls.

[Track entry](README.md) · [Sources](SOURCES.md) · [Validation](VALIDATION.md)

## Bounded smoke-test record

Run inspection, omitted read_file, and missing-file tasks above with one account-accessible text/tool model. Keep each run at four turns and six calls, inspect the actual requests, and record provider/model, terminal status, error diagnostics and supported behavior in the worksheet. Add the optional [injection observation](07-untrusted-content.md) only after those exchanges work. Stop on protocol errors; do not retry indefinitely or discard unknown blocks. These request limits do not impose a hard dollar cap.

No hosted smoke test was possible during the corrective review because neither provider credential was configured. That outstanding validation is explicit in [VALIDATION.md](VALIDATION.md); mocked responses and local-model observations do not satisfy it.
