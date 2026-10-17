# Plan 03: Messages and model input

Status: implementation complete; independent learner pilot remains unperformed. See [scope](../../../modules/messages-and-model-input/README.md).

Select and pin one tokenizer/template with checked license, then author encode/decode and conversation-rendering exercises. Explain roles, special tokens, tools, counts, and omitted history. No training or retrieval service. Provide a short conceptual state map: weights, current context, runtime cache, external storage, and harness state.

Acceptance: complete local explanation, reproducible uv commands, fixtures, observable completion checks, original sources, and explicit limits on claims about hosted-model formatting. Use pilot feedback where available.

Sources: [Karpathy tokenizer lecture](https://www.youtube.com/watch?v=zduSFxRajkE), [minbpe](https://github.com/karpathy/minbpe), and the selected [Qwen tokenizer/template source record](../../../modules/messages-and-model-input/SOURCES.md).

## Delivered and verification

- Local state companion and self-contained tokenizer/template lesson.
- Pinned Qwen2.5 tokenizer/config/license at revision 7ae557604adf67be50417f59c2c2f167def9a775, downloaded without weights and hash-checked.
- Optional tokenizers/Jinja dependency group with frozen uv commands; Track 1 stays dependency-free.
- Original prose, code, JSON, Unicode and tool-exchange fixtures; observable counts/IDs/rendering and omission variations.
- Six actual local behavioral checks passed. Sources, tested scope and limits are recorded in [module validation](../../../modules/messages-and-model-input/VALIDATION.md).
- CI tests Python 3.12/3.13; do not infer a passing run merely from workflow presence. No inference, hosted-format equivalence or learner-pilot result is claimed.

This satisfies implementation acceptance. Pilot feedback can still revise the lesson. Generation and sampling remains the next separate module.
