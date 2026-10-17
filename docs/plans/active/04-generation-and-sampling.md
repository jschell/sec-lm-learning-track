# Plan 04: Generation and sampling

Status: active implementation/validation. [Lesson](../../../modules/generation-and-sampling/README.md) and [validation checklist](../../../modules/generation-and-sampling/VALIDATION.md).

## Accepted scope

SmolLM2-135M-Instruct is selected as the small educational baseline; it needs to be useful for the instruction and bounded task, not comparable in general coverage with state-of-the-art models. A 360M comparison is a fallback only if a lesson objective cannot be demonstrated.

Start from a blank slate. Provide system prerequisites, uv environment, pinned CPU runtime build, model download and license/hash verification, server startup and observation commands. Do not assume an installed/runtime server merely because the model choice is settled. Keep setup separate from the conceptual exercise and inference available without an external provider account.

## Implementation and acceptance

- Authored score-vector calculation illustrates softmax, temperature, top-k and sampling.
- Native runtime observations expose actual token IDs, selected/candidate probabilities, input formatting, stop reasons and timings. Do not call partial top-N probabilities raw logits or silently renormalize them.
- Fixed synthetic reply, extraction and rewrite tasks provide checkable outputs; record success and failure without inventing model competence.
- Vary one setting, repeat a seed, and observe both EOS and a token cap.
- Pin model lineage/quantizer/runtime, preserve licenses, provide reproducible Python 3.12+/uv commands, and keep downloaded/build artifacts outside git.
- Validate fresh setup and API compatibility, model suitability, actual resource needs and physical Pi 4 operation as separate evidence items. A local x86 check or synthetic contract test cannot satisfy Pi/learner validation.

The lesson, setup scripts, client, arithmetic and contract tests are authored. Actual build/model evidence belongs in the module validation record; keep this plan active while explicit validation items remain open. No model leaderboard, training implementation or general-purpose agent requirement is added.

## Original sources

[Karpathy Deep Dive](https://www.youtube.com/watch?v=7xTGNNLPyMI), [makemore](https://github.com/karpathy/makemore), [SmolLM2 publisher](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct), and the pinned [runtime/model source record](../../../modules/generation-and-sampling/SOURCES.md). Scope, acceptance and exercises are project choices.
