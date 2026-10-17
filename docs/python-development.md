# Python and uv contributor guidance

This repository targets **Python 3.12+**. The default interpreter is pinned to 3.12 in `.python-version`; `pyproject.toml` and the committed lockfile require at least 3.12. This minimum is the project owner's preference, not a claim about MCP SDK requirements.

## Original reference

Use the official [modelcontextprotocol/python-sdk AGENTS.md](https://github.com/modelcontextprotocol/python-sdk/blob/9f66f376d486e84e9810b368cf8be9d5908661ab/AGENTS.md) as a development-guidance reference, alongside its [pyproject.toml](https://github.com/modelcontextprotocol/python-sdk/blob/9f66f376d486e84e9810b368cf8be9d5908661ab/pyproject.toml). Both were inspected 2026-10-16. This document paraphrases relevant practices; it does not copy the upstream guide or import its repository-specific obligations.

| Adopt here | Application |
| --- | --- |
| uv package management | Use uv add / uv add --dev and deliberate lockfile updates; no pip or uv pip install |
| Frozen execution | Use uv run --frozen; prepared offline lessons also use --offline |
| Visible dependencies | Prefer module-scope imports; explain genuine optional-loading exceptions |
| Maintainable interfaces | Annotate new/changed interfaces and explain caller-relevant behavior |
| Explicit text encoding | UTF-8 for new/changed text I/O |
| Specific error handling | Broad catches only at deliberate top-level failure boundaries |
| Deterministic tests and matching docs | Separate replay/mocks from real execution; update lessons with changes |

The upstream SDK's release branches, issue-assignment requirements, 100% coverage policy, conformance-suite rules, dynamic-dependency layout, and pytest/anyio tooling are specific to that project. They are not requirements of this learning collection. The stdlib lab remains dependency-free and uses unittest. This reference does not introduce an MCP dependency or change the live model adapter into an MCP client.

## Working commands

Install uv using the [official instructions](https://docs.astral.sh/uv/getting-started/installation/). Prepare once from the repository root:

```bash
uv python install 3.12
uv sync --frozen
```

Then run the lab/checks without downloads:

```bash
uv run --frozen --offline python tracks/01-author-the-loop/lab/cli.py --scenario read
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
```

Use `uv add <dependency>` only when a lesson needs it, `uv add --dev <tool>` for development tooling, and `uv lock --upgrade-package <name>` for deliberate upgrades. After intentionally editing the minimum Python version or dependency metadata, regenerate `uv.lock` with `uv lock`, then review both files. Frozen runs must not rewrite it implicitly.

CI follows [Astral's original GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/) with the official setup-uv action, uv 0.12.23, and Python 3.12/3.13. Host commands use uv; the minimal Docker executor uses its image's Python directly. CI setup and initial image/interpreter downloads require network access; offline replay does not after setup.
