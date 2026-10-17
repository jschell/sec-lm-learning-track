# Language-model mechanics for security professionals

Understand what happens between a prompt, model generation, a requested tool call, execution, and the next inference. Build small observable exercises before adding security applications.

The audience is security professionals familiar with Python. Security examples ground the material; operational consulting delivery is a later application rather than a prerequisite.

## Start with the working loop

[Track 1: Understand and author the loop](tracks/01-author-the-loop/README.md) is the Huntley-inspired, independently usable starting point. Read [the loop on one page](tracks/01-author-the-loop/core-loop.md), then run, inspect and vary the request, tool exchange, and feedback loop. Reconstruction is optional.

After Python/uv setup in Track 1:

```bash
uv run --frozen --offline python learn.py stage 1
```

## Capability map

Use the [run/inspect/explain worksheet](tracks/01-author-the-loop/pilot-worksheet.md) for a guided Track 1 session and to record learner-pilot evidence. It includes both the local CPU and hosted-model routes.

| Capability | Material | Status |
| --- | --- | --- |
| Author and inspect the agent loop | [Track 1](tracks/01-author-the-loop/README.md) | Implemented; [validation](tracks/01-author-the-loop/VALIDATION.md) separates replay, Docker, and unperformed live checks |
| Observe actual tool selection and errors | [Read-only live experiments](tracks/01-author-the-loop/live-observation.md) | Implemented; provider behavior not yet observed live |
| Understand tokens and formatted messages | [Messages and model input](modules/messages-and-model-input/README.md) | Implemented local inspection; [validation](modules/messages-and-model-input/VALIDATION.md) |
| Understand generation and sampling | [Generation and sampling](modules/generation-and-sampling/README.md) | Runnable lab; [validation](modules/generation-and-sampling/VALIDATION.md) tracks model suitability and Pi portability |
| Connect local generation to tool feedback | [Tool requests and feedback](modules/tool-requests-and-feedback/README.md) | Observed 360M/example working configuration, with baseline failures retained; [validation](modules/tool-requests-and-feedback/VALIDATION.md) |
| Bound domain tools and evidence retrieval | [Security tools](tracks/02-security-tools/README.md), [evidence/context](tracks/03-evidence-and-context/README.md) | Application outlines, deferred |
| Validate findings and control engagement access | [Validation](tracks/04-validation/README.md), [execution/data](tracks/05-execution-and-data/README.md) | Application outlines, deferred; baseline checks already accompany runnable labs |
| Package a consulting workflow | [Repeatable workflows](tracks/06-repeatable-workflows/README.md) | Application outline, deferred |
| Explore local serving, MCP, or training internals | [Further branches](reference/optional-tracks.md) | Optional proposals |

This is a capability map, not a requirement to complete every row. Keep the existing Track 1 paths stable. Short conceptual companions about generation, messages, and state are part of understanding the system; building tokenizers or training networks from scratch is optional.

## Original sources and project choices

[Geoffrey Huntley's workshop](https://ghuntley.com/agent/) supplies the loop starting point. [Andrej Karpathy's educational material](https://karpathy.ai/) supplies model/tokenization foundations. [Anthropic's workflow/agent distinction](https://www.anthropic.com/engineering/building-effective-agents) helps locate programmed control versus model-selected action. The scope, exercises, sequencing, and effort estimates are this project's judgments, not endorsements by those authors.

[Design](docs/design.md) · [Plans](docs/plans/README.md) · [Module template](templates/module.md) · [Citation policy](docs/citation-policy.md) · [Original sources](reference/sources.md) · [Python/uv guidance](docs/python-development.md)

## License

Original project code and documentation are licensed under [MIT](LICENSE). Third-party assets and dependencies retain their own licenses; see the [tokenizer asset source record](modules/messages-and-model-input/SOURCES.md).
