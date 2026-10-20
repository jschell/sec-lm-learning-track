# Messages, tokens, and model input

Status: implemented local inspection lab, offline after dependency/asset preparation; [validation](VALIDATION.md) records tested behavior and remaining usability checks.
Estimated effort: 45–75 minutes, a project estimate, plus first download.
Prerequisites: Track 1 base understanding of the loop ([Part 0](../../tracks/01-author-the-loop/00-the-loop.md) at minimum; [decision 0003](../../docs/decisions/0003-base-understanding-first.md)); Python dictionaries/lists, Python 3.12+ and uv. No completed learner code from Track 1 is needed.

> **Recall before you start:** Which messages did request 3 of Part 0's loop step contain, in order?

<details><summary>Check your recall</summary>

The user task, the model's first call, its error result, the model's second reply with its call, and that call's result. This module shows how such a message list becomes model input.

</details>

## Goal and explanation

Explain how text and structured messages become a model-specific token sequence. Locate role markers, tool definitions, requested calls and returned observations in an actual local rendering.

Start with [where state lives](state.md) if context, weights and harness memory are unclear. A tokenizer maps text into vocabulary IDs; a token can represent part of a word, punctuation, whitespace or bytes. Our Unicode fixture shows why decoding one token at a time can be misleading. [Karpathy's tokenizer lecture](https://www.youtube.com/watch?v=zduSFxRajkE) explains these concepts in depth; building a tokenizer is optional.

Message dictionaries need formatting as well as tokenization. A chat template inserts a model's expected role/boundary markers and can serialize tool information. [Hugging Face's chat-template guide](https://huggingface.co/docs/transformers/chat_templating) explains this conversion and why templates differ across models. The locally published template is inspectable; a hosted API's private formatting is not established by this exercise.

## Prepare once online

From the repository root:

```bash
uv python install 3.12
uv sync --frozen --group tokens
uv run --frozen --group tokens python modules/messages-and-model-input/lab/prepare.py
```

Initial preparation needs PyPI and huggingface.co network access. The optional tokens group pins tokenizers 0.22.2 and Jinja2 3.1.6 through uv.lock. Track 1 still needs neither. Follow [uv installation](https://docs.astral.sh/uv/getting-started/installation/) if needed.

The preparation script downloads about 7 MB of tokenizer/config/license data into .cache/model-input, checks SHA-256, and retains the upstream license. It downloads no model weights and requires no account, API key, GPU or inference server. The model repository revision is 7ae557604adf67be50417f59c2c2f167def9a775; [source and licensing details](SOURCES.md).

The inspection and test commands below are offline **after** those steps. A clean checkout has no tokenizer assets; `--offline` does not download them.

## Worked example: inspect text and roles

```bash
uv run --frozen --offline --group tokens python modules/messages-and-model-input/lab/inspect_input.py --variant plain
```

The JSON output includes each original fixture, token count, IDs, vocabulary pieces, character offsets and decoded text, followed by the rendered conversation and its encoding. These are computed local results, not synthetic model responses.

| Original project fixture | Expected tokens with this pinned tokenizer |
| --- | --- |
| Investigate unusual sign-ins. | 6 |
| Two-line Python function | 11 |
| Synthetic JSON sign-in event | 16 |
| café followed by a lock emoji | 4 |

The prose IDs are `[33876, 63956, 18511, 1841, 21853, 13]`. The plain conversation is 28 tokens and starts with `<|im_start|>system`, includes a user message, and ends with `<|im_start|>assistant` followed by a newline. It is a prepared input awaiting generation; this script generates no answer.

For this tokenizer, `<|im_start|>` is one special token, ID 151644, and `<|im_end|>` is ID 151645. The word `system` in a rendered role header is separate text; do not assume every visible header element is itself a special token. Vocabulary pieces may show byte-level symbols rather than normal typography. Inspect decoded text as well as pieces.

The implementation uses `add_special_tokens=False` when encoding the already formatted conversation, and `skip_special_tokens=False` when decoding. This avoids asking for extra wrapper tokens and keeps markers visible, following the [chat-template guidance](https://huggingface.co/docs/transformers/chat_templating). Hiding markers during decode does not remove their IDs from the original input.

## Observe tools and omit history

Predict which information each variation should retain, then run:

```bash
uv run --frozen --offline --group tokens python modules/messages-and-model-input/lab/inspect_input.py --variant tool
uv run --frozen --offline --group tokens python modules/messages-and-model-input/lab/inspect_input.py --variant omitted
uv run --frozen --offline --group tokens python modules/messages-and-model-input/lab/inspect_input.py --variant plain --no-generation-prompt
```

Tool includes the definition, assistant call and observation. Omitted drops the whole call/result pair while retaining the definition and initial task. Plain drops both the exchange and definitions. Removing the generation prompt drops the final assistant-start suffix. Compare actual counts; do not add independently encoded fragment counts and assume they equal the combined tokenization.

Locate `<tools>`, `<tool_call>` and `<tool_response>` in the tool rendering. The [original Qwen template](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/tokenizer_config.json) groups tool responses into user-role blocks. These XML-like tags are formatting text; inspect IDs before assuming they are special tokens. We use the template's function-message shape, which differs from Track 1's Anthropic API blocks. No implicit cross-provider conversion occurs.

The count of two lines is an authored fixture here: **no count_lines tool runs**. Track 1's [transfer exercise](../../tracks/01-author-the-loop/06-transfer-tool.md) demonstrates actual execution. Supplying a tool description creates input; executing a tool requires a host dispatcher.

## Make one small change

```bash
uv run --frozen --offline --group tokens python modules/messages-and-model-input/lab/inspect_input.py --text 'Investigate unusual sign-ins!'
```

Predict how punctuation might affect the IDs, then compare with the original prose. For a larger variation, edit a copy of the synthetic text in fixtures.json and rerun. Restore the supplied fixture before using the regression checks. The tokenizer assets stay hash-checked; modifying them is a separate experiment.

## Completion check

Show one exact text roundtrip, a token boundary inside a word or Unicode representation, a role marker's ID, a tool definition, and the returned observation in the rendered input. Explain what disappears in omitted and what remains. Name what these observations cannot establish: generated behavior, task success, cache reuse or hosted-provider formatting.

Implementation regression checks:

```bash
uv run --frozen --offline --group tokens python -m unittest discover -s modules/messages-and-model-input/lab/tests -v
```

Passing implementation tests does not establish learner understanding. Reconstruction of the small [inspection functions](lab/inspect_input.py) is optional.

## Troubleshooting and boundaries

Missing packages: run uv sync with --group tokens, then retain that option on commands. Missing/altered assets: rerun prepare.py online; it replaces only assets that fail the fixed checks. A changed hash is a preparation failure, not a reason to silently update the manifest. Offline failures on first setup mean preparation is incomplete.

We evaluate the original downloaded Jinja template with a small, explicitly scoped renderer. It is not Transformers.apply_chat_template, and it does not promise compatibility with arbitrary templates, multimodal content or every tokenizer-config feature. [Jinja's sandbox documentation](https://jinja.palletsprojects.com/en/stable/sandbox/) describes its execution restrictions; this lab accepts only its pinned template and bounded supplied fixtures, not arbitrary untrusted templates. No Python remote code is loaded.

Synthetic local inputs only. Custom text is printed to stdout; keep secrets and customer data out. No inference, training, tool execution or hosted-model observation occurs.

> **Optional resource — Andrej Karpathy, Let's build the GPT Tokenizer**
> Explains byte-level tokenization and BPE. Useful depth after inspecting this lab; no transcript or implementation is copied.
> [Original video](https://www.youtube.com/watch?v=zduSFxRajkE) · [Original minbpe repository](https://github.com/karpathy/minbpe)

[Sources and adaptations](SOURCES.md) · [Validation](VALIDATION.md) · [Collection](../../README.md) · [Completed implementation plan](../../docs/plans/complete/03-messages-and-model-input.md)
