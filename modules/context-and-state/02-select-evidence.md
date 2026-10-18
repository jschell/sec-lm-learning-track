# 2. Select evidence

Goal: distinguish available source data from the subset actually supplied in input.

Context selection chooses which information is supplied for inference. Retrieval is one way to make that choice; see [Anthropic's context-engineering discussion](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Our literal substring selector is intentionally simple. It teaches selection loss, not semantic search or model performance.

## Worked packet

The [original synthetic packet](lab/fixtures/packet.json) asks what is known about attempt A-17 for alice. E01 reports failure in one source; E02 reports success in another. C01 records a later collection gap. E03 is unrelated. Neither success nor failure is established as the single authoritative outcome; the disagreement is unresolved. All timestamps and identities are fictional.

Predict: will searching only for `alice` retain the collection gap?

```bash
uv run --frozen --offline python modules/context-and-state/lab/inspect_context.py select --output .cache/context-select-1
```

Inspect `full-input.json`, `selected-input.json` and `report.json` in that directory. These are constructed candidate inputs; no model receives them. Task, system instruction and empty tool list are identical; only evidence selection changes. The complete selection operation is:

```python
[row for row in records if query.casefold() in row['text'].casefold()]
```

It returns the matching source records in source order, without paraphrasing or inventing matches. E01 and E02 survive. C01 and E03 do not. The report separately lists missing required IDs, so the irrelevant record's exclusion is not treated as equivalent to losing the coverage limit.

## Vary one factor

Change only the query, retaining the same packet and task:

```bash
uv run --frozen --offline python modules/context-and-state/lab/inspect_context.py select --query 'collection gap' --output .cache/context-select-gap
```

C01 survives, while E01/E02 do not. There is no universally sufficient query demonstrated here. A zero-hit query produces an empty evidence string, not invented evidence; try `--query no-such-word` with another new directory if useful.

## Explain and check

- Locate the exact missing ID in the first selected input. What claim about later activity would be unjustified?
- Does a source record remaining on disk mean it was supplied in `selected-input.json`?
- Explain why both keyword variants omit relevant information, despite returning valid results.
- Compare `text_characters` and `text_utf8_bytes`. Why are neither token counts nor measurements of the complete request?

Expected: C01 is absent from the alice selection; no claim of complete later coverage is warranted. The second query preserves only C01. A shorter packet may omit needed evidence. Counts cover the rendered evidence only; the en dash in the gap range occupies more than one UTF-8 byte. Tokenization is a separate [inspectable mechanism](../messages-and-model-input/README.md).

The literal checker checks IDs/anchors, not their attribution or meaning. A human must inspect the actual source disagreement. Complete output examples are in [worked observations](worked-observations.md).

[Next: resume](03-summarize-and-resume.md) · [Sources](SOURCES.md)
