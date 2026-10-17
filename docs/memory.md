# Project memory

Accepted constraints and decisions; update when the owner changes direction.

- Corrective-review teaching choice (2026-10-16): use missing stop-reason and call-budget handling as a subsequent Control and inspect learning objective, rather than blocking initial loop authoring. Demonstrate the failure with recording-only tools, then add/check guards separately. Keep task instructions accurate, failures observable, and execution-enabled controls intact. Live smoke validation remains open without configured credentials; the owner selected MIT for original project code and documentation.

- Purpose: familiarize security professionals with language-model operations and functional mechanics. Track 1 is a compact loop-learning artifact; consulting delivery and production harness engineering are later applications.
- Format: self-contained, modular Markdown explanations, with small callouts to original sources and runnable local examples.
- Runtime: Python 3.12+, uv, frozen lockfile. Offline synthetic replay first; live observations require a configured provider and must be reported separately.
- Teaching decision: complete runnable stages first; predict, inspect, modify and explain; reconstruction optional; narrow behavioral checks and a small read-only transfer task. Rationale, original sources and revisit conditions: [decision 0001](decisions/0001-worked-stages-first.md).
- Keep source attribution beside supported concepts. No unsupported copying or invented validation. Contributor conventions and their MCP Python SDK source are in [AGENTS.md](../AGENTS.md).
- Current verified behavior and outstanding live/pilot work: [Track 1 validation](../tracks/01-author-the-loop/VALIDATION.md). This memory does not mark either as performed.

- Plan 03 implementation is complete: the state companion and pinned local tokenizer/template lab are authored. Optional tokens dependencies preserve Track 1’s dependency-free setup. Local inspection does not demonstrate inference, tool execution, hosted formatting or learner-pilot success; see module validation.

- License: MIT for original project code and documentation, selected by the owner on 2026-10-16. Downloaded Qwen assets retain Apache-2.0; dependencies and external sources retain their own terms.

- Generation module: SmolLM2-135M-Instruct is the selected educational baseline. Validate usefulness for the actual instruction and bounded task; do not require frontier-model coverage. Try 360M only if a required objective is not demonstrated. Start from a blank slate: provide runtime installation/build, model retrieval, license/hash verification and server startup. Do not assume an existing llama.cpp instance. Pi 4 operation/resource measurements and fresh-learner usability remain explicit validation items until observed.
