# Review: one sampled lesson from each self-directed learning exemplar

Status: author review, 2026-10-20 (UTC). One lesson or exercise was sampled from each course named in an owner-supplied research summary on self-directed, text-first interactive learning (compiled 2026-10-19). The summary's recommended entry points were used where it named them. This is a pattern review, not evidence that any pattern improves Track 1 learning. No upstream text or code is copied into the project.

## Scope and method

| Course | Sample read | How it was read |
| --- | --- | --- |
| University of Helsinki, Python Programming MOOC 2026 | Part 1 §1 "Getting started"; common error messages page; exercise counts for Parts 8 and 12 | Repository source |
| futurecoder | Chapter 4 pages "Building up strings" and its exercises, including hint and message steps | Repository source |
| The Carpentries, Plotting and Programming in Python | Episode 12 "For Loops" | Repository source |
| Exercism Python track | Concept exercise "making-the-grade": design, introduction, instructions, hints, stub and tests | Repository source |
| Runestone, Foundations of Python Programming | Chapter 1 "Predict Before You Run!" and "To Understand a Program, Change It!"; Iteration "The Accumulator Pattern" | Repository source; the published site returned HTTP 403 |
| CS Circles (Waterloo CEMC) | Lesson 1E "Errors" | Published page through a summarizing fetch tool; raw page text was not inspected |
| Rustlings | Functions README, exercise functions3, its hint and solution, watch-mode usage page | Repository source |
| Think Python, 3rd edition | Chapter 5 notebook: debugging, "Ask a virtual assistant" and exercises | Repository source |
| Kaggle Learn, learntools | Python exercise 2 checker definitions and the ThoughtExperiment class | Repository source |

Not reviewed: OLI courseware (requires an account), pythonwhat, the method sources (Teaching Tech Together, the PRIMM paper) and the research claims in the summary (doer effect, Parsons-problem and PRIMM effect sizes). Those claims remain **unverified candidates** under the [citation policy](../citation-policy.md). The Helsinki hidden tests are not in the content repository and were not inspected.

## Observations by course

Each item below describes the sampled material in original wording. "Track 1 relevance" entries are project judgments.

### Helsinki MOOC

- The section opens with a "Learning objectives" box of three outcomes ("After this section… You will be able to…").
- Each concept is a code block, then a sample-output block, often followed at once by an exercise. Part 1 §1 has 5 exercises in 228 lines. Later material is sparser: Part 12 sections run 276–750 lines with 2–7 exercises.
- A deliberate error appears early with its real traceback: the missing-quotes `print`.
- The exercises include a "Fix the code" variant: reorder seven `print` lines into alphabetical order. This is effectively a reorder (Parsons-style) task presented as fixing code.
- There are no closing key points; the section ends after its last exercise.
- A standalone "Common error messages" page explains each message with a short broken example.

**Track 1 relevance:** objectives box, one output block per command and a separate common-errors page. Exercise density falls off for advanced material, so frequent practice is a choice, not something advanced topics impose.

### futurecoder

- The unit of content is a **step**, roughly one idea, one program and one run. Most "run this" steps first ask the learner to choose the expected output from multiple choices. The distractors encode specific misconceptions, such as the output if the loop body ran in the wrong order.
- **The explanation of a result comes in the next step**, after the learner has predicted and run. The design itself keeps the answer hidden.
- One step asks what happens if two lines are swapped, predicted then run. This is a one-factor modification.
- Hints are an ordered list revealed one at a time, from orientation ("make sure you're not working from the broken version") to near-solution ("Use an empty string!"). Some exercises also offer the solution as a Parsons puzzle (`parsons_solution = True`).
- **Message steps** pair a plausible wrong solution with a targeted message. For example, a solution that adds a space before printing gets "Almost there! You have one space too many…" and a pointer to the order of the code.
- Test inputs differ from the instruction example ('World' shown; 'Bob' also tested).
- Pages close with a short `final_text` that names the general pattern. The tone is warm and brief.

**Track 1 relevance:** this is the strongest single model. The Track 1 checker already detects plausible wrong implementations (fabricated answer, lost history), so those failures could carry futurecoder-style targeted messages. "Explanation follows the run" is the structural fix for predictions answered in advance.

### Carpentries episode

- The front matter has `teaching: 10` and `exercises: 15` minutes, then `objectives` (verbs: explain, trace, write) and a single priming `question`.
- **Every heading is a complete claim** ("A `for` loop is made up of a collection, a loop variable, and a body."), and the closing `keypoints` repeat those headings almost verbatim. The structure produces the summary.
- Prose is short bullets under each claim, with `output` and `error` blocks.
- All seven challenges come at the end of the episode, not between chunks. This episode does not support the summary's claim that practice is interleaved with explanation. Each challenge has a collapsible solution.
- The "Tracing Execution" challenge asks for a table of executed line numbers and variable values per iteration.

