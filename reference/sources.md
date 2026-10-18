# Original source register

Checked 2026-10-16. Sources were opened during design research to confirm identity and topic; code was not executed, benchmarks were not reproduced, and these entries do not certify runtime compatibility. Pin source commits and record tested versions when authoring labs.

| ID | Original source | Use / relevant scope |
| --- | --- | --- |
| S01 | Geoffrey Huntley, [how to build a coding agent: free workshop](https://ghuntley.com/agent/), 2025-08-24; [original code](https://github.com/ghuntley/how-to-build-a-coding-agent) | Track 1: inference/tool-feedback loop and teaching primitives |
| S02 | Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Tracks 1/6: predefined workflows versus model-directed control |
| S03 | SWE-agent project, [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | Optional Track 1 comparison: a bash-centered minimal harness; do not transfer benchmark claims to our labs |
| S04 | Anthropic, [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Track 2: schemas, descriptions, result design, and tool evaluation |
| S05 | Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Track 3: selecting and maintaining inference context |
| S06 | Sentence Transformers, [Semantic Search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) | Optional Track 3 retrieval implementation |
| S07 | Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Track 4: tasks, trials, graders, outcomes |
| S08 | Simon Willison, [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Track 5: private data, untrusted content, external communication |
| S09 | Docker, [Docker Engine security](https://docs.docker.com/engine/security/) | Tracks 1/5: execution-boundary components and configuration |
| S10 | Pydantic AI, [Agents](https://ai.pydantic.dev/agents/) and [Advanced Tool Features](https://ai.pydantic.dev/tools-advanced/) | Track 6: compare loop control, validation, and approval integration; recheck version-specific behavior |
| S11 | Andrej Karpathy, [educational catalog](https://karpathy.ai/) and [Zero to Hero syllabus](https://karpathy.ai/zero-to-hero.html) | Optional foundations; original author and lecture scope |
| S12 | Andrej Karpathy, [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) | Conceptual model background; author catalog confirms topic; full transcript not verified |
| S13 | Andrej Karpathy, [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE); [minbpe](https://github.com/karpathy/minbpe) | Optional tokenization implementation |
| S14 | Andrej Karpathy, [makemore](https://github.com/karpathy/makemore), [micrograd](https://github.com/karpathy/micrograd), [Zero to Hero notebooks](https://github.com/karpathy/nn-zero-to-hero) | Optional generation and training foundations |
| S15 | Andrej Karpathy, [build-nanogpt](https://github.com/karpathy/build-nanogpt) | Optional transformer implementation/training branch |
| S16 | ggml-org, [llama.cpp function calling](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md), [server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) | Local inference, templates, tool formats |
| S17 | Model Context Protocol, [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server) | Optional reusable-tool interface |
| S18 | Amp, [Oracle](https://ampcode.com/news/oracle) | Optional model-as-tool pattern |

Consulting-specific acceptance criteria, engagement-isolation exercises, synthetic fixture design, storage policy, and track priorities are project requirements/design judgments. They are not attributed to the above authors.

Follow the [citation policy](../docs/citation-policy.md); link original sources locally, not only by register ID.


Track 1 now has a [pinned upstream and protocol record](../tracks/01-author-the-loop/SOURCES.md), original synthetic fixtures, and a [validation record](../tracks/01-author-the-loop/VALIDATION.md). No upstream Go code is copied.

Contributor guidance additionally references the original [MCP Python SDK AGENTS.md](https://github.com/modelcontextprotocol/python-sdk/blob/9f66f376d486e84e9810b368cf8be9d5908661ab/AGENTS.md) and [pyproject.toml](https://github.com/modelcontextprotocol/python-sdk/blob/9f66f376d486e84e9810b368cf8be9d5908661ab/pyproject.toml), inspected 2026-10-16. [Local adaptation and scope](../docs/python-development.md).

OpenRouter live transport: original [Anthropic-format Messages endpoint](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-a-message), [authentication](https://openrouter.ai/docs/api_reference/authentication), and [tool calling](https://openrouter.ai/docs/guides/features/tool-calling), checked 2026-10-16. Documentation and mocked compatibility checks are distinguished from unperformed live inference in Track 1 validation.

The implemented [messages and model-input module](../modules/messages-and-model-input/README.md) records its original Qwen tokenizer/template revision, file hashes, license and tested runtime in its [local source record](../modules/messages-and-model-input/SOURCES.md).

The [generation and sampling module](../modules/generation-and-sampling/README.md) records its selected SmolLM2 model, Q8 converter/hash, pinned llama.cpp source, runtime API and original educational sources in its [local source record](../modules/generation-and-sampling/SOURCES.md).

The [tool requests and feedback module](../modules/tool-requests-and-feedback/README.md) connects the existing loop to native completion through an original teaching wire protocol. Its [source record](../modules/tool-requests-and-feedback/SOURCES.md) distinguishes client tool semantics, pinned llama.cpp schema constraints, and the optional native function-calling API.

Mechanics expansion, checked 2026-10-17: S01, S04, S05, S07, S08 and the S11 Zero to Hero syllabus were reopened for source identity/topic. They support the conceptual foundations of Plans 07–10, not the new exercises' effectiveness. The [MCP specification, revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) was opened as the versioned protocol reference for Plan 08; SDK compatibility and implemented protocol coverage remain to be verified during authoring. New fixture designs, authoring order, session estimates and completion rubrics are project choices. See [the plan sequence](../docs/plans/README.md); no additional track is represented as implemented by this planning update.

The implemented [Context and state module](../modules/context-and-state/README.md) has a [source/fixture record](../modules/context-and-state/SOURCES.md), checked 2026-10-17, and separate [implementation validation](../modules/context-and-state/VALIDATION.md). Its source/file observations, authored summaries and literal checks are not model-behavior evidence.

The implemented [Tool interfaces and protocols module](../modules/tool-interfaces-and-protocols/README.md) records [MCP SDK 2.3.0 and immutable source/license references](../modules/tool-interfaces-and-protocols/SOURCES.md), checked 2026-10-17. Its [validation](../modules/tool-interfaces-and-protocols/VALIDATION.md) separates actual local stdio integration from authored proposals, unperformed model inference and independent learner validation. The observed protocol revision is 2026-07-28, separate from SDK package version.

The implemented [Output validation and uncertainty module](../modules/output-validation-and-uncertainty/README.md) has a [source/provenance record](../modules/output-validation-and-uncertainty/SOURCES.md), checked 2026-10-17, covering the original evaluation article, hash-pinned retained observations and authored fixture rubric. Its [validation](../modules/output-validation-and-uncertainty/VALIDATION.md) distinguishes re-inspection, synthetic mutation, structural references and pending independent learner judgments.

The implemented [Untrusted input and authority module](../modules/untrusted-input-and-authority/README.md) has a [source/fixture record](../modules/untrusted-input-and-authority/SOURCES.md), checked 2026-10-17, citing Willison, Huntley and the client-tool protocol beside the taught concepts. Its [validation](../modules/untrusted-input-and-authority/VALIDATION.md) separates actual bounded file/decision effects from authored proposals and unperformed model/learner observations.

Pedagogy preparation sources, opened 2026-10-17: NRC [Knowing What Students Know, assessment foundations](https://www.nationalacademies.org/read/10019/chapter/3), CMU [performance-based prior knowledge assessment](https://www.cmu.edu/teaching/assessment/priorknowledge/performancebased.html), IES [Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1), and NRC [How People Learn, learning and transfer](https://www.nationalacademies.org/read/9853/chapter/6). [The pilot package](../docs/pilot/README.md), implemented by [Plan 11](../docs/plans/complete/11-pilot-preparation-and-quality-review.md), adapts these foundations to a small adult-professional pilot; it does not claim that the custom instrument or curriculum is validated. Task wording, scoring anchors and timing are project choices.
