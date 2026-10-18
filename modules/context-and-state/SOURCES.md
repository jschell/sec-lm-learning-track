# Original sources and fixture provenance

Sources opened 2026-10-17. Existence/topic checks do not establish learner effectiveness or reproduce upstream experiments. Explanations, synthetic fixtures and inspection script are original project work under the repository's MIT license; no upstream code, transcripts or customer data are copied.

| Original source | Concept used | Verification and limits |
| --- | --- | --- |
| Geoffrey Huntley, [how to build a coding agent: free workshop](https://ghuntley.com/agent/), 2025-08-24 | Inference/tool-feedback progression | Article opened; the project's [Track 1 source record](../../tracks/01-author-the-loop/SOURCES.md) pins upstream code; no Go adaptation |
| Anthropic, [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Matching client tool call/result messages | Documentation opened; state lab reuses the existing original Python worked exchange, not a hosted provider |
| Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29 | Selection, compaction, external notes and information loss | Article opened; fixture comparisons do not measure a model's summarization quality |
| Hugging Face, [Transformers v5.7.0 cache explanation](https://huggingface.co/docs/transformers/v5.7.0/en/cache_explanation) | Cache distinguished from editable transcript/files | Documentation opened; inherited [state map](../messages-and-model-input/state.md) explains it; no runtime/cache inspection here |

## Project artifacts

- `lab/fixtures/packet.json`: four invented records with stable IDs, conflicting source outcomes and a collection gap. No dataset ingestion or anonymization claim.
- `lab/fixtures/summaries.json`: two authored representations, including a seeded omission and unsupported assertion. Neither is model-generated.
- `lab/fixtures/rubric.json`: an independent hand-authored list of required literal markers; does not establish semantic support or general summary quality.
- `lab/inspect_context.py`: original inspection code, importing the repository's existing `exchange`, `Tools`, `Workspace` and `Trace`. Fixed assistant responses; actual read-only file access. The incomplete exchange copy is explicitly inspection-only.
- `worked-observations.md`: measured source/evidence sizes and transition observations from the local author run. Fixtures are versioned with the lesson in git; source revisions are changed deliberately, not fetched at runtime.

Concept citations appear beside explanations in each lesson. No automatic summary generation, tokenizer, model/runtime or external service is used by these scripts.
