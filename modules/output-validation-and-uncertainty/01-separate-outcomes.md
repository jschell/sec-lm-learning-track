# 1. Separate outcomes

Goal: explain why formatting, actual reading, matching feedback, loop completion and task correctness need separate checks.

A grader checks a stated aspect of an outcome or trajectory. Several checks can apply to the same trial; [Anthropic's original evaluation explanation](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) supplies these terms. This lesson's exact-copy task and criteria are project design, recorded in [decision 0002](../../docs/decisions/0002-feedback-integration-and-model-outcomes.md).

## Predict and run

The task is to read a fresh code from `status.txt` and return that entire code. In retained case `example_ordinary_1`, the expected code is `LAB-092a8a02` and the raw final model text is:

```json
{"answer":"092a8a02"}
```

Predict which checks should pass. Should a missing prefix invalidate the tool/feedback exchange, the exact answer, or both?

From the repository root after [setup](README.md#setup-and-run):

```bash
uv run --frozen --offline python modules/output-validation-and-uncertainty/lab/inspect_validation.py outcomes --output .cache/validation-outcomes-1
```

Open the generated `report.json`. For the first case, valid wire format, successful read, matching feedback and loop completion all pass. The exact-answer/task checks fail. No prefix repair, answer trimming, retry or success-label override is used. The task check requires an observed successful read, an exact answer and a completed loop; it is separate from the feedback check.

## Inspect the evidence

Open [the retained source JSON](../tool-requests-and-feedback/observations/main-2026-10-17.json), then `runs.example_ordinary_1`:

1. `local_response` contains raw wire text. The existing strict parser checks its complete object shape; parsing does not establish correctness.
2. `tool` records the read and actual returned code. Its successful flag alone is not an exact-answer grade.
3. The following `request` contains matching call/result IDs. The next `local_request` includes that feedback in projected messages and formatted input. The existing feedback grader checks those transitions.
4. The final `stop` says `completed`. The last raw answer still omits `LAB-`.

The script computes the answer check from raw response text and expected fixture contents, not from the saved `task_passed` label. Its report includes that old label separately for comparison. The source-file hash is checked before inspection; a changed source requires an explicit provenance review.

## Vary one factor

The same command creates `synthetic-broken-feedback.json` from the recorded second, successful case. It changes **only** the result ID in the following canonical request. Original source, actual tool-event result, projected native input and raw model responses remain unchanged. This derived copy is never submitted to a model or provider and is not a new trial.

Now the feedback check fails, while the retained exact answer and task-outcome check remain true. This does not show that a model answered correctly without feedback: its actual run had matching feedback. It shows that a checker looking only at the final answer misses this deliberately introduced transcript defect.

## Explain and check

- Locate the failed exact comparison and the actual successful read in case 1. Why are their grades different?
- Locate the sole changed ID in the synthetic copy. Why must this copy not be counted as another model observation?
- Which requirement would an application depending on exact code copying need to enforce?
- Would any of these checks demonstrate private reasoning, general reliability, or support for a security finding?

Expected: answer correctness and feedback integration can fail independently. Use the checks required by the stated objective; preserve unsuccessful outcomes. These three selected trials cannot establish a general success rate. [Worked observations](worked-observations.md) gives the full small matrix.

[Next: claims](02-check-claims.md) · [Source provenance](SOURCES.md)
