# Validation: local tool requests and feedback

Baseline checked 2026-10-16; prompt/model comparison checked 2026-10-17. [Protocol/model sources](SOURCES.md). The compact [baseline record](observations/x86-smoke.json) and [full comparison selection](observations/prompt-comparison.json) are evidence from actual Linux x86_64 inference, not expected output or scripted transcripts.

## Reproduce the checks

```bash
uv run --frozen --offline python -m unittest discover -s modules/tool-requests-and-feedback/lab/tests -v
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/run.py --output .cache/feedback-check
```

Eighteen contract/regression tests pass locally with synthetic fixtures and the retained original CI failure. They cover strict parsing without repairs, matching feedback projection, raw-output retention, schema opt-in, stops, actual scripted reads, unavailable tools, examples, and separate integration/task requirements. They reject dropped canonical/native feedback and mismatched IDs without relabeling the recorded wrong answer. These tests do not perform inference. Generation setup separately checks explicit model selection and the selected artifact's hash before replacement.

Actual inference requires [prepared runtime/model assets](../generation-and-sampling/README.md). The verifier starts and stops its own loopback server; no running instance is assumed:

```bash
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/verify_model.py > .cache/tool-feedback-observations.json
```

This emits full bounded inputs, outputs, normalized responses and tool results. Each model receives the four original conditions and three fresh tasks for each prompt-style/generation combination. CI retains the outputs as artifacts. The verifier asserts that actual completions were received without input truncation, the output limit maps correctly, and omitted/capped tools do not read successfully. Default verification can finish successfully with explicitly recorded task failures; that is an API/containment check.

After explicitly preparing the 360M model, standard real-model CI requires three actual ordinary/example read-and-feedback exchanges:

```bash
uv run --frozen --group generation-setup python modules/generation-and-sampling/lab/prepare.py --model 360m --jobs 1
uv run --frozen --offline python modules/tool-requests-and-feedback/lab/verify_model.py --model 360m --require-feedback > .cache/tool-feedback-360m-observations.json
```

The integration requirement verifies actual file contents, matching call/result IDs, the following canonical request, returned data in projected/formatted input, a native response and a completed loop. Exact-answer `task_passed` values remain unchanged; CI separately displays their counts. Green integration does not establish accuracy. Rationale and the failed main run are recorded in [decision 0002](../../docs/decisions/0002-feedback-integration-and-model-outcomes.md).

The optional strict `--require-example-task` flag still requires all three ordinary/example exact answers to pass; it can be combined with `--require-feedback`. Failed/missing required cases cause exit 1 **after** printing observations. CI uploads artifacts even if a check fails. No model fallback or answer repair occurs.

## Actual baseline observed

CPU: Linux x86_64, AMD EPYC 9V74, two inference threads, 1024-token context. Python 3.12.14. Exact runtime/model/hash in the record and [setup manifest](../generation-and-sampling/lab/setup.json). No physical Pi 4, GPU or hosted inference used.

| Condition | Native behavior | Loop/result |
| --- | --- | --- |
| Ordinary text generation | Repeated format examples until 128-token cap | `model_stop:max_tokens`; no reads; task failed |
| Schema-constrained generation | Produced valid `read_file` requests, including after receiving the actual code | Two successful reads, third proposal blocked by `tool_limit`; no final answer; task failed |
| Tool omitted from definitions/permissions; same grammar | Still proposed `read_file` | Dispatch returned unknown/disabled-tool errors; no successful read; task failed |
| One-token constrained output | Generated `{` then reached cap | `model_stop:max_tokens`; no dispatch; task failed |
| Scripted comparison (not a model) | Requested read, constructed answer from matching actual feedback | One successful read and exact code; task passed |

The constrained model reached the real tool/feedback boundary. Grammar improved output format but did not produce a successful use of feedback in this baseline. These records are limited to the stated prompt/template/decoder/model combinations.

## Prompt and model comparison

