# 0003: Base understanding of the loop before any focus area

Date: 2026-10-20. Status: adopted at the owner's direction ("we want base understanding established before moving to any focus area, including security"). Extends [decision 0001](0001-worked-stages-first.md); does not replace it. Implementation is planned in [Plan 17](../plans/active/17-track1-part0-the-loop.md).

## Problem

Track 1 opens with a security framing: its entry page asks whether an agent's "I disabled the account" claim was proposed, dispatched or verified, before the learner has seen a loop. Its first activity, worksheet section 1, already uses trace, dispatch and history vocabulary. The other modules (context and state, tool protocols, output validation, untrusted input and authority) and the Track 1 extensions (Docker containment, injected content, missing guards) are focus areas: each assumes the learner already understands the loop.

An author-side comparison with [Geoffrey Huntley's workshop](https://ghuntley.com/agent/), checked against the [pinned repository](https://github.com/ghuntley/how-to-build-a-coding-agent/tree/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e) on 2026-10-20 (UTC), confirmed that his progression establishes the loop first: a chat stage whose conversation grows across user turns (`chat.go`), then a tool definition with name, description, input schema and function, and an inner loop that repeats until the model stops requesting tools, with tool errors returned as ordinary results flagged as errors (`read.go`). The later stages reuse the identical inner loop and add tools; none adds stop-reason or limit checks. Each stage is supplied as a complete runnable program.

## Decision

1. **Base understanding comes first.** Before any focus area, a learner should be able to show that:
   - a conversation is history that the application re-sends with each request;
   - a tool definition, a model's proposed call and the controller's dispatch are three different things;
   - a result returns to the model as a message matched to its call by ID, including error results;
   - the loop repeats until the model stops proposing calls;
   - the loop itself is small.

   The check for this is predicting request N+1 from request N.
2. **Track 1 Part 0 teaches it**, following Huntley's order with original Python code and scripted replay: conversation, tool definition, one exchange, the loop (including an error result), then the same loop with more read-only tools. No upstream code is copied; the pinned repository has no licence file.
3. **Focus areas come after it.** Security review, containment, untrusted input, guards and the other modules are focus areas. Each states Track 1 base understanding as a prerequisite. The account-disable example stays, as the first application of the loop rather than the entry framing.
4. **Answers to the open questions:**
   - Writing the loop stays optional, as in decision 0001; reading and predicting it are core. This matches Huntley's supplied complete programs.
   - Part 0's core runs on scripted replay; observing the same loop with a real model is an optional step.
   - Part 0 is additive. Worksheet section 1 stays frozen (Plan 15), and the six outcomes are grouped and relabelled, not renumbered.

## Consequences

- Part 0's minimal loop is intentionally guard-free, like Huntley's. It is safe only because Part 0 refuses live mode, exposes only read-only tools and runs on finite replay. The worked stages then add checks (duplicate IDs, stop reason, limits), and the guarded reference adds the rest. Lesson 8's recording-only comparison fixture stays separate.
- The pilot route begins with Part 0, after the baseline form. That is an instruction revision; assessment items are unchanged.
- Author and AI reviews remain preparation, not learner evidence. Revisit this decision after the Plan 02 walkthrough, in particular whether Part 0 makes parts of sections 1–2 redundant.

## Sources

The progression is Huntley's (pinned stages in the [Track 1 source record](../../tracks/01-author-the-loop/SOURCES.md)). Call/result pairing and error results follow [Anthropic's client-tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls). The base-understanding outcomes, the focus-area classification and the ordering rule are this project's decisions.
