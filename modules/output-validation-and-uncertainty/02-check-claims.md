# 2. Check claims

Goal: distinguish resolvable references from claims supported by the referenced evidence, and preserve uncertainty when collection is incomplete.

Code checks can verify fixed structural conditions; human review can apply a stated rubric to meaning. [Anthropic's evaluation article](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) describes code-based and human graders and their different limits. Our structural checker and six-claim rubric are deliberately small project examples, not a general truth detector.

## Predict and run

Read [the synthetic packet](../context-and-state/lab/fixtures/packet.json). E01 reports failure; E02 reports success for the same attempt. Their disagreement is unresolved. C01 records unavailable application-audit coverage at 10:02–10:05 UTC. E03 is an unrelated health check. These are invented records, not a real engagement.

Open [claims.json](lab/claims.json). Predict which claims have valid references and which conclusions are supported. Then:

```bash
uv run --frozen --offline python modules/output-validation-and-uncertainty/lab/inspect_validation.py claims --output .cache/validation-claims-1
```

Inspect `report.json`, `evidence.json` and the blank `claim-review.md` in the output directory. The automatic check verifies object shape and that cited IDs exist in this packet. It assigns no semantic verdict. Claims 1–5 have resolvable references; claim 6 cites absent E99.

Claim 2 cites E01, E02 and C01, yet asserts that the attempt definitely failed and no successful activity occurred. All citations resolve, but they do not support that conclusion. Claim 4 turns a collection gap into a claim of no activity. A valid object with valid references can therefore still be wrong.

## Apply the human rubric

For each claim, record whether it is a supported source observation, a supported limit, warranted uncertainty, or an unsupported assertion. Explain:

1. Does the cited record say what the claim attributes to it?
2. Does another supplied record conflict? Is a resolution actually provided?
3. Is a missing collection interval being mistaken for no activity?
4. Can the conclusion be narrowed, or is more evidence necessary?

Fill your worksheet before opening [the authored answer key](lab/rubric.json). Reporting “the identity source says failed” preserves attribution; declaring the overall attempt definitively failed chooses a winner without evidence. Reporting disagreement and a known gap is useful output, rather than a failure to finish the task. Do not assume that other uncollected sources agree.

## Vary only the citation

Save a copy of `claims.json` somewhere under `.cache/`. In the copy, change only claim 3's references from E01/E02 to E03, then run:

```bash
uv run --frozen --offline python modules/output-validation-and-uncertainty/lab/inspect_validation.py claims --claims .cache/claims-edited.json --output .cache/validation-claims-2
```

Use your saved copy's actual path. The reference check still passes because E03 exists. The health check does not support the unchanged statement about conflicting sign-in outcomes. The authored answer key describes the original six claims; your variation needs its own manual explanation, not an automatic reused verdict. Leave source fixtures unchanged.

## Explain and check

- Give one structurally valid claim that is unsupported, naming the conflicting or missing evidence.
- Rewrite claim 4 as a supported limit. Explain why a collection gap cannot establish absence.
- Explain why changing a citation to another real ID can leave the automatic grade unchanged.
- What additional observation would justify resolving the source disagreement? Do not invent that observation.

Expected: claim 2 and claim 4 are unsupported despite resolvable IDs; claim 6 has both an unresolved reference and no support for its reset assertion. Claim 3 expresses bounded uncertainty, while claim 5 states a collection limit. This is a human fixture rubric; no model reviewer, calibrated confidence score or production investigation grade is provided.

[Worked observations](worked-observations.md) · [Session notes](README.md#completion-notes) · [Sources](SOURCES.md)
