# 3. Summarize and resume

Goal: inspect what a replacement summary preserves, and show that a saved note must be loaded into new input.

Compaction replaces older context with a selected representation, often a summary. External notes are stored separately and later retrieved into context. [Anthropic's original discussion](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) describes these strategies and the risk of losing details. Here both summaries are **authored fixtures**. We isolate retention without requiring a small model to summarize or reason about incidents.

## Predict, then run

Read the packet from the previous lesson or [open it directly](lab/fixtures/packet.json). Predict which IDs a useful summary must retain to preserve the disagreement and coverage limit. Then:

```bash
uv run --frozen --offline python modules/context-and-state/lab/inspect_context.py resume --output .cache/context-resume-1
```

Compare `full-input.json` with `faithful-input.json`, then with `lossy-input.json`. Only the supplied evidence representation changes. The faithful summary retains the two source outcomes, their disagreement, and the gap. The lossy summary drops E02/C01 and asserts “No successful activity occurred.” That assertion is unsupported: E02 reports success and the collection is incomplete. This is a seeded authoring defect, not an observed model hallucination.

`report.json` flags missing IDs and literal anchors. It cannot validate that the summary is faithful. For example, a string saying `E01 was NOT failed. E02 was NOT success. C01 has NO collection gap at 10:02–10:05.` passes these literal checks while reversing the evidence. This counterexample is covered by a test to document the checker's limit. Read the actual statements and compare them to the packet.

## Load the saved note

The same command writes `faithful-note.txt`, then constructs `resume-without-loading.json` and `resume-after-loading.json`:

```python
note = (output / 'faithful-note.txt').read_text(encoding='utf-8')
request = input_request(packet['task'], note)
```

Open both inputs. The first contains only the task; the second includes the explicitly read note. Saving a note alone does not insert it into input. This program demonstrates the transition in one process and saves both variants; the files also remain readable after it exits. No inference or automatic memory retrieval occurs.

## Explain and check

1. Which required records are absent from the lossy version, and which assertion overstates the evidence?
2. Why can an ID/anchor check expose omission without proving entailment?
3. Locate the code that changes external note bytes into supplied input. Is the saved note a model-weight update?
4. Propose a shorter summary that keeps both conflicting outcomes and the gap. Compare it manually with the packet; rebuilding a summarizer is unnecessary.

Expected: E02 and C01 are missing. A supported statement reports disagreement and limits; it does not choose a winning source or assert absence of activity. Note loading changes request content, not weights. These checks assess your explanation of this fixture, not operational investigation competence.

[Session notes and transfer](README.md#session-notes-and-transfer-check) · [Sources](SOURCES.md)
