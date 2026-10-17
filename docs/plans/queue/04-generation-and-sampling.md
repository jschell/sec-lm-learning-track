# Plan 04: Generation and sampling

Status: queued after the messages module. See [scope](../../../modules/generation-and-sampling/README.md).

Select one small pretrained model/runtime exposing next-token scores. Build bounded probability/sampling/termination observations. Explain training versus inference without requiring training implementation.

Acceptance: pinned model/tokenizer/runtime and checked rights/resource needs, complete Markdown explanation, uv commands, fixed synthetic prompts, score inspection, one-factor variation, and explicit distinction between token generation and harness control. No benchmark suite or leaderboard.

Sources: [Karpathy Deep Dive](https://www.youtube.com/watch?v=7xTGNNLPyMI), [makemore](https://github.com/karpathy/makemore), and eventual runtime/model documentation. Exercise design is original project work.
