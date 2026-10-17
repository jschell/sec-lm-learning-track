# Tool requests and feedback: sources

Checked 2026-10-16. Text, fixtures, wire protocol, bridge and tests are original MIT project work. No upstream code copied. Dates identify inspection, not completion of all validation.

| Concept/artifact | Original source | Use and verification |
| --- | --- | --- |
| Inference, dispatch and tool-feedback loop | Geoffrey Huntley, [coding-agent workshop](https://ghuntley.com/agent/), [source at fa3dd49](https://github.com/ghuntley/how-to-build-a-coding-agent/tree/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e) | Previously inspected for Track 1; [original source record](../../tracks/01-author-the-loop/SOURCES.md). Existing original Python loop is reused unchanged |
| Client tools and matching result IDs | Anthropic, [handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls), [define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) | Protocol distinction; user-defined names, descriptions and input schemas checked. Our two-shape JSON text projection is a teaching design, not Anthropic's wire API |
| Formatting and native completion fields | ggml-org, [server documentation](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/tools/server/README.md) | Pinned `/apply-template`, `/tokenize`, `/completion`, `json_schema`, `stop_type`; source inspected and actual CPU requests exercised |
| Schema grammar and its limits | ggml-org, [GBNF/JSON Schema guide](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/grammars/README.md) | Inspected original source; runtime constrains generated format and does not inject the JSON Schema into the prompt. Original supported-subset schema used here; no adapted grammar code |
| Native function-calling comparison | ggml-org, [function calling](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/docs/function-calling.md) | Optional comparison; this lesson does not exercise the native tool API or claim model-specific support |
| Prepared runtime/model/environment | [Generation source record](../generation-and-sampling/SOURCES.md), [setup manifest](../generation-and-sampling/lab/setup.json) | Reuses pinned llama.cpp f74e2fa, SmolLM2-135M-Instruct, bartowski Q8 artifact/hash, licenses and Python 3.12+/uv setup. No additional model download or dependency added |

Schema validity versus task correctness, nonce fixture design, read-only access and completion checks are this project's educational choices. Actual records are separately labeled from deterministic comparisons and mocked tests in [validation](VALIDATION.md).
