# Validation record

Checked 2026-10-17 on the author environment, Python 3.12.15 / uv 0.12.23. This record distinguishes implementation from learning effectiveness.

## Performed

- Seven context tests pass: actual read and matching feedback, immutable request snapshots/counterfactual copy, selection loss/zero hits, summary omission and explicit loading, IDs without anchors, a semantic counterexample that intentionally passes the literal checker, Unicode sizes, and subprocess persistence/overwrite refusal. Several checks share a test method.
- Existing Track 1 suite: 43 tests pass after importing its worked exchange and file/trace primitives. No existing loop code changed.
- All three documented lesson commands run with fresh output directories. The transfer query `collection gap` retains C01 and omits E01/E02 as documented. [Worked observations](worked-observations.md) records actual local outcomes.
- The command environment was already prepared; no claim of a fresh OS installation or independent setup pilot.

Reproduce from the repository root after setup:

```bash
uv run --frozen --offline python -m unittest discover -s modules/context-and-state/lab/tests -v
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
```

[Context CI](../../.github/workflows/context.yml) runs contracts and the three entry points on Python 3.12/3.13. Its results are separate from this local record; do not infer a completed run from workflow configuration.

## Evidence boundaries and open checks

| Evidence | State |
| --- | --- |
| Worked examples, deterministic inspection and actual read-only file access | Locally checked |
| Model behavior / automatic summarization | Not performed; no model is called or needed for these input-inspection objectives |
| Semantic faithfulness | Human fixture rubric supplied; literal checker is deliberately insufficient and its counterexample is tested |
| Independent learner prediction/explanation/transfer | Pending; author walkthrough is not a learner pilot |
| Physical Pi / fresh OS | Not performed; no new hardware or inference-portability claim |
| Hosted API / native token formatting / KV cache | Not exercised |

The [sources](SOURCES.md) support the conceptual mechanisms. Synthetic inputs and checks are project design; passing these checks does not prove understanding or real-world incident conclusions.
