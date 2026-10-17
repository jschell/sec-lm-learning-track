# Decision 0001: runnable stages before reconstruction

Accepted 2026-10-16. Scope: Track 1 loop familiarity. This is the project's teaching decision, not an upstream requirement.

## Problem and decision

A large reference harness plus TODO starters makes a learner navigate transport, tracing and execution controls before seeing the loop. Checks accepting only a plausible return shape can also accept an implementation that skips inference or feedback.

Lead with complete runnable stages: one inference, one tool exchange, then repeated feedback. Ask learners to predict, inspect, modify and explain each stage. Keep reconstruction optional. Keep execution controls in the full reference harness and offer command execution as an extension. Add one small transfer exercise that connects count_lines to the existing loop.

Use narrow behavioral checks that observe actual requests, dispatch, feedback and stopping. Include regression submissions that fabricate a response, skip the second inference, or replace actual feedback. Bound the learner checker process to ten seconds. These checks support implementation feedback; they do not establish understanding, model competence, production security or resistance to deliberate cheating. Do not build a grading platform.

## Original sources and limits

[Geoffrey Huntley's workshop](https://ghuntley.com/agent/) and [inspected repository stages](https://github.com/ghuntley/how-to-build-a-coding-agent/tree/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e) provide the progressive complete-program teaching pattern. This project adds behavioral checks; it does not attribute a learner grader to Huntley.

[Stanford CS336's adapters](https://github.com/stanford-cs336/assignment1-basics/blob/main/tests/adapters.py) illustrate explicit interfaces connecting learner implementations to tests. [Karpathy's micrograd tests](https://github.com/karpathy/micrograd/blob/master/test/test_engine.py) compare computed behavior with a reference implementation. We adopt the principle of checking actual behavior, using our own small synthetic-model contracts. No upstream code or tests are copied. Sources checked 2026-10-16; these mutable links identify inspiration, not pinned executable dependencies.

## Consequences and review

Maintain the short worked stages alongside the guarded reference, with shared behavioral tests to detect drift. Keep replay, actual tool execution and live model observation explicitly distinct. Keep the Markdown lessons independently usable and source concepts beside their explanation. A fresh learner pilot remains required before claiming demonstrated usability; see the [validation record](../../tracks/01-author-the-loop/VALIDATION.md). Revisit the decision if a pilot shows the two implementations confuse learners or the optional reconstruction becomes a prerequisite in practice.