**Track 1 relevance:** claim headings that become key points; a trace table (request number → messages added → calls used → status) suits the agent loop well. The Carpentries model is instructor-led, so self-directed use needs more feedback than these collapsible solutions give.

### Exercism concept exercise

- `.meta/design.md` has Goal, Learning objectives, Out of scope, Concepts, Prerequisites and Resources. It is written for maintainers, not learners.
- `instructions.md` frames the work as a story ("You're a teaching assistant correcting student exams") with six numbered tasks, each with one example call.
- **The examples in the instructions differ from the test data.** The task 2 example input is not among the test cases.
- `hints.md` has general hints and then hints per task. They point to documentation and concepts and never give code.
- Test failure messages state the call, the actual result, the expected result and what the value means: "Called count_failed_students(…). The function returned …, but the tests expected … for the number of students who failed."
- Tests are tagged by task number.

**Track 1 relevance:** story framing tied to the learner's work, per-task hints, and failure messages in the form call/observed/expected/meaning. Track 1 checker messages already state expected versus observed; adding "what this means" would match.

### Runestone FOPP

- The chapter 1 pages "Predict Before You Run!" and "To Understand a Program, Change It!" are short **advice** pages, not exercises. Their key idea is that "a prediction is not a random guess": it rests on an explanation of current state. The summary's description of them as PRIMM-style pages overstates them.
- "The Accumulator Pattern" names the pattern's anatomy (initialize, iterate, update). It then gives runnable code, a step-through visualization of the same code, a prediction prompt, a multiple-choice question and a Parsons problem.
- **Each multiple-choice distractor has its own feedback**, including partial credit for a nearly right answer ("Good thought: … But then…").

**Track 1 relevance:** ask learners for a reason with each prediction, name the anatomy of the agent loop explicitly, and give feedback per distractor for any multiple-choice check. The Skulpt in-browser runtime and the GFDL license make the platform and text unsuitable to adopt; only the patterns are relevant.

### CS Circles (summarized page; lower confidence)

- The lesson alternates short explanation with labeled examples of syntax, run-time and logic errors.
- It has three fix-it exercises with **edit limits** ("You can change at most one character"; "at most two characters"), enforced by the grader.
- A side note suggests reading code aloud (rubber-duck debugging), and the lesson ends by pointing to the next lesson.

**Track 1 relevance:** an edit limit turns "fix this" into "find the exact defect", for example "fix this exchange by changing one line". The observation should be rechecked against the raw page before citing it.

### Rustlings

- Each topic folder has a README of a few lines that points to the Rust Book for reading. Exercises are tiny, compilable-or-not files with a `TODO` comment at the defect site.
- The hint for an exercise is one or two sentences that **narrow where to look** without naming the fix ("the function declaration is okay, but there's something wrong with the place where we are calling the function").
- The solution file mirrors the exercise path and adds a one-line comment explaining the fix.
- A watch mode re-runs the current exercise and shows the hint on `h`. Quizzes are interleaved: 3 quizzes among 95 exercise entries.

**Track 1 relevance:** it is the closest in form (offline, file-based, CLI-driven). "Hint narrows the location" is a good first rung for the hint ladder. Watch mode itself is not proposed.

### Think Python, 3rd edition (one chapter)

- Each chapter notebook runs deliberate errors in cells (an `%%expect` cell magic) and has its own **Debugging** section. One example shows an error reported on line 5 when the defect is on line 4, then advises reading error messages carefully without assuming they are correct.
- "Ask a virtual assistant" exercises have the learner ask an AI assistant to explain or fix code, then **paste the answer back and test it**.
- The exercises are self-checked with no grader. The repository has no license file at its root, and the README states no license; reuse terms were not established.

**Track 1 relevance:** "the error report is not necessarily the location of the defect" and "verify the assistant's claim by running it" both match the core Track 1 distinction between a claim and independent evidence.

### Kaggle learntools

- Each problem class carries a hint, a solution and test cases. `ThoughtExperiment` problems have no automatic check and reveal the solution when the learner checks.
- A "Debug" thought experiment (explain why this fails) is paired with a "Fix" problem (make it pass) in one multipart problem.
- The repository says it is not designed to work outside Kaggle Learn.

**Track 1 relevance:** the explicit split between checkable problems and thought experiments matches Plan 13's planned separation of mechanical checks from self-checks on interpretation. The explain-then-fix pair is a good shape for a Stage 2 defect exercise.

## Corrections to the research summary

- Carpentries challenges come at the end of the episode in the sample, not between chunks.
- Helsinki sections state objectives but have no closing key points; Carpentries and futurecoder provide the close-out.
- The Runestone "PRIMM" chapter 1 pages are short advice, although later chapters do embed predictions, multiple choice and Parsons problems.
- "Every exercise auto-checked" holds for futurecoder, Exercism, Helsinki and Rustlings. It does not hold for Carpentries or Think Python, and Kaggle marks some problems explicitly as unchecked thought experiments.

