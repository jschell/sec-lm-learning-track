# Where does the state live?

Status: draft companion; uses the verified offline Track 1 example. This lesson does not run a model or inspect a runtime cache.
Estimated effort: 20–30 minutes, a project estimate.
Prerequisites: Python lists/dictionaries; [Track 1 setup](../../tracks/01-author-the-loop/README.md). Reconstruction exercises are optional.

## Goal

Locate the state needed for a tool exchange, and explain what clearing the conversation actually removes.

## Five places to look

The following map is this project's teaching organization. It separates the application loop in [Huntley's workshop](https://ghuntley.com/agent/) from model computation and persistent application data.

| State | What it contains | What changes during an ordinary run? | Visible in our replay? |
| --- | --- | --- | --- |
| Model weights | Learned numerical parameters | Ordinary inference uses the parameters; training or explicit adaptation changes them | No weights are loaded |
| Current model input | Instructions, messages and available tool definitions, subsequently formatted/tokenized by the provider or runtime | The controller builds a new request with selected history and results | Yes: request events show the API objects, not the final model tokens |
| Runtime KV cache | Attention keys and values computed from processed tokens | A supporting runtime reuses these computations during generation | No runtime exists in replay |
| Harness state | Message list, call counter, iteration limit, tool registry and workspace configuration | The controller appends results and updates counters | Requests and tool/stop events expose parts; inspect code for the rest |
| External storage | Files, databases, saved notes and traces | Tool execution or application code may read/write them | File reads and trace writes are real |

For model training versus inference, see [Karpathy's Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI). A prompt supplying a fact ordinarily changes the input, not the learned weights. This lesson does not demonstrate weight updates or online adaptation.

A KV cache stores intermediate attention computations so a runtime can reuse work on previous tokens. It is runtime-managed numerical state, not an editable conversation transcript or a database of facts. Its persistence and reuse depend on the serving implementation. The [Hugging Face caching explanation](https://huggingface.co/docs/transformers/v5.7.0/en/cache_explanation) describes this mechanism; we do not install Transformers or claim that this is the hosted provider's implementation.

## Worked exchange

From the repository root after setup:

```bash
uv run --frozen --offline python learn.py stage 2
```

The complete example prints the conversation and a trace path. Inspect the trace with:

```bash
uv run --frozen --offline python learn.py trace /tmp/loop-stage-REPLACE/trace.jsonl
```

Replace the path with the printed path. No API key, model download or Docker is required. File operations use a fresh temporary synthetic workspace. The model responses are scripted.

Find the first request: it contains the task and definitions, but no returned file contents. Find the assistant's read_file call. The host dispatches that call and appends a matching tool_result containing the read text. Find that result in the second request. The file's existence did not itself put its bytes into the first request.

The call/result message ordering follows [Anthropic's client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). The particular assistant choice is our synthetic fixture. A trace demonstrates the controller's supplied input; it does not expose private model reasoning.

## Predict and vary

Open [the short exchange function](../../tracks/01-author-the-loop/lab/solutions/stages.py). Locate the list initially holding the user message, the append of assistant content, the actual dispatch, and the append of returned results. Predict what the second request would contain if the controller instead supplied only the original user message. You can inspect that counterfactual list without making an inference call.

Then run the stage again. It creates another workspace and trace. Explain why those persistent trace files can remain on disk even though the Python process ended. Explain why starting another process does not automatically load an earlier trace as conversation history.

[Anthropic's context-engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) discusses selecting instructions, tools, history and external data for the available input. A saved note becomes relevant to inference when the application retrieves and supplies it. Stateful services can perform that retrieval for you; this stateless lab does not. Summarizing or omitting history changes the supplied evidence and can lose details.

## Completion check

Write five short answers:

1. Which request first contains the file's returned text?
2. What code moves it from external storage into the message list?
3. What remains on disk after the process exits, and what must be loaded explicitly?
4. Why does dropping prior messages neither erase model weights nor delete the source file?
5. What evidence would be needed to claim the real runtime reused a KV cache?

Expected observations: the second request contains the tool result; Tools.dispatch reads through Workspace and exchange appends the result; workspace/trace files remain until removed, while the in-process list is not automatically restored. Request traces alone cannot establish KV-cache reuse. These checks assess an explanation of this example, not general model competence.

## Troubleshooting and boundaries

A missing temporary path usually means the placeholder was not replaced or that an earlier workspace was removed. Run the stage again. The supplied trace inspector may present only recognized events; open trace.jsonl directly to inspect all request events. No tool in this exercise changes source fixtures.

This companion does not yet show token IDs or a model's chat template. API message roles are not themselves evidence of the exact special tokens seen by a hosted model. The [tokenizer portion of this module](README.md) inspects one published tokenizer/template locally; it does not establish hosted-format equivalence. No real customer data belongs in fixtures or traces.

## Sources and adaptations

| Original source | Use and verification scope |
| --- | --- |
| [Geoffrey Huntley: coding-agent workshop](https://ghuntley.com/agent/) | Application loop; pinned source record in [Track 1](../../tracks/01-author-the-loop/SOURCES.md); no copied code |
| [Andrej Karpathy: Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI) | Training/inference conceptual background; optional depth, not a prerequisite video |
| [Hugging Face: Caching, Transformers v5.7.0 docs](https://huggingface.co/docs/transformers/v5.7.0/en/cache_explanation) | KV-cache concept; documentation checked 2026-10-16; runtime not installed/tested |
| [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Message feedback protocol; implementation verification in Track 1 |
| [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Input curation, published 2025-09-29; checked 2026-10-16 |

The state map, questions and walkthrough are original project work. [Back to module](README.md).
