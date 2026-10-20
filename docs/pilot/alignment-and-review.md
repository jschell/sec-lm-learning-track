# Alignment and quality review

Status: author preparation; independent human review and learner evidence pending. This is a research-informed local instrument, not a validated curriculum.

## Objective and evidence map

The required route is in [the protocol](README.md), which follows the [Track 1 core](../../tracks/01-author-the-loop/README.md#one-core-route) plus the named selection companion. Track 1's six progress outcomes use the worksheet as the learner-facing record. Pilot IDs O1–O5 below remain stable; they are not a second numbering of the core outcomes. Each assessment item asks for a mechanism or evidence, rather than command recall.

Core outcomes 1/2/5/6 map to O1/O2/O3/O4. Since Plan 17, Part 0 (decision 0003) adds learning activities for O1, O2 and O4; assessment items, keys and objectives are unchanged. Outcome 5 includes the authored wrong-final-answer diagnosis in the existing transfer lesson. Outcome 6 separates inspecting supplied file/history content from explaining the training distinction; replay does not measure weights. Core outcome 3 (error recovery) and outcome 4 (budget variation) have direct evidence checks in worksheet sections 2 and 4; there is no separate pre/post item for each. O5 belongs to the Select evidence companion and is not a Track 1 completion requirement. Do not infer full core coverage from the five-form score alone.

| Objective | Explanation and worked example | Learner action | Assessment |
| --- | --- | --- | --- |
| O1 Locate inference versus dispatch | Part 0 steps 2–3; Track 1 core loop and worksheet sections 1–2 | Locate a proposed call and its actual implementation invocation | A1/B1/C1; T1 |
| O2 Trace matching feedback into input | Part 0 steps 3–4 and request N+1; worksheet section 2, repeated error feedback | Match call IDs and inspect the next request | A2/B2/C2; T2 |
| O3 Separate completion from correctness | Worksheet sections 4–5, finite stop and read-only transfer | Compare stop state with task requirements and actual output | A3/B3/C3; T3 |
| O4 Separate saved state, supplied input and weights | Part 0 step 1 (re-sent history); core loop history; selection lesson's candidate versus selected evidence | Inspect history and compare full evidence with selected input | A4/B4/C4; T4 |
| O5 Detect selection loss | Context and state Lesson 2, literal selection | Change only the query and identify omitted coverage information | A5/B5/C5; T5 |

Prerequisites are basic Python reading and terminal use. The supplied examples define inference (a model response), dispatch (the controller invokes a tool implementation), tool result and subsequent input. The transfer gives the entire lookup contract and relevant events; it assesses no SIEM product knowledge. Docker, provider setup and optional guard reconstruction are not assessed.

## Focused review

| Issue | Preparation change |
| --- | --- |
| Unbounded route | Worksheet sections 1, 2, 4 and 5 plus one selection lesson; other exercises remain optional |
| Repeated process/status material | Pilot entry points link this protocol and the existing validation record |
| Viewer omits authority details | Separate proposal, permission, simulation and observed-effect summaries; raw JSONL remains authoritative |
| Tokenizer called offline from clean checkout | Module now explicitly requires online dependency/asset preparation before offline inspection/tests |
| Local recipe overstates reliability | Observed 360M successes and failures are both named; existing anchors and failure records retained |
| CI change looks like a new task grade | Integration requirements changed after a failure; exact-answer criteria and failed task grades did not, as recorded in [decision 0002](../decisions/0002-feedback-integration-and-model-outcomes.md) |
| Input presence called semantic use | Describe feedback supplied in subsequent input; a trace cannot establish semantic use |

Forms A/B have the same item structure with changed values. That is an author design choice, not measured equivalence. An independent reviewer should check difficulty, contracts and keys before interpreting score differences. The unfamiliar transfer supplies all facts but does not measure real engagement performance. Record exposure to this public material.

## Author command audit

Checked 2026-10-18 UTC by the author on Linux x86_64, uv 0.12.23 and CPython 3.12.15. A detached worktree at main `b64642ad92e0304900a33a78bc7d2c7caaac44e2` received this change's candidate files before command execution. `uv python install 3.12` retrieved the interpreter; `uv sync --frozen` created a new environment. Git/uv, OS tools, network access and the host package cache already existed. This is a fresh-checkout/environment desk check, not a fresh OS or Pi test.

| Required command/action | Actual observation |
| --- | --- |
| `learn.py stage 1` | One synthetic inference; no tool execution |
| `learn.py stage 2`, then `learn.py trace` with its actual path | Two requests; matching read-1 call/result and actual work/notes.txt bytes in the second request; viewer showed history location |
| `learn.py stage 3` | Five requests, three error results, successful read, completed; four actual dispatches |
| `learn.py --scenario multi` | Completed, two actual tool calls |
| Same with `--max-calls 1` | tool_limit, zero calls; exit status 0 as documented |
| `learn.py transfer` | Actual count_lines dispatch, two lines, matching feedback, VERIFIED |
| Selection with default query | E01/E02 retained; C01 coverage gap omitted |
| Selection with `--query 'collection gap'` | C01 retained; E01/E02 omitted |
| Relevant unit suites | 46 Track 1 plus 7 context tests passed through frozen/offline uv |

All Python lab commands above used `uv run --frozen --offline python` and the exact route arguments in the protocol. The trace placeholder was replaced with the actual Stage 2 path. Generated artifacts were inspected in the fresh worktree's ignored `.cache/pilot-author-audit/` and each printed temporary workspace; those host-specific artifacts are not learner records.

Outside the required learner route, author QA generated the existing authority fixture and displayed its trace through learn.py: proposed, permission, simulation and observed_effect labels were present, with recorded operations explicitly executed=false. New regressions check denied versus executed labels, recording-only effects, untrusted text remaining data and unknown event visibility. Changed relative Markdown links and whitespace were checked. No model, credentials, tokenizer or Docker was needed; no independent person or live-model observation occurred.

## Independent human review record

Status: pending. Reviewer role/date/revision: not recorded. No author or AI desk review counts as a second human review.

Give the reviewer the assessment forms, general 0/1/2 anchors and sample responses S1–S6 without the author's sample scores. Ask them to check clarity, factual correctness, form comparability and whether each item tests its mapped objective. They should score before comparing with the key. Preserve initial disagreements, discuss their cause and revise ambiguous wording before a session. Simple agreement counts are descriptive, not a reliability validation.

| Sample | Independent initial score | Author score compared afterward | Disagreement and resolution |
| --- | --- | --- | --- |
| S1 | Pending | Pending | Pending |
| S2 | Pending | Pending | Pending |
| S3 | Pending | Pending | Pending |
| S4 | Pending | Pending | Pending |
| S5 | Pending | Pending | Pending |
| S6 | Pending | Pending | Pending |

Release states are distinct: **author-prepared** means artifacts and technical checks complete; **independently reviewed** requires the real reviewer record; **learner-piloted** requires actual responses and session evidence. Keep missing delayed checks missing. Fix a technical blocker or ambiguous item, then use observed misconceptions and assistance to select further changes. Pause new modules until the initial walkthrough informs that choice. Preserve form/rubric revisions and original responses; do not retrofit old scores into passes.

## Original foundations

Sources verified 2026-10-17 (America/Los_Angeles):

- National Research Council, [Knowing What Students Know: assessment foundations](https://www.nationalacademies.org/read/10019/chapter/3) (2001): connect intended understanding, observations and interpretation.
- CMU Eberly Center, [performance-based prior knowledge assessment](https://www.cmu.edu/teaching/assessment/priorknowledge/performancebased.html): observe performance rather than confidence alone.
- IES, [Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1): worked examples, problems and explanatory questions inform the route.
- National Research Council, [How People Learn: learning and transfer](https://www.nationalacademies.org/read/9853/chapter/6) (2000): application to a changed situation informs the unfamiliar transfer.

These principles do not validate these custom questions for adult security professionals. Forms, rubric, timings, delayed interval and release rules are original project choices. Instructional source attribution remains beside the original lessons.
