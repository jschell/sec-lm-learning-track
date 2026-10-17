# Plan 10: Untrusted input and execution authority

Status: queued; implement after Plan 09. Track 1 contains a synthetic injection scenario; the new comparison below is not implemented.
Estimated learner effort: two 30–45-minute modules; project estimate.
Prerequisites: locate tool results in input and distinguish proposal from execution. Supply a complete controller and fixtures; no earlier learner code required.

## Learning question

How can retrieved content influence a proposed action, and where is execution authority enforced independently?

## Worked modules

1. **Follow the untrusted text.** Reuse the Track 1 injection fixture or an original minimal derivative. Trace file contents into an actual tool result and next request. Compare benign and injected copies, changing only the embedded instruction. Use authored responses to demonstrate a proposed unauthorized operation, explicitly labelled scripted. Optional live observation may show refusal, action, malformed output or no useful response; never require or claim that every model follows an injection.
2. **Locate authority.** Replay the same proposal against a recording-only dispatcher and a bounded read-only dispatcher that independently denies the forbidden operation. Record requested arguments, decision and actual execution count. Seed an approval-by-description mistake only in the recording-only example; compare it with explicit operation/argument validation. A prompt telling the model to be careful is not evidence that the dispatcher enforced a permission.

[Simon Willison's lethal-trifecta analysis](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) supplies the untrusted-content/data/action risk framing. Do not claim this read-only offline fixture reproduces every element of exfiltration risk. Baseline Track 1 containment remains intact; the lesson builds on the owner's decision to teach missing controls through bounded subsequent exercises.

## Starting state and artifacts

Implement under `modules/untrusted-input-and-authority/`. Supply original synthetic file contents, fixed proposals, complete dispatch comparison, exact commands and expected event table. Label toy secrets as synthetic. No real exfiltration endpoint, destructive tool or new shell execution is needed.

Artifact: a short data-flow/authority map and event table separating content exposure, proposed action, policy decision and actual effect. Reuse existing trace conventions; do not build an approval service or generalized security middleware.

## Acceptance

- [ ] Each unit contains prediction, complete run, one-factor variation, deliberate bounded failure and explanation.
- [ ] Untrusted bytes are visible in returned data and subsequent input; no claim of private reasoning visibility.
- [ ] A scripted forbidden proposal executes zero forbidden operations under the bounded dispatcher.
- [ ] Trace distinguishes refusal/no attempt, denied attempt and actual effect; recording a proposal is never labelled execution.
- [ ] The independent enforcing code and residual limits are identifiable by the learner.
- [ ] Optional live behavior is separate from deterministic checks; an observed refusal does not establish general safety.
- [ ] Sources, fixture provenance, original controls and explicit unperformed learner validation retained.

## Boundaries

No real credentials, client data, outbound network, deletion, writable source fixtures or host-shell fallback. Do not disable the execution-enabled reference's controls. Cross-client isolation, remote approvals, container-escape testing and full engagement retention policies remain deferred in [Track 5](../../../tracks/05-execution-and-data/README.md).

## Sources

[Willison: The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), checked 2026-10-17 for the risk model; [Huntley's loop workshop](https://ghuntley.com/agent/), checked 2026-10-17 for the loop starting point; [Track 1 control lesson](../../../tracks/01-author-the-loop/README.md) for this project's existing guarded/recording-only comparisons. Fixture, boundaries and acceptance are project design.