## Patterns most applicable to Track 1 (project judgments)

These are candidates for Plan 13 Stage D and later revisions. They do not commit the project to any change.

1. **Put the explanation after the run.** Present the prediction, then the command, then reveal the explanation (futurecoder's structure; collapsible solutions in Carpentries). Ask for a reason with each prediction (FOPP).
2. **Turn wrong implementations the checker already detects into learner messages.** Pair each with a short targeted message in the form observed/expected/meaning (futurecoder message steps, Exercism failure messages).
3. **Order hints to narrow the location first.** Where to look, then what relationship to check, then an annotated explanation (Rustlings, futurecoder, Exercism hints.md). Never give code in the first two rungs.
4. **Make fix exercises with edit limits.** For example, "this Stage 2 variant drops the assistant call; fix it by changing one line" (CS Circles, Rustlings, Helsinki "Fix the code"). Optionally precede it with "explain why this fails" (Kaggle).
5. **Add a trace table exercise.** Fill in, per request: messages added, calls proposed, calls dispatched, calls used and status (Carpentries "Tracing Execution").
6. **Use claim headings that become key points.** Each chunk's heading states the fact; the section ends by repeating them (Carpentries).
7. **Use story framing tied to the learner's work.** Carry the "agent says it disabled the account" review question through each section (Exercism).
8. **Keep examples separate from checks.** Worked examples and assessment items use different values (Exercism, futurecoder).
9. **Add a common-errors page** listing actual Track 1 diagnostics with a short cause and recovery for each (Helsinki).
10. **Separate checkable from interpretive items explicitly** (Kaggle ThoughtExperiment; consistent with Plan 13 Stage D).

Not applicable: browser runtimes (Skulpt, Pyodide), watch-mode tooling, mastery tracking or any platform dependency. These conflict with [decision 0001](../decisions/0001-worked-stages-first.md) and Plan 13's exclusion of a browser runtime or grading platform.

## Sources

Checked 2026-10-20 (UTC). Commits are the shallow-clone HEAD at review time. Licenses are recorded as stated in each repository; none of their material is reproduced here beyond short quotations.

| Source | Original location | Revision / license as stated |
| --- | --- | --- |
| University of Helsinki MOOC Center, Python Programming MOOC 2026 | [rage/programming-26](https://github.com/rage/programming-26) (`data/part-1/1-getting-started.md`, `data/error_messages.md`) | `ffa514db571c68b8e2d13b5c064437dd93ce4037`; README states Apache-2.0 |
| Alex Hall, futurecoder | [alexmojaki/futurecoder](https://github.com/alexmojaki/futurecoder) (`core/chapters/c04_for_loops.py`) | `def491c2a348371f56249d05c64e0cf70f33ac2b`; MIT |
| The Carpentries, Plotting and Programming in Python | [swcarpentry/python-novice-gapminder](https://github.com/swcarpentry/python-novice-gapminder) (`episodes/12-for-loops.md`) | `03c39315c48b6a13c4b887bb200cbcd83ac6915c`; instructional material CC BY 4.0 |
| Exercism, Python track | [exercism/python](https://github.com/exercism/python) (`exercises/concept/making-the-grade/`) | `6105f6d9d3ef66ce3d5c8f529d2882af3d76b706`; MIT |
| Miller, Ranum, Elkner et al., Foundations of Python Programming | [RunestoneInteractive/fopp](https://github.com/RunestoneInteractive/fopp) (`_sources/GeneralIntro/WP*.rst`, `_sources/Iteration/TheAccumulatorPattern.rst`) | `942ffb33bb62929d3e5eabaa8f027df0ed69d023`; GFDL 1.3 notice in source files |
| CEMC, University of Waterloo, CS Circles lesson 1E | [Errors](https://cscircles.cemc.uwaterloo.ca/1e-errors/) | Published page via summarizing fetch; Creative Commons icon shown, specific license not established |
| Carol Nichols et al., Rustlings | [rust-lang/rustlings](https://github.com/rust-lang/rustlings) (`exercises/02_functions/`, `rustlings-macros/info.toml`, `website/content/usage/index.md`) | `bc8e51115c9304fbd036f5d6fca683e71363468f`; MIT |
| Allen B. Downey, Think Python 3rd edition | [AllenDowney/ThinkPython](https://github.com/AllenDowney/ThinkPython) (`chapters/chap05.ipynb`) | `37024c68e6ccf30007bcf7f183670beebde013bc`; license not established from repository |
| Kaggle, learntools | [Kaggle/learntools](https://github.com/Kaggle/learntools) (`learntools/python/ex2.py`, `learntools/core/problem.py`) | `e9ba66dc899d3e17b80d3a1b9a5d29f430d310cb`; Apache-2.0 |
