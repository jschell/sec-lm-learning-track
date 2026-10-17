# Contributor instructions

## Purpose and scope

Maintain a Markdown-first, modular learning collection for security consultants. Preserve loop familiarity as a compact, independently usable starting track. Do not expand it into a production-agent certification or neural-network curriculum.

## Original sources are mandatory

- Follow [the citation policy](docs/citation-policy.md) for every lesson, exercise, design note, and substantive change.
- Cite original authors, research, official documentation, and upstream code beside the supported concept. A source list alone is insufficient.
- Distinguish sourced behavior from this project's recommendations and original exercises.
- Open and verify sources before claiming support. Do not invent timestamps, versions, benchmark results, licenses, or quotes.
- When adapting code, record upstream path and immutable commit, retain required notices, and check the actual license. A citation does not grant permission to copy.
- Record unverified sources as candidates; never present them as verified evidence.

## Authoring

Use [the module template](templates/module.md). Every module must identify prerequisites, status, a bounded exercise, observable checks, and source attribution. Keep drafts clearly marked. Do not imply proposed labs exist or have passed.

Explain essential material locally in original wording. Use external links for attribution and optional depth. Modules need their own starting state; do not depend on a previous learner's unfinished code. Avoid large hidden helper layers and duplicated source excerpts.

## Lab boundaries

Synthetic fixtures by default. No client identifiers, secrets, live customer endpoints, or copied engagement data. Read-only domain operations first. Define containment before executing generated code. Keep hosted-model credentials outside the tool executor. Never describe a container as proof against all escape paths.

For the SIEM examples, routine raw telemetry remains in the SIEM; local stores hold derived behavioral information. Raw incident artifacts require explicit investigation scope and handling rules.

## Change process

Use a branch and reviewable PR. Preserve unrelated content. Validate relative Markdown links and source coverage. Run meaningful code checks once runnable labs exist; do not add empty CI or tests that merely mirror the document text.

Use docs/plans/active, complete, and queue for implementation plans. Move plans only when their acceptance criteria are met. Do not select a license on the owner's behalf.
