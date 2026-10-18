# Track 1 source and adaptation record

Checked 2026-10-16. This track is an original Python teaching implementation inspired by Geoffrey Huntley's progression. No Go code, transcript passages, or external SDK implementation is copied. Original project code and documentation are licensed under [MIT](../../LICENSE); this does not grant rights to copy upstream code.

## Huntley attribution

Original author: **Geoffrey Huntley**. Article: [how to build a coding agent: free workshop](https://ghuntley.com/agent/), published 2025-08-24.

Inspected upstream commit: [fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e](https://github.com/ghuntley/how-to-build-a-coding-agent/tree/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e). This is a later source snapshot, not a claim to reproduce the August 2025 code exactly.

| Upstream path at pinned commit | Relevant concept |
| --- | --- |
| [chat.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/chat.go) | Basic chat/inference starting point |
| [read.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/read.go) | Read-file tool exchange |
| [list_files.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/list_files.go) | Directory tool stage |
| [bash_tool.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/bash_tool.go) | Command tool stage |
| [edit_tool.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/edit_tool.go) | String replacement stage |
| [code_search_tool.go](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/code_search_tool.go) | Tool registry and repeated feedback; file opened during research |

The inspected repository tree contains no license file. We therefore do not assume permission to copy its code. Any future copying requires checking applicable rights and retaining required notices; attribution alone is insufficient.

## Protocol and execution sources

| Original source | Use and verification scope |
| --- | --- |
| Anthropic, [Messages API](https://platform.claude.com/docs/en/api/messages/create) | REST endpoint/request shape; adapter uses API version header 2023-06-01; no SDK dependency |
| Anthropic, [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) | name, description, input_schema |
| Anthropic, [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | tool_use IDs, tool_result, ordering, is_error |
| Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflow versus model-directed control |
| Docker, [Run reference](https://docs.docker.com/engine/containers/run/) and [Engine security](https://docs.docker.com/engine/security/) | Container options, security components; actual test scope in validation record |
| Simon Willison, [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Private data, untrusted content, external communication |

OpenRouter’s original [Messages endpoint reference](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message), [authentication guide](https://openrouter.ai/docs/api_reference/authentication), and [tool-calling guide](https://openrouter.ai/docs/guides/features/tool-calling) support the optional OpenRouter transport. Checked 2026-10-16: endpoint, bearer authentication, Anthropic-format requests/results, and documented tool support. The same Python loop is retained; no third-party routing library is introduced. Provider requests are tested with synthetic HTTP responses, not paid live inference.

The live adapter supports text and ordinary client tools only. It stops on unsupported content/stop reasons rather than claiming general provider compatibility. Tested Python and mocked transport details are in [VALIDATION.md](VALIDATION.md). A mutable documentation page is not evidence that every future model supports these settings.

## Python environment

Python 3.12+ and uv are project preferences. Setup and frozen/offline execution follow [Astral’s project guide](https://docs.astral.sh/uv/guides/projects/); CI uses the official [uv GitHub Actions integration](https://docs.astral.sh/uv/guides/integration/github/). Checked 2026-10-16. The Docker command executor uses its own image Python; uv manages the host controller and tests.

## Original project artifacts

All lab fixtures, assistant responses, expected command observations, bug, reference repair, grader, learner starters, tests, and trace format are authored for this project. The JSON replay provenance field labels responses as synthetic rather than captured model output. Fixture hashes are in [fixture-manifest.json](lab/fixture-manifest.json).

Changes from the workshop: Python instead of Go; REST instead of SDK; network-disabled Docker instead of host command execution; /bin/sh instead of bash; bounded literal search instead of ripgrep; unique-match edit policy; explicit limits and traces; independently supplied grader. These are teaching and containment choices, not features attributed to Huntley.

## Usability and observation additions

The one-page loop is an original explanatory sketch of Huntley’s inference/tool-feedback pattern using Anthropic client-tool message names. The short launcher, read-only allowlist, omitted-tool experiment, prediction worksheet, and pilot checklist are original project additions. Read-only enforcement removes operations from both the exposed definitions and dispatch; tests distinguish this controller property from unperformed model/learner observation.

## Worked stages and behavioral checks

Complete runnable stages follow [Huntley's original progression](https://github.com/ghuntley/how-to-build-a-coding-agent/tree/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e). Our original check contracts are informed by [Stanford CS336 adapters](https://github.com/stanford-cs336/assignment1-basics/blob/main/tests/adapters.py) and [Karpathy's micrograd behavioral tests](https://github.com/karpathy/micrograd/blob/master/test/test_engine.py), inspected 2026-10-16. No upstream code/tests are copied. These sources do not validate this curriculum's usability. See [decision 0001](../../docs/decisions/0001-worked-stages-first.md) for the project's choices and limits. The count_lines tool and replay are original transfer exercises.

## Corrective review additions

The task-specific policies, terminal-guard checks, redacted HTTP diagnostics and injection data-flow fixture are original project additions. Anthropic’s [client-tool guidance](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls), rechecked 2026-10-16, describes stop reasons, result placement and untrusted tool content. [Simon Willison’s original threat explanation](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) supports the injection discussion. The fixture contains no private data or exfiltration endpoint, and its replay does not demonstrate model resistance. OpenRouter’s [Messages endpoint documentation](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message) was rechecked; live compatibility remains unobserved.

The [missing-guard comparison](08-learn-from-missing-guards.md) makes the omissions in the pinned Huntley dispatch loop observable through original recording-only Python tools. The separate core and guard checkpoints are project pedagogy, not an upstream grading requirement. No dangerous execution is required to observe the difference.

## Learning-path and trace usability

The six core outcomes, single worksheet route, evidence/progress table and cumulative trace summaries are original project choices. They retain Huntley's progression and the existing client-tool protocol citations above. Python's official [copytree reference](https://docs.python.org/3.12/library/shutil.html#shutil.copytree) documents copying a directory and refusing an existing destination by default; [argparse documentation](https://docs.python.org/3.12/library/argparse.html) supports the trace/guard command help. Opened 2026-10-17 (America/Los_Angeles), tested with CPython 3.12.15. No Python documentation code was copied. Platform support and learner timing remain limited to actual recorded observations.
