# Contributor instructions

## Purpose and scope

Maintain a Markdown-first, modular learning collection about language-model operations and functional mechanics for security professionals. Use consulting examples where useful; keep full delivery workflows as later applications. Preserve loop familiarity as a compact, independently usable starting track. Do not expand it into a production-agent certification or neural-network curriculum.

## Original sources are mandatory

- Follow [the citation policy](docs/citation-policy.md) for every lesson, exercise, design note, and substantive change.
- Cite original authors, research, official documentation, and upstream code beside the supported concept. A source list alone is insufficient.
- Distinguish sourced behavior from this project's recommendations and original exercises.
- Open and verify sources before claiming support. Do not invent timestamps, versions, benchmark results, licenses, or quotes.
- When adapting code, record upstream path and immutable commit, retain required notices, and check the actual license. A citation does not grant permission to copy.
- Record unverified sources as candidates; never present them as verified evidence.

## Authoring

Target Python 3.12+. Prefer uv for interpreter/environment management and documented host commands. Keep `.python-version`, `requires-python`, lockfile, and CI aligned. Offline lab commands use `uv run --frozen --offline python`; commands inside the minimal Docker executor use its own Python directly.

Use [the module template](templates/module.md). Keep the README capability map and queued plans aligned with the mechanics-first sequence. Current test/verification claims belong in the Track 1 validation record; link there rather than duplicating historical counts. Do not claim a learner pilot or live model run occurred unless evidence exists. Every module must identify prerequisites, status, a bounded exercise, observable checks, and source attribution. Keep drafts clearly marked. Do not imply proposed labs exist or have passed.

Explain essential material locally in original wording. Use external links for attribution and optional depth. Modules need their own starting state; do not depend on a previous learner's unfinished code. Avoid large hidden helper layers and duplicated source excerpts.

## Teaching decision and memory

Follow [decision 0001](docs/decisions/0001-worked-stages-first.md): complete runnable stages first, followed by prediction, inspection, modification and explanation. Reconstruction is optional. Keep behavioral checks small and explicit: observe inference, actual dispatch, matching feedback and finite stops, and retain regressions for plausible wrong implementations. Do not turn this collection into a grader platform or imply passing checks proves understanding. Preserve the short read-only transfer exercise before expanding machinery. Original Huntley, CS336 and micrograd sources and limitations are recorded in the decision. Maintain accepted constraints in [project memory](docs/memory.md).

Track 1 progression: core feedback mechanics come first. Teach missing stop-reason and call-budget handling as an explicit learning objective in the later control section, using recording-only proposals before comparing guards. Keep the optional guard check separate from core completion; do not block the initial exercise for these intentional omissions. The execution-enabled reference retains its controls.

## Python development guide

The relevant conventions below are informed by the original [MCP Python SDK AGENTS.md](https://github.com/modelcontextprotocol/python-sdk/blob/9f66f376d486e84e9810b368cf8be9d5908661ab/AGENTS.md), checked 2026-10-16. They are adapted to this small learning repository; upstream release, contribution, and conformance policies do not apply here.

- Use uv for package/environment management; do not use pip or uv pip install. Add dependencies with `uv add`, development tools with `uv add --dev`, and make deliberate upgrades with `uv lock --upgrade-package <name>`. Keep the lockfile committed.
- Run commands through `uv run --frozen`; use `--offline` for prepared replay labs. Avoid implicit latest-version tool installs. Initial interpreter/environment setup may need network access.
- Keep imports visible at module scope unless optional loading genuinely requires otherwise. Add meaningful type annotations to new/changed interfaces and document observable behavior and caller-relevant exceptions. Keep teaching comments focused on learning transitions and non-obvious constraints.
- Specify UTF-8 for new/changed text I/O. Catch specific exceptions; reserve broad catches for a documented top-level failure boundary such as the lab run controller.
- Keep tests deterministic, bounded, and focused on behavior. Separate mocked/replayed checks from actual execution. Update relevant lessons when behavior changes. Existing standard-library unittest checks remain the project test framework; this guide does not require adding pytest, anyio, Ruff, Pyright, or a coverage target.

See [Python/uv contributor guidance](docs/python-development.md) for scope and original references.

## Lab boundaries

Synthetic fixtures by default. No client identifiers, secrets, live customer endpoints, or copied engagement data. Read-only domain operations first. Define containment before executing generated code. Keep hosted-model credentials outside the tool executor. Never describe a container as proof against all escape paths.

For the SIEM examples, routine raw telemetry remains in the SIEM; local stores hold derived behavioral information. Raw incident artifacts require explicit investigation scope and handling rules.

## Change process

Use a branch and reviewable PR. Preserve unrelated content. Validate relative Markdown links and source coverage. Run meaningful code checks once runnable labs exist; do not add empty CI or tests that merely mirror the document text.

Use docs/plans/active, complete, and queue for implementation plans. Move plans only when their acceptance criteria are met. The owner selected MIT for original project code and documentation. Retain third-party licenses and notices; do not imply that MIT relicenses downloaded assets.
