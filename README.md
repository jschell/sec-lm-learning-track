# Security language-model learning tracks

Learn to build and assess small LLM-assisted security workflows whose outputs are traceable to evidence, whose access is bounded, and whose results can be independently checked.

For security professionals providing consulting services. Assumes Python and ordinary security-engineering experience; neural-network training is optional.

## Start here

This repository currently contains a **curriculum design sketch**, not a completed course or runnable lab suite.

| Track | Outcome | Design |
| --- | --- | --- |
| 1. Understand and author the loop | Build and explain a small Python harness | [Track 1](tracks/01-author-the-loop/README.md) |
| 2. Build bounded security tools | Define useful operations with explicit access and failure behavior | [Track 2](tracks/02-security-tools/README.md) |
| 3. Assemble evidence and context | Select evidence while preserving provenance and engagement boundaries | [Track 3](tracks/03-evidence-and-context/README.md) |
| 4. Validate outputs | Check artifacts, coverage, claims, and uncertainty independently | [Track 4](tracks/04-validation/README.md) |
| 5. Control execution and data | Enforce isolation, destinations, permissions, and review points | [Track 5](tracks/05-execution-and-data/README.md) |
| 6. Package a repeatable workflow | Deliver something another consultant can run and inspect | [Track 6](tracks/06-repeatable-workflows/README.md) |

Track 1 is the compact 4–8-hour loop-familiarity exercise inspired by [Geoffrey Huntley's workshop](https://ghuntley.com/agent/) and [original Go source](https://github.com/ghuntley/how-to-build-a-coding-agent). The Python adaptation and consulting exercises will be this project's own material. The other tracks supplement it; they are not prerequisites for completing it.

## How to use the collection

Start with Track 1. Select later modules by the problem you need to understand. The suggested consulting route is 1 → 2 → 3 → 4 → 5 → 6; baseline containment is included in Track 1 before command execution.

Each future lesson will explain the concept locally, include a worked example and bounded exercise, and end with an observable completion check. External resources provide attribution and optional depth, not mandatory viewing assignments.

- [Design and scope](docs/design.md)
- [Module authoring template](templates/module.md)
- [Citation and source policy](docs/citation-policy.md)
- [Original source register](reference/sources.md)
- [Optional foundations and specialist branches](reference/optional-tracks.md)
- [Implementation sequence](docs/plans/README.md)

The track selection, ordering, exercises, and effort estimates are project design judgments. Cited materials support the underlying concepts, not claims that their authors endorse this curriculum.
