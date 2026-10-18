# Plan 09: Output validation and uncertainty

Status: implementation complete; two offline worked lessons, authentic-trace re-inspection and authored claim rubric are supplied. Independent learner review remains open. See [module](../../../modules/output-validation-and-uncertainty/README.md) and [validation](../../../modules/output-validation-and-uncertainty/VALIDATION.md).
Estimated learner effort: two 30–45-minute modules; project estimate.
Prerequisites: inspect a tool trace and small JSON records. Supply all inputs; no model download or credentials required.

## Learning question

Which checks establish formatting, execution, feedback, task correctness and evidential support, and which conclusions remain unresolved?

## Worked modules

1. **Separate outcomes.** Use a small selected set of retained local-model traces, including a completed feedback exchange with a wrong exact answer. Predict each grade; inspect parsing, actual read, matching feedback, completion and answer correctness separately. Reuse [decision 0002](../../decisions/0002-feedback-integration-and-model-outcomes.md) and its unchanged exact-answer criteria. Vary one seeded defect in a labelled synthetic copy; keep the authentic record untouched.
2. **Check claims.** Supply a small event packet with stable IDs, a known gap and a contradiction, plus authored supported, unsupported and appropriately limited statements. Compare claims to evidence with a visible fixture rubric. Include a seeded unsupported assertion that is well formatted. Require a learner explanation of the missing support and a revision that states the limit. Automated checks can verify IDs and known fixture facts; open-ended claim support still needs a stated human rubric.

Task, trial and grader distinctions use [Anthropic's original evaluation discussion](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). These small exercises teach checking, not statistically reliable model ranking. Fixture construction and the claim rubric are original project design.

## Starting state and artifacts

Implement under `modules/output-validation-and-uncertainty/`. Supply authentic observation references, small labelled synthetic variants, packet, rubric, complete grader example and worked outcome table. Reuse existing records by reference or an explicitly sourced minimal extract; preserve model/runtime provenance. Do not duplicate large trace archives or build a leaderboard harness.

The learner writes an outcome matrix and a short supported/unsupported/uncertain claim review with evidence IDs. Full reconstruction and model-as-judge are optional later comparisons, not prerequisites. Live reruns, if offered, record fresh outcomes separately from the supplied observations.

## Acceptance

- [x] Predict, run, inspect, vary and explain sequence in two independently runnable units.
- [x] A schema-valid wrong answer and a completed wrong task remain graded as incorrect by the relevant check.
- [x] Feedback integration and exact-answer accuracy remain distinct; failure evidence is neither repaired nor removed.
- [x] Authored rubric identifies seeded unsupported claims and collection-gap misuse; independent learner detection is not yet observed.
- [x] Fixture checks, human judgments and actual model observations are labelled separately.
- [x] Completion includes a learner explanation of what each check cannot establish.
- [x] Source attribution, meaningful regression checks and validation records supplied; independent pilot not implied.

## Boundaries

Synthetic evidence and existing public project observations only. No confidence score treated as calibrated probability, broad model benchmark, new hosted call, production detection-effectiveness claim or mandatory LLM reviewer. Reuse [Track 4](../../../tracks/04-validation/README.md) concepts; rule conversion and consulting findings remain later applications.

## Sources

[Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), topic checked 2026-10-17; [project decision 0002](../../decisions/0002-feedback-integration-and-model-outcomes.md) and [local observations](../../../modules/tool-requests-and-feedback/VALIDATION.md) for this repository's actual cases. Authoring must verify selected cases and preserve their provenance. Exercises and acceptance criteria are project choices.