The original baseline is retained above. A fixed authored exchange was then added as `example`; the `copy-line` variant adds one instruction paragraph clarifying the entire line, its prefix and the result-content field. Only these explicit variants were explored; this is not an automatic prompt optimizer. [Brown et al.](https://arxiv.org/abs/2005.14165v4) supplies the text-demonstration concept, not evidence of performance for our models.

All exploratory attempts are preserved in [the comparison record](observations/prompt-comparison.json), including an early 135M exact success, copying a tool-call ID, omitted prefixes and copying the example answer without a read. These outcomes were not repaired or removed. The final comparison used the same pinned CPU runtime, Q8 format, two threads, 1024-token context, greedy setting and task/independent check for both models:

| Prompt / generation | 135M exact task passes | 360M exact task passes |
| --- | --- | --- |
| `example`, ordinary | 0 of 3 | 3 of 3 |
| `example`, constrained | 0 of 3 | 3 of 3 |
| `copy-line`, ordinary | 0 of 3 | 3 of 3 |
| `copy-line`, constrained | 0 of 3 | 1 of 3 |

These are counts from the captured small smoke comparison, not estimates of general success rates. Both models without an example still failed the task in the captured baseline conditions. The final 135M `example` attempts read correctly but omitted `LAB-`; `copy-line` instead copied `LAB-example` without reading. The 360M `example` runs made one actual read and returned the exact fresh code in all six ordinary/constrained attempts. The extra clarification was not consistently helpful. A further full verifier run with `--require-example-task` passed all three newly generated ordinary/example tasks; that run and its other outcomes are preserved under `recipe_verification` in the record.

The local demonstration uses **360M plus `example`, ordinary generation**: six of six fresh tasks passed across the earlier local comparison and recipe recheck. The example/constrained condition passed only two of three tasks in the recheck, despite passing three earlier. The later merged-main failure below limits any dependability claim. Baseline 135M still serves the sampling/failure lessons. The 360M asset was explicitly downloaded and checked against [its separate manifest](../generation-and-sampling/lab/setup-360m.json); it did not replace the baseline file. Both retain Apache-2.0 notices. Native trained function calling is not being tested.

## Later merged-main failure

[Run 39077441549](https://github.com/jschell/sec-lm-learning-track/actions/runs/39077441549), at merge commit `4cce9b1d4eda9fc894075b86ce6986b287085128`, failed its then-required perfect-copy check. All three cases made an actual read and supplied matching feedback before completing. Exact outcomes were:

| Case | File line | Actual final answer | Exact task |
| --- | --- | --- | --- |
| example_ordinary_1 | LAB-092a8a02 | 092a8a02 | Failed |
| example_ordinary_2 | LAB-3e78cca6 | LAB-3e78cca6 | Passed |
| example_ordinary_3 | LAB-19c133b0 | LAB-19c133b0 | Passed |

The [retained original selection](observations/main-2026-10-17.json) includes raw outputs, IDs, feedback, formatted input, the failed strict check, run/commit and verified artifact ZIP hash. Applying the feedback-integration checker to it passes all three exchanges; the unchanged exact task checker still fails. The original CI run remains a failed strict-task observation. [Decision 0002](../../docs/decisions/0002-feedback-integration-and-model-outcomes.md) changes standard CI's contract and exposes both outcomes instead of promising perfect model copying. This is not a newly successful model run or a repaired answer.

Each attempt had a fresh code and call ID, so these runs are not identical-input paired trials. Model training, weights and architecture differ; the table does not isolate parameter count as a cause. No broad model recommendation, security claim, inference about hidden reasoning, or physical Pi performance follows from these observations.

Setup correction observed during this work: UI compilation being off did not disable the runtime's optional prebuilt UI fetch. The corrected build disables both, and a local rebuild embedded zero UI assets while completing actual inference. Original CMake/source references are in [generation sources](../generation-and-sampling/SOURCES.md). This does not turn an existing Linux environment into a fresh-OS/Pi validation.

## Still open

- An independent learner walkthrough and explanation of the trace boundaries.
- More learner/task diversity and repeatability across machines; the bounded 360M/example recipe is now observed, not a general agent capability.
- Native llama.cpp function-calling compatibility/behavior, which this custom wire exercise does not test.
- Physical Pi 4 fresh setup, RAM, setup time, inference latency and task outcome, shared with [generation validation](../generation-and-sampling/VALIDATION.md).
- Prompt-injection resistance and external provider behavior; neither is evaluated here.

This lesson has a scripted worked exchange, an observed local-model working configuration, and bounded failure comparisons. The 135M baseline is **not** validated as a dependable autonomous read-and-answer agent.
