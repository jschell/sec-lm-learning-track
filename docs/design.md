# Pragmatic learning design

Updated 2026-10-16. Scope: language-model operations and functional mechanics, taught through small observable exercises for security professionals.

## Learning unit

One question, one worked example, one runnable experiment, one deliberate variation, and one observable completion check. Teach essential concepts in Markdown; cite originals beside the explanation. External video is optional depth.

Preserve [Huntley's loop track](../tracks/01-author-the-loop/README.md) as a 2–4-hour familiarity path with optional reconstruction and execution extensions. Add short companions rather than a new mandatory six-track sequence. The estimate is a project planning judgment. Use [the core-loop page](../tracks/01-author-the-loop/core-loop.md) before the full reference machinery.

## Implementation order

1. Correct navigation and current validation; provide the short entry point and read-only live observation path.
2. Pilot Track 1 with a fresh learner; fix observed instruction blockers. [Checklist](../tracks/01-author-the-loop/pilot-checklist.md). This remains unperformed.
3. Build [messages, tokens, and formatted input](../modules/messages-and-model-input/README.md) with one tokenizer/template.
4. Build [generation and sampling](../modules/generation-and-sampling/README.md) with one small pretrained model.
5. Select individual security application exercises when they answer a concrete operational question. Do not implement old Tracks 2–6 together as a curriculum expansion.

The pilot should inform instructional choices, but planning or reversible implementation need not stop while no learner is available. Do not manufacture independent learner validation.

## What each exercise exposes

Distinguish model weights, request context, runtime caches, persistent external files, and harness counters/pending work. A completed inference turn is not an independently checked task result. A model's token-generation loop is different from the harness's inference/tool-execution loop.

Separate deterministic inspection/replay from actual model observation. Replay validates controller mechanics; live experiments vary one factor and record behavior. Ask the learner to predict before running. Evaluation is a method throughout, not an obligatory benchmarking project.

Security examples are selected for explanatory value. Keep baseline execution boundaries, but defer broad engagement controls, report handoff, model leaderboards, framework surveys, and multi-agent work. No live customer access is required.

## Technical boundaries

Python 3.12+, uv, and committed lockfile. Track 1 is standard-library Python, Anthropic-format REST for Anthropic/OpenRouter, explicit provider credentials, fixed endpoints, synthetic replay, and Docker-only command execution. Read-only live observation needs no Docker. No host-shell fallback.

Use one small pretrained model for future generation inspection; no training is required. Select the exact model/tokenizer, revision, license, resource needs, and runtime during the relevant module implementation. Do not hide mechanisms behind a general routing or orchestration framework.

## Authoritative locations

- Track setup/navigation: Track 1 README.
- Live-provider setup and observation worksheet: live-observation.md.
- Current verification and limitations: VALIDATION.md.
- Source provenance/history: SOURCES.md and the source register.
- Implementation sequence: plans index.

Link to those pages rather than repeating historical test counts or setup instructions across lessons.

## Original foundations

[Huntley workshop](https://ghuntley.com/agent/), [Karpathy catalog](https://karpathy.ai/) and [Zero to Hero](https://karpathy.ai/zero-to-hero.html), and [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents). Exercise design, sequencing, and completion criteria are original project decisions.
