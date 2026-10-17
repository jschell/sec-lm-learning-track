# Plan 07: Context and state

Status: implementation complete. Three offline lessons and inspection lab are authored and locally checked; independent learner validation remains open. See [the module](../../../modules/context-and-state/README.md) and [validation](../../../modules/context-and-state/VALIDATION.md).
Estimated learner effort: three 20–40-minute modules, excluding setup; project estimate.
Prerequisites: Python lists/dictionaries and Track 1 setup or a supplied equivalent. No model, Docker or API key for the first experiments.

## Learning question

What information reaches the next inference, what persists outside it, and what can be lost when history is selected or summarized?

## Worked modules

1. **Locate state.** Reuse and link the [existing state companion](../../../modules/messages-and-model-input/state.md). Supply a complete short exchange over a synthetic status file. Predict the second request, inspect the actual appended result, then omit that result in a counterfactual input. Keep the canonical protocol-valid conversation unchanged; label the counterfactual as input inspection, not a valid provider exchange. Compare in-process history, saved trace and source file after process exit. Do not claim weight/cache changes from request traces.
2. **Select evidence.** Supply a tiny fixed packet with stable event IDs, one relevant fact, a contradiction and a documented collection gap. Compare full input with a deterministic keyword-selected subset. Vary only selection; record included/excluded IDs and packet size. Character/byte counts must be named accurately; token counts require an explicitly selected tokenizer. No vector store or embedding model.
3. **Summarize and resume.** Supply authored faithful and deliberately lossy summaries of the same packet. Compare them one at a time with the full-input baseline. Check retained facts, references and unresolved gaps against fixture truth. A saved note affects input only after the controller loads it. An optional bounded live comparison may follow; authored summaries and scripted responses must never be called model-generated observations.

Input selection, compaction and persisted notes draw on [Anthropic's context-engineering explanation](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). The packet, comparisons and grading are original teaching design. Continue distinguishing weights, input, cache, harness state and files using the existing companion's original sources.

## Starting state and artifacts

Implement under `modules/context-and-state/`, with the existing state page retained as the conceptual entry point. Supply complete Python 3.12+/uv commands, original synthetic packet, authored summaries, a small inspection script and worked output. Each run starts from the supplied snapshot. Write a comparison record of included IDs/facts/gaps and the learner's explanation. No edits to the Track 1 learner's own implementation are needed.

Reuse existing trace and message structures where that keeps the code visible. Do not invent a generalized memory service. Start offline; live code is justified only by a stated observational question and must reuse an explicit existing model/provider route, not assume a running server.

## Acceptance

- [x] Markdown teaches each essential concept locally, with complete examples and small original-source callouts.
- [x] Each module has prediction, exact run/inspection instructions, one-factor variation and an explanation check.
- [x] Worked observations and explanation questions identify where the fact first enters input and what is retained in each variant; independent learner demonstration remains unperformed.
- [x] Deliberately lossy summary drops a known fact or gap; an independent fixture check exposes that loss.
- [x] Input availability is separate from model use/correctness; replay and authored summaries are labelled.
- [x] Fresh supplied starting states, bounded files and documented output paths; meaningful deterministic checks pass.
- [x] Navigation, sources and implementation validation updated; independent learner evidence remains pending until observed.

## Exclusions and continuation

No automatic summarizer, long-running agent, KV-cache instrumentation, semantic-search benchmark, client corpus, or requirement for a small model to perform forensic reasoning. Optional live observations retain failures and identify model/runtime/settings; they are not a completion gate for the input-inspection objective. After this implementation and checks, proceed to Plan 08 while independent validation remains open.

## Sources to use during authoring

[Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), checked 2026-10-17 for selection, compaction and external notes; [Huntley workshop](https://ghuntley.com/agent/), checked 2026-10-17 for inference/tool feedback; existing companion source table for state distinctions. Source-topic checks are not API compatibility or learner validation. Pin any newly adapted code and verify its license before reuse.
