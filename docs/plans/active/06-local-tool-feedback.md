# Plan 06: Connect local generation to tool feedback

Status: lesson implemented; baseline suitability and learner validation open.

## Scope

Bridge the existing original Track 1 loop to the prepared local runtime through an explicit, inspectable teaching text protocol. Keep native provider tool formats distinct. Use one synthetic read-only task, fresh file contents, a scripted feedback comparison and actual model observations. Show formatting, valid dispatch, feedback and answer accuracy separately.

The [lesson](../../../modules/tool-requests-and-feedback/README.md) and [source record](../../../modules/tool-requests-and-feedback/SOURCES.md) connect [Huntley's loop](https://ghuntley.com/agent/) with pinned [llama.cpp generation/grammar behavior](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/grammars/README.md). The wire protocol and scope are project decisions.

## Acceptance and remaining work

- [x] Complete independently runnable starting code, with no learner edits required.
- [x] Existing loop reused; fresh IDs and actual tool feedback visible.
- [x] Scripted comparison reads current synthetic contents and answers from feedback.
- [x] Actual baseline runs preserve ordinary, constrained, omitted-tool and output-cap outcomes.
- [x] Task correctness is separate from schema validity and loop completion.
- [x] Replay/contracts and real-model checks remain distinct.
- [ ] Learner can explain each boundary using their own trace (pilot required).
- [ ] Validate a small model/prompt configuration completing the actual read-and-answer task. Preserve the 135M failures; any 360M comparison must be explicit, pinned and independently measured.
- [ ] Physical Pi 4 setup/resources/task behavior verified, shared with Plan 04.

No new framework, general provider abstraction, shell, production agent, benchmark platform or automatic model fallback. Do not mark model suitability complete because output parses. Current results and reproducible commands: [validation](../../../modules/tool-requests-and-feedback/VALIDATION.md).
