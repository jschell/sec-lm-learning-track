# Learner handoff: author desk check

Date: 2026-10-17. Scope: the [Track 1 worksheet](../../tracks/01-author-the-loop/pilot-worksheet.md), setup/navigation and existing replay commands. This was performed by the author; the [independent learner pilot](../plans/active/02-track1-pilot.md) remains open.

## Starting state

A new checkout of main at `4cce9b1d4eda9fc894075b86ce6986b287085128`, with a new virtual environment. Linux x86_64; uv 0.12.23 was already installed. `uv python install 3.12` retrieved CPython 3.12.15; `uv sync --frozen` created the environment and `uv run --frozen --offline python --version` reported 3.12.15. This is a fresh-checkout/environment check, not a fresh-OS installation or a physical Pi test.

No model assets, provider keys or Docker were needed for the worksheet's core commands. Temporary run directories contained copied synthetic fixtures. Source fixtures remained unchanged. Earlier exploratory checks on this checkout also used the existing system Python 3.12.14; the commands below and Track 1 suite were then repeated in the new 3.12.15 environment.

## Observed commands

Run each command from the repository root after the setup above:

| Command after `uv run --frozen --offline python` | Actual observation |
| --- | --- |
| `learn.py stage 1` | One recorded inference request, zero tools; scripted response returned |
| `learn.py stage 2` | Two requests; matching call/result IDs and actual copied notes.txt contents in the second request and history |
| `learn.py trace TRACE_PATH` | Compact viewer exited successfully for the actual Stage 2 path; it lists events without expanding request bodies/history |
| `learn.py stage 3` | Five requests, four tool events, three error results; later read succeeded and status was completed |
| `learn.py --scenario repair` | Six requests/tool events; copied fizzbuzz.py matched the supplied repaired solution. Command execution remained false: grader outcomes were scripted |
| `learn.py --scenario multi` | Two requests and two successful dispatches; completed |
| `learn.py --scenario multi --max-calls 1` | One request, no dispatches; tool_limit before the two-call batch |
| `learn.py transfer` | Actual count_lines dispatch; observed notes.txt count of two, matching feedback and completed status |
| `learn.py --scenario injection` | Two requests, one read; target fizzbuzz.py remained byte-identical to its source fixture |
| `learn.py guards` | Six expected comparison observations with recording-only proposals; no action execution |

All these CLI invocations exited 0, including the deliberate tool_limit case. The terminal status and observed effects convey information the process exit code alone does not. The trace assertions compared returned Stage 2 text with the actual copied file, and repaired output with the supplied solution; final assistant text was not used as a substitute for execution evidence.

The standard-library suite also passed in the new environment:

```bash
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
```

Current test count and wider validation are maintained in [Track 1 validation](../../tracks/01-author-the-loop/VALIDATION.md).

## Documentation findings and corrections

1. The compact viewer hides full requests and history. The worksheet and exchange lesson now direct learners to the JSONL file. Stage 2 records feedback in history/the second request without a standalone tool event; Stages 1–2 also lack the repeated loop's explicit stop event.
2. A controller stop is not synonymous with a failing process exit. The budget variation asks learners to inspect the reported status and actual dispatch count.
3. Track 1's completion table and pilot checklist treated a hosted key as necessary for model observation. They now distinguish local CPU observations from the still-unperformed hosted experiments.
4. The direct local route did not clearly say that the learner can prepare 360M without downloading 135M first. Its setup now states the explicit choice and keeps baseline comparison optional.
5. Design/plan text still described all model observations as future/unperformed. It now links observed local evidence while leaving hosted compatibility, learner understanding and physical Pi validation separate.

The existing `--model 360m` preparation/server selectors and `--prompt-style example` client selector were checked against their CLI help/source. The local model itself was not downloaded or rerun during this handoff work. Its actual recipe evidence remains in [the model comparison record](../../modules/tool-requests-and-feedback/VALIDATION.md), with the [original manifests and sources](../../modules/tool-requests-and-feedback/SOURCES.md).

During merge verification, the separate main model job failed its strict exact-copy requirement (two of three tasks passed). That failure was retrieved and retained; [decision 0002](../decisions/0002-feedback-integration-and-model-outcomes.md) records the revised integration contract and unchanged task grades. The passing replay commands above do not erase that model failure.

## Remaining validation

An independent learner must still complete the worksheet, record time/help and explain the transitions using their own evidence. Physical Pi setup/resources and hosted-provider experiments also remain unperformed here. No learner comprehension, new model reliability or injection-resistance claim follows from this desk check.

The worksheet and checks are original project work. The taught loop is based on [Geoffrey Huntley's original workshop](https://ghuntley.com/agent/); call/result ordering and IDs are described in [Anthropic's original client-tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). Those sources were rechecked on 2026-10-17; this record reports this project's execution and teaching choices, not the authors' endorsement.
