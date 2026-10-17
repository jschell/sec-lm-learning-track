# Plan 03: Messages and model input

Status: active preparation; state companion authored, tokenizer/template work pending. See [scope](../../../modules/messages-and-model-input/README.md).

Select and pin one tokenizer/template with checked license, then author encode/decode and conversation-rendering exercises. Explain roles, special tokens, tools, counts, and omitted history. No training or retrieval service. Provide a short conceptual state map: weights, current context, runtime cache, external storage, and harness state.

Acceptance: complete local explanation, reproducible uv commands, fixtures, observable completion checks, original sources, and explicit limits on claims about hosted-model formatting. Use pilot feedback where available.

Sources: [Karpathy tokenizer lecture](https://www.youtube.com/watch?v=zduSFxRajkE), [minbpe](https://github.com/karpathy/minbpe), and the eventual selected model/runtime's original documentation. Implementation choices remain pending.

## Progress and remaining work

- Authored the [state companion](../../../modules/messages-and-model-input/state.md), using the existing complete tool-exchange example. No new dependency or runtime behavior is claimed.
- Pending: select a tokenizer/template, verify its immutable revision and license, implement encode/decode/rendering fixtures and checks, record tested commands/resource needs.
- Keep the module in preparation until those acceptance criteria pass. Live model observation and learner-pilot evidence remain separate.
