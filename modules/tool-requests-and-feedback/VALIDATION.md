# Validation: local tool requests and feedback

Checked 2026-10-16. [Protocol/model sources](SOURCES.md). The compact [actual observation record](observations/x86-smoke.json) is evidence from Linux x86_64 with the pinned 135M Q8 model, not expected output or a scripted transcript.

## Reproduce the checks

```bash
uv run --frozen --offline python -m unittest discover -s modules/tool-requests-and-feedback/lab/tests -v
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --output .cache/feedback-check
```

Nine synthetic contract tests passed locally. They cover strict parsing without repairs, duplicate keys, matching feedback projection, raw-output retention, explicit schema opt-in, stop/context handling, no dispatch from capped output, actual scripted reading, unavailable tools, and separation of task correctness from conversation completion. They do not measure a model.

Actual inference requires [prepared runtime/model assets](../generation-and-sampling/README.md). The verifier starts and stops its own loopback server; no running instance is assumed:

```bash
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/verify_model.py > .cache/tool-feedback-observations.json
```

This emits full bounded inputs, outputs, normalized responses and tool results. CI retains this as an artifact. The verifier asserts that actual completions were received without input truncation, the output limit maps correctly, and omitted/capped tools do not read successfully. Model task failure is an explicit report field, not an infrastructure assertion disguised as model success. A CLI task failure exits 1; the verifier can finish successfully with recorded task failures.

## Actual baseline observed

CPU: Linux x86_64, AMD EPYC 9V74, two inference threads, 1024-token context. Python 3.12.14. Exact runtime/model/hash in the record and [setup manifest](../generation-and-sampling/lab/setup.json). No physical Pi 4, GPU or hosted inference used.

| Condition | Native behavior | Loop/result |
| --- | --- | --- |
| Ordinary text generation | Repeated format examples until 128-token cap | `model_stop:max_tokens`; no reads; task failed |
| Schema-constrained generation | Produced valid `read_file` requests, including after receiving the actual code | Two successful reads, third proposal blocked by `tool_limit`; no final answer; task failed |
| Tool omitted from definitions/permissions; same grammar | Still proposed `read_file` | Dispatch returned unknown/disabled-tool errors; no successful read; task failed |
| One-token constrained output | Generated `{` then reached cap | `model_stop:max_tokens`; no dispatch; task failed |
| Scripted comparison (not a model) | Requested read, constructed answer from matching actual feedback | One successful read and exact code; task passed |

The constrained model reached the real tool/feedback boundary. Grammar improved output format but did not produce a successful use of feedback. The result is limited to this prompt/template/decoder/model combination; it does not isolate whether different prompting or another model would succeed. No repeated trials or general capability estimate are claimed. Development also exposed that separate sandboxed command sessions here cannot share loopback sockets; recorded inference uses one verifier process with its child server, avoiding that environment-specific limitation.

## Still open

- An independent learner walkthrough and explanation of the trace boundaries.
- A model/prompt configuration completing the actual read-and-answer task; retain this failed baseline when testing an explicit 360M comparison. No automatic model switch.
- Native llama.cpp function-calling compatibility/behavior, which this custom wire exercise does not test.
- Physical Pi 4 fresh setup, RAM, setup time, inference latency and task outcome, shared with [generation validation](../generation-and-sampling/VALIDATION.md).
- Prompt-injection resistance and external provider behavior; neither is evaluated here.

This lesson is usable as a bounded diagnosis exercise and a scripted worked exchange. The baseline is **not** validated as a successful autonomous read-and-answer agent.
