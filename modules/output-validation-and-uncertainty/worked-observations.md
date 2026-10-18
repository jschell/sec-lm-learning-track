# Worked observations

Re-inspected locally 2026-10-17 (America/Los_Angeles), Python 3.12.15 / uv 0.12.23. The three authentic trials were originally observed in [CI run 39077441549](https://github.com/jschell/sec-lm-learning-track/actions/runs/39077441549); this module does not run inference again.

## Outcome matrix

| Case | Wire valid | Actual read recorded | Matching feedback | Loop completed | Exact answer | Task passed |
| --- | --- | --- | --- | --- | --- | --- |
| Recorded example 1 | true | true | true | true | false | false |
| Recorded example 2 | true | true | true | true | true | true |
| Recorded example 3 | true | true | true | true | true | true |
| Synthetic broken-feedback copy of example 2 | true | true | false | true | true | true |

Example 1 expects `LAB-092a8a02`; raw answer `092a8a02` remains wrong. The exact task check requires observed reading, an exact answer and loop completion. It does not replace the separate feedback-integration check.

The synthetic row changes one canonical result ID in a saved copy while retaining the actual run's answer and native input. It is a demonstration of a transcript check, not evidence of a model answering without feedback. Do not include it in a trial count or success-rate calculation.

The original retained file remains byte-for-byte unchanged; the [manifest](lab/observation-source.json) records its SHA-256 plus original CI artifact, model hash and runtime revision. No output normalization, prefix repair or dropped failure is used.

## Claim review

| Claim | Object shape valid | References resolve | Authored human-rubric judgment |
| --- | --- | --- | --- |
| 1 | true | true | Supported attributed observation |
| 2 | true | true | Unsupported definitive conclusion |
| 3 | true | true | Warranted uncertainty about conflicting outcomes |
| 4 | true | true | Unsupported absence inferred from missing collection |
| 5 | true | true | Supported collection limit |
| 6 | true | false | Unsupported assertion and absent E99 reference |

The first two columns come from the script. The last is the authored [fixture rubric](lab/rubric.json), not an automatic semantic evaluation or independent learner judgment.

In the transfer variation, claim 3 cites only E03. The reference still resolves; the unrelated health check does not support the sign-in disagreement. The human judgment changes even though the structural check stays green. The answer key's original claim-3 judgment must not be blindly reused after this edit.

[Lesson commands](README.md#setup-and-run) · [Sources](SOURCES.md) · [Validation boundaries](VALIDATION.md)
