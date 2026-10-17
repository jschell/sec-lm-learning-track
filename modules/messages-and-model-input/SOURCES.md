# Messages and model input: original sources and assets

Checked 2026-10-16. Explanations, fixtures, preparation code, renderer adapter and tests are original project work. No tokenizer is trained and no upstream Python implementation is copied.

| Concept or artifact | Original source | Use and verification |
| --- | --- | --- |
| Tokens and byte-level BPE | Andrej Karpathy, [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE), [minbpe](https://github.com/karpathy/minbpe) | Conceptual background; optional depth, no copied code or unverified chapter timestamps |
| Chat formatting and generation prompt | Hugging Face, [Chat templates](https://huggingface.co/docs/transformers/chat_templating) | Documentation inspected; our narrow Jinja adapter is not its apply_chat_template implementation |
| Actual tokenizer/template/config | Qwen, [Qwen2.5-0.5B-Instruct at pinned revision](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/7ae557604adf67be50417f59c2c2f167def9a775) | Downloaded tokenizer.json and tokenizer_config.json unmodified; tested with tokenizers 0.22.2 and Jinja2 3.1.6 |
| License | Qwen, [LICENSE at the same revision](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/LICENSE) | Apache License 2.0 inspected; retained unmodified alongside downloaded assets. Does not select a license for this course |
| Tokenizer load/encode/decode | Hugging Face, [tokenizers Python bindings](https://github.com/huggingface/tokenizers/tree/v0.22.2/bindings/python) | Installed pinned package; real local tests, no inference |
| Jinja execution | Pallets, [Sandbox](https://jinja.palletsprojects.com/en/stable/sandbox/) | Pinned template only; no general untrusted-template service |
| uv optional groups | Astral, [Managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) | Optional tokens group; frozen lockfile, offline commands after setup |

## Exact asset provenance

Repository: Qwen/Qwen2.5-0.5B-Instruct. Revision: 7ae557604adf67be50417f59c2c2f167def9a775. The [manifest](lab/assets.json) records the URL components and SHA-256 for each original file. No model weights are fetched. The cache is excluded from git; preparation retrieves original bytes directly from the publisher. LICENSE stays beside those files. No separate NOTICE file was listed in the inspected model repository tree.

The template string is read from the original tokenizer_config.json at runtime and is not copied into this project's Python source. The renderer supplies only the variables and JSON filter needed by this pinned text/tool exercise. Fixture calls and results are authored inputs, not captured model choices or actual file reads. No model quality or hosted-provider prompt format is established.

[Lesson](README.md) · [State companion sources](state.md#sources-and-adaptations)
