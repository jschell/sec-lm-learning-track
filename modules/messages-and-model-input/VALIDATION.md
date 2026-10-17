# Messages and model input: validation

Checked 2026-10-16. Linux, CPython 3.12.14, uv 0.12.23; tokenizers 0.22.2, Jinja2 3.1.6. See [asset provenance](SOURCES.md).

| Check | Observed result |
| --- | --- |
| Pinned original tokenizer/config/license download | Downloaded and SHA-256 verified; about 7 MB total |
| Actual local tokenizer/template tests | Six unittest checks passed locally |
| Prose, code, JSON and Unicode roundtrips | Exact with special markers retained on decode; fixed IDs/counts checked |
| Role markers and generation suffix | Actual pinned IDs and rendered suffix checked |
| Definition/call/result rendering | All present in the real template output |
| Omitted history | Call/result content absent, definition retained; counts compared |
| Missing/modified assets | Rejected before tokenizer/template loading |
| Model generation, weight changes, runtime cache | Not performed or demonstrated |
| Hosted-provider equivalence | Not claimed |
| Independent learner pilot | Not performed |

Repeat using the [lesson's preparation and offline commands](README.md). CI prepares assets online, then runs local tests in offline uv mode. The Python process does not call a model service. Exact fixture counts depend on this asset revision and renderer; changing JSON whitespace or dictionary order can change counts without changing the conceptual tool schema.

This is implementation evidence, not proof of understanding or security of arbitrary templates.
