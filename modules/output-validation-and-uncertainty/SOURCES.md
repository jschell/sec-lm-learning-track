# Sources and provenance

Checked 2026-10-17 (America/Los_Angeles). Explanations, fixture claims/rubric, inspection code and synthetic variation are original project work under MIT. No external dataset, paper text or upstream implementation is copied.

| Original source | Concept used | Verification scope |
| --- | --- | --- |
| Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), 2026-01-09 | Task/trial/grader distinctions; code-based and human checks | Official article opened; our small fixture is not a reproduced benchmark |
| Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Input/evidence selection background | Official article reopened; original packet provenance in the [context module](../context-and-state/SOURCES.md) |
| Project [decision 0002](../../docs/decisions/0002-feedback-integration-and-model-outcomes.md) | Separate feedback integration from exact-answer outcome | Local decision and retained original case inspected; project policy, not an external author's claim |

## Authentic observations, referenced rather than duplicated

The [retained original selection](../tool-requests-and-feedback/observations/main-2026-10-17.json) comes from [CI run 39077441549](https://github.com/jschell/sec-lm-learning-track/actions/runs/39077441549), original source commit `4cce9b1d4eda9fc894075b86ce6986b287085128`. It contains all three required ordinary/example cases, including the wrong answer. It is available at [immutable repository commit 19ae6e7](https://github.com/jschell/sec-lm-learning-track/blob/19ae6e7fbf53dee3cff6a522b57e39161c74a817/modules/tool-requests-and-feedback/observations/main-2026-10-17.json).

[observation-source.json](lab/observation-source.json) pins the retained file SHA-256 **1680fd217ba306bbbbacd1ba871cba95bfbcd0608762936b927da2bca4d39d8e**, original artifact ID/ZIP hash, model GGUF hash and runtime revision. The ZIP verification was performed when retaining the record; this module verifies the committed JSON bytes, not a fresh download of that ZIP. Model: HuggingFaceTB/SmolLM2-360M-Instruct, Q8_0; runtime revision `f74e2fa6a31cc33ab4ee4ae516641cfe62df3924`. Full original setup/source/license details remain in the [feedback module](../tool-requests-and-feedback/SOURCES.md).

`inspect_validation.py` imports the existing original `decode_wire` and `example_feedback_check` implementations. Importing them does not run their CLI entry points, runtime build or inference. Task outcomes are independently recomputed from raw answer text, recorded reads and stop events using the existing exact-match criteria. The saved task label is shown separately, not trusted as a grade.

Only the generated synthetic copy changes a single canonical result ID in recorded case 2; it is labelled and never passed to a model. The unchanged source remains the evidence for actual model behavior. Re-inspection is not a new trial.

## Authored claims and rubric

The packet is the existing original [context fixture](../context-and-state/lab/fixtures/packet.json), with stable IDs and fictional records. It is loaded from committed files, requiring no previous learner run. The claims and answer key are new authored fixtures. Semantic verdicts in the answer key are human-authored judgments about these fixed claims, not generated scores. Structural validation is intentionally unable to establish entailment.

An edited claim needs fresh review; its old claim ID does not preserve the original rubric judgment. Fixture design, constraints, completion questions and acceptance decisions are project choices.
