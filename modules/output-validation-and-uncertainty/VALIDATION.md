# Validation record

Local author check: 2026-10-17 (America/Los_Angeles), Python 3.12.15 / uv 0.12.23. No inference, model build, network retrieval or semantic model reviewer is used.

```bash
uv run --frozen --offline python -m unittest discover -s modules/output-validation-and-uncertainty/lab/tests -v
uv run --frozen --offline python -m unittest discover -s modules/tool-requests-and-feedback/lab/tests -v
```

## Performed

- Nine new tests pass: valid/completed wrong answer, independence from the saved task label, one-ID synthetic feedback defect, invalid duplicate-key wire text, source preservation, source-hash rejection, valid-but-unsupported references, malformed claim shape versus unresolved ID, and CLI worksheet creation/overwrite refusal.
- Eighteen existing feedback-module tests pass. The parser, feedback checker and loop are unchanged.
- Both documented lesson entry points run, producing the [worked outcome matrix](worked-observations.md), structural claim report and blank review worksheet.
- The citation transfer variant was run: changing only claim 3's citations to E03 leaves the structural reference check true. Its semantic defect is explained manually, not assigned an automatic score.
- Original retained bytes still match the recorded manifest hash after inspection/mutation-copy creation. No historical answer or grade was repaired.

[Validation CI](../../.github/workflows/validation.yml) runs the new and existing feedback tests plus both entry points on Python 3.12/3.13. Actual CI conclusions must be read from the runs; configuration alone is not a successful observation.

## Scope and open evidence

| Evidence | Status |
| --- | --- |
| Deterministic re-inspection of authentic traces | Checked; no new model trial |
| Labelled synthetic defect | Checked separately; never inference evidence |
| Structural claim references | Checked against fixed packet IDs |
| Semantic fixture rubric | Authored judgments supplied; no automatic semantic grade |
| Independent learner prediction/explanation/revision | Pending |
| Fresh OS / physical Pi / hosted-provider behavior | Not observed here |

Author checks do not establish learner understanding, calibrated uncertainty or operational investigation effectiveness. The existing context packet is provided by the repository, not inherited from a learner's unfinished work. [Original sources and provenance](SOURCES.md).
