# Build bounded security tools

Status: design sketch; lessons and labs are not implemented.

## Goal

Expose useful security operations with explicit inputs, access, result semantics, and failure behavior.

## Prerequisites

Track 1 or equivalent understanding of tool exchanges.

## Proposed lessons

| Lesson | Coverage |
| --- | --- |
| 1. Tool contracts | Names, descriptions, typed schemas, validation, and unambiguous operation boundaries. |
| 2. Bounded event queries | Explicit time range, engagement scope, pagination, completeness, and read-only credentials. |
| 3. Enrichment and disagreement | Return source/version and conflicting observations without silently choosing a winner. |
| 4. Results and errors | Stable IDs, concise/detailed views, partial results, rate limits, and expired credentials. |

## Proposed exercise

Build read-only query_events and enrich_indicator over synthetic fixtures. Compare two interfaces for the same task; vary only descriptions or result format. Proposed names and fixture design are original project choices.

## Completion check

A caller can identify access scope, result completeness, provenance, and recoverable versus terminal errors; five small tasks expose wrong-tool and wrong-argument behavior.

## Scope

Teach the necessary concepts locally. External viewing is optional. Use independent starting states, synthetic fixtures, and small visible implementations. No live client access or production deployment is required.

## Original sources and project additions

[Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) supports interface and result-design concepts. Engagement-specific restrictions are project requirements, not claims about the source.

Apply the [citation policy](../../docs/citation-policy.md) in each future lesson; this track outline is not a substitute for local attribution. See the [source register](../../reference/sources.md) for verification scope.

[Back to collection](../../README.md)

