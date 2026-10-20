# Track 1: Understand the agent loop

An agent is a small loop around a language model: the program sends a request, the model may propose a tool call, the program decides whether to run it, and the result goes back in the next request, until the model stops asking. As [Geoffrey Huntley's workshop](https://ghuntley.com/agent/) shows, the loop itself is only a few dozen lines. Track 1 makes that loop familiar first, because everything else in this collection, security review included, builds on it ([decision 0003](../../docs/decisions/0003-base-understanding-first.md)).

Our Python implementation, fixtures and exercises are original project work following Huntley's progression; [source details](SOURCES.md).

## By the end you can

Part 0 establishes the base. The six numbered outcomes below are recorded in the [worksheet](pilot-worksheet.md#progress-and-evidence); their numbers are unchanged, grouped by layer.

**The loop** (Part 0, sections 1–2)

- **1.** Locate the model response and distinguish a proposed tool call from actual dispatch.
- **2.** Match a call/result ID and locate that feedback in subsequent inference input.
- **3.** Explain repeated feedback after a tool error, separating scripted recovery from model observation.
- **6 (first half).** Locate which file and history contents reach the next request.

**Controls and evidence** (sections 4–5, loop recap)

- **4.** Change a controller budget and explain which operations ran and why the loop stopped.
- **5.** Check the task outcome separately from conversation completion.
- **6 (second half).** Explain why ordinary tool feedback does not update model weights.

Demonstrate these with a saved run, a prediction or variation and your own explanation. A successful command alone does not establish understanding.

## What you need

Basic Python functions, lists/dictionaries and terminal use; Git, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python **3.12+** (default 3.12, installed below). The core needs no model, API key or Docker.

Planning estimate: **30–45 minutes for Part 0 plus 2–4 focused hours for the numbered core route below**, excluding first-time setup, companion lessons and further exercises. This is provisional, not measured learner time. Individual lesson-page estimates cover their fuller exercises, including reconstruction or execution where stated; they are not additive requirements for this route. Record actual setup and learning time separately.

Author checks used Linux x86_64 with bash and Python 3.12; CI also checks Python 3.13. Native Windows, macOS and physical Pi operation have not been validated. Windows users can use a Linux terminal in WSL for these commands, but WSL has not been independently checked here. Use the actual paths printed on your machine; learner runs are retained under this checkout's ignored .cache/exercises/track-1/ directory. [Observed environments and limitations](VALIDATION.md).

## Prepare once

In a terminal, get the repository and enter it:

```bash
git clone https://github.com/jschell/sec-lm-learning-track.git
cd sec-lm-learning-track
uv python install 3.12
uv sync --frozen
```

If you already have a checkout, enter its root and run the last two commands. Initial preparation may need network access. Each run creates `.cache/exercises/track-1/<exercise>/<run-id>/` with its work files, trace.jsonl and result.json (summaries for comparisons/checks have no model outcome). Commands print the paths; earlier runs are retained. Record the run path directly—no evidence-copy step is needed. [Retention and manual cleanup](pilot-worksheet.md#preserve-your-evidence).

The following core commands run offline with the supplied replay and bounded real file operations, using [uv's frozen project workflow](https://docs.astral.sh/uv/guides/projects/).

<a id="start-and-inspect"></a>
<a id="learning-path"></a>

## One core route

Start with Part 0, then follow the [worksheet](pilot-worksheet.md). Every core page ends with a **Next in core** link; lessons are supporting explanations that return you to it.

0. [Part 0: the loop](00-the-loop.md). Five short steps in Huntley's order: a conversation, a tool definition, one exchange, the loop with an error, the same loop with more tools. Predict, then run and watch a live transcript. This is the base for everything after it.
1. [Worksheet section 1: one exchange](pilot-worksheet.md#1-follow-one-exchange). Six short steps: run stages 1 and 2, find the call, its dispatch and its matching result, then predict and run a one-command missing-file variation. [Lessons 1](01-minimal-inference.md) and [2](02-one-tool-exchange.md) explain these steps.
2. [Section 2: error feedback](pilot-worksheet.md#2-follow-feedback-after-an-error). Inspect repeated requests and returned errors. [Lesson 3](03-author-the-loop.md) explains the loop.
3. Recap: [the loop on one page](core-loop.md). Compare what you ran with the whole mechanism, including the guards you will test next.
4. [Section 4: budget variation](pilot-worksheet.md#4-change-one-controller-setting). Predict and compare two settings. [Lesson 5](05-control-and-inspect.md) explains stopping behavior.
5. [Section 5: read-only transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool). Locate registration, dispatch and feedback, then complete [the wrong-answer diagnosis](06-transfer-tool.md#diagnose-a-wrong-final-answer).
6. [Explain and record completion](pilot-worksheet.md#explain-and-record-completion) against the six outcomes above.

**[Start: Part 0, the loop](00-the-loop.md)**

Worksheet section numbers identify activities; lesson numbers identify supporting explanations. Sections 3 and 6 are optional further exercises, marked as such where they appear. Complete worked functions are supplied: run, predict, inspect, vary and explain before considering reconstruction.

Use `uv run --frozen --offline python learn.py --help` to discover commands. For a structured assessed pilot, a facilitator follows [the protocol](../../docs/pilot/README.md) using this same core plus the separately named **Select evidence** companion. Evidence selection is not an additional Track 1 completion requirement.

## Apply it: an agent says "I disabled the account"

Once the loop is familiar, apply it to a review question. An agent reports "I disabled the account." Did it only propose a call, did the controller invoke the tool, what did the returned result report, and what independent account-state read-back would verify the change? A final success message alone does not answer those questions. The completion step asks you to answer this from your own traces. This is an illustrative question; the lab operates only on synthetic local files.

<a id="completion-and-modes"></a>

## Going further

Choose an activity after the core; these do not form a second required sequence. Most are **focus areas** that build on the loop: containment and execution (Lesson 4), untrusted input (Lesson 7), guards (Lesson 8). They assume Part 0 and the core.

| Activity | Starting point | Additional scope |
| --- | --- | --- |
| Reconstruct the loop or tool | [Part 0's optional step](00-the-loop.md#optional-write-the-loop-yourself), starters in [Lesson 3](03-author-the-loop.md) and [transfer](06-transfer-tool.md) | Author code, then compare worked behavior |
| Inspect repair or run a program | [Worksheet section 3](pilot-worksheet.md#3-separate-a-file-edit-from-program-execution), [Lesson 4](04-complete-a-task.md) | Replay edits real files; genuine command execution requires the Docker extension |
| Follow untrusted input | [Worksheet section 6](pilot-worksheet.md#6-locate-untrusted-instructions), [Lesson 7](07-untrusted-content.md) | Locate injected text in supplied input; no model-resistance claim |
| Fix a broken exchange or loop | `learn.py fix`, from [Lesson 2](02-one-tool-exchange.md#optional-fix-a-broken-exchange) and [Lesson 3](03-author-the-loop.md#optional-fix-a-loop-that-hides-errors) | Three one-defect files with targeted checker messages and two-rung hints |
| Learn missing guards | [Lesson 8](08-learn-from-missing-guards.md) | Recording-only comparison; guard authoring/checks remain separate from core completion |
| Observe a local model | [360M/example recipe](../../modules/tool-requests-and-feedback/README.md#run-the-observed-working-configuration) | Blank-slate CPU setup, downloads and teaching text adapter; successes and failures retained |
| Observe a hosted model | [Hosted guide](live-observation.md) | Provider credentials and actual inference; task accuracy checked separately |

## Reference

[Worksheet](pilot-worksheet.md) · [Implementation](lab/loop.py) · [Trace format](trace-format.md) · [Validation and test commands](VALIDATION.md) · [Sources](SOURCES.md)

## What this lab does and does not show

The core establishes familiarity with the loop and its controller. Replay responses are authored, file operations are real, and command observations are scripted. It does not establish model competence or production security. [Back to collection](../../README.md).
