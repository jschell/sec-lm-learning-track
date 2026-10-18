# Output validation and uncertainty

Status: two runnable offline worked lessons; independent learner walkthrough pending.
Estimated effort: two 30–45-minute sessions; project estimate.
Prerequisites: inspect a tool trace and small JSON objects. Complete starting files are supplied. No model download, server, API key, MCP group or Docker required.

A response can be valid JSON, complete a tool exchange and still fail its task. A claim can cite a real event ID and still misrepresent the event. Learn which check answers which question:

| Lesson | Worked example | One deliberate variation |
| --- | --- | --- |
| [1. Separate outcomes](01-separate-outcomes.md) | Recheck three retained actual model traces, including the wrong exact answer | Change one feedback ID in a labelled copy of a successful case |
| [2. Check claims](02-check-claims.md) | Review six authored claims against conflicting evidence and a collection gap | Substitute a real but irrelevant reference |

[Anthropic's original evaluation article](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) distinguishes tasks, trials and graders. Here one task has several recorded trials and separate checks. Re-inspecting a saved trace does not create another trial. These small cases teach evaluation mechanics; they are not a model ranking. Exercise design and the fixture rubric are original project work.

## Setup and run

Install [uv](../../docs/python-development.md), then from the repository root:

```bash
uv python install 3.12
uv sync --frozen
uv run --frozen --offline python modules/output-validation-and-uncertainty/lab/inspect_validation.py outcomes --output .cache/validation-outcomes-1
uv run --frozen --offline python modules/output-validation-and-uncertainty/lab/inspect_validation.py claims --output .cache/validation-claims-1
```

Only initial environment setup may need network access. These commands inspect committed local files with standard-library code. They do not run model preparation or inference. Use a new output directory for each run; existing directories are refused.

The first command verifies and references [the retained model record](../tool-requests-and-feedback/observations/main-2026-10-17.json), preserving raw outputs and source provenance. It reuses the existing parser and feedback check. The second uses [the supplied synthetic packet](../context-and-state/lab/fixtures/packet.json), independent of any earlier learner run. It writes structural checks and a blank human-review worksheet, not semantic verdicts.

An observed wrong answer or unsupported claim is expected learning material; a successful inspection exits 0. Missing/changed source or invalid setup exits 2. Read the individual checks instead of treating the shell exit code as a task grade.

## Completion notes

Make a prediction before each lesson, then record:

- Which artifact and exact event/claim support your judgment?
- Which check passed, which failed, and what does each leave unknown?
- What changed in the synthetic variation, and what remained untouched?
- For one unsupported claim: what narrower statement is supported, or what evidence is missing?

The claims command writes `claim-review.md` in its output directory. Complete it before comparing [the authored rubric](lab/rubric.json). A checklist or answer key is not evidence of independent learner understanding.

[Worked observations](worked-observations.md) · [Sources](SOURCES.md) · [Validation](VALIDATION.md) · [Collection](../../README.md)
