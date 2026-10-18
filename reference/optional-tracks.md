# Optional foundations and specialist branches

Status: further branch proposals. Short conceptual model foundations and [messages/token formatting](../modules/messages-and-model-input/README.md) are promoted companions in the [capability map](../README.md); implementing BPE, training, and transformer internals remain optional.

| Branch | Learning goal and bounded exercise | Original sources |
| --- | --- | --- |
| Extended conceptual viewing | Explain generation, training/inference, and base/assistant distinctions; draw the boundary around the harness | Karpathy's [catalog](https://karpathy.ai/) and [Deep Dive](https://www.youtube.com/watch?v=7xTGNNLPyMI) |
| Tokenizer implementation depth | Inspect token counts, special tokens, and rendered chat messages; BPE implementation is optional | Karpathy's [Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE), [minbpe](https://github.com/karpathy/minbpe); runtime template documentation |
| Native function-calling comparison | Optional follow-up: compare a native endpoint/template/parser with the implemented [custom text bridge](../modules/tool-requests-and-feedback/README.md); local CPU setup and inference already exist | [llama.cpp function calling](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md) and [server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) |
| MCP | Implemented in [Tool interfaces and protocols](../modules/tool-interfaces-and-protocols/README.md); compare one function through direct and local stdio calls; remote transports/authentication remain optional | [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28) |
| Neural-network foundations | Build a tiny generator or gradient engine; separate generation from agent orchestration | Karpathy's [makemore](https://github.com/karpathy/makemore), [micrograd](https://github.com/karpathy/micrograd), [syllabus](https://karpathy.ai/zero-to-hero.html) |
| Transformer internals | Implement a small GPT-style network; separate project from consulting essentials | Karpathy's [Zero to Hero](https://karpathy.ai/zero-to-hero.html), [build-nanogpt](https://github.com/karpathy/build-nanogpt) |
| Model-as-tool | Observe a nested review call and its added cost/failure surface | [Amp Oracle](https://ampcode.com/news/oracle) |

Selection is a project recommendation. Avoid broad model leaderboards, multi-agent systems, and mandatory framework surveys in the core. No branch is an implicit extension of the 4–8-hour harness exercise.
