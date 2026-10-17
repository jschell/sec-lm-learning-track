# Messages, tokens, and model input

Status: **in preparation**. The [state companion](state.md) is authored and uses the existing offline loop example. Tokenizer/template exercises remain proposed; no tokenizer dependency or tokenizer lab is delivered yet.

## Question and goal

What is between the Python message objects in Track 1 and the input received by a model? Identify token boundaries, role markers, and the representation of a tool exchange.

Start with [where state lives](state.md): weights, current input, runtime cache, harness state, and external storage. It is independently usable after Track 1 setup and does not require authoring the loop.

## Bounded implementation

Choose one inspectable pretrained tokenizer/chat template with a pinned revision and checked license. Use one short text, one code snippet, and one synthetic log entry. Inspect encode/decode, counts, special tokens, and a rendered conversation. Add one tool definition/result and observe how the template represents it. Unsupported template features must be reported rather than silently invented.

No training, BPE implementation, embeddings server, or model leaderboard is required. Local rendering is an example for the chosen model, not proof of a hosted provider's private prompt formatting.

## Exercise and checks to author

Predict token splits; encode/decode the fixtures; render a user/assistant exchange; add a tool schema/result; omit history and compare the resulting input. Supply complete commands, expected representations, and an independent starting state. Distinguish inspecting changed input from observing a model's answer: only the latter requires inference.

Finish when the learner can locate roles, content, special markers, and tool information, explain why tokens differ from words, and name the limit of what the local template proves.

## Original sources

[Karpathy: Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE), [minbpe](https://github.com/karpathy/minbpe), and [Zero to Hero syllabus](https://karpathy.ai/zero-to-hero.html). Runtime-specific rendering documentation and model licensing will be verified when the implementation is selected. This scope is project design.

[Collection](../../README.md) · [Active plan](../../docs/plans/active/03-messages-and-model-input.md)
