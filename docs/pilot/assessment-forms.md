# Assessment handouts

Original synthetic questions for this pilot. Give the learner only their assigned form/case, without the facilitator key, sample scores or the other forms. These are authored excerpts, not captured model behavior or requests to send. No program needs to run. Keep answers short but identify the relevant operation, message or record. Unknown facts must remain unknown.

## Form A

**A1 — Request versus execution.** An inference response contains:

```json
{"type":"tool_use","id":"a-4","name":"read_file","input":{"path":"report.txt"}}
```

The controller stores this dictionary in its message list and stops before invoking a tool. Has the file been read? Identify the operation that would be needed and who performs it.

**A2 — Feedback linkage.** The assistant's call has ID `a-4`. A result appended to the following request is:

```json
{"type":"tool_result","tool_use_id":"a-9","content":"GREEN","is_error":false}
```

What defect is visible, what should the controller associate, and what does `is_error: false` fail to establish?

**A3 — Outcome.** The task requires the exact string `GREEN-14`. The last assistant text is `GREEN-41`, and the harness records `stop: completed`. Did the task pass? Give the separate check and explain the meaning of the stop.

**A4 — State.** A process saved `report.txt` containing `GREEN-14`. A later process constructs a request containing only `"Report the saved result"`; no file read or earlier conversation is supplied. Does this request show the saved bytes reaching inference? What must the application do? Does saving or appending text demonstrate a weight update?

**A5 — Selection.** A corpus has these records; a literal selector keeps only text containing `mira`:

```text
R1: mira attempt 31 was denied by the identity source.
R2: mira attempt 31 was allowed by the application source; disagreement unresolved.
G1: Collection unavailable from 12:03 to 12:06 UTC.
R3: Unrelated service health check passed.
```

Which records enter the selected input, which relevant information is lost, and can that input justify “no later activity occurred”?

## Form B

**B1 — Request versus execution.** An inference response contains:

```json
{"type":"tool_use","id":"b-7","name":"read_file","input":{"path":"summary.txt"}}
```

The controller stores this dictionary in its message list and stops before invoking a tool. Has the file been read? Identify the operation that would be needed and who performs it.

**B2 — Feedback linkage.** The assistant's call has ID `b-7`. A result appended to the following request is:

```json
{"type":"tool_result","tool_use_id":"b-2","content":"AMBER","is_error":false}
```

What defect is visible, what should the controller associate, and what does `is_error: false` fail to establish?

**B3 — Outcome.** The task requires the exact string `AMBER-25`. The last assistant text is `AMBER-52`, and the harness records `stop: completed`. Did the task pass? Give the separate check and explain the meaning of the stop.

**B4 — State.** A process saved `summary.txt` containing `AMBER-25`. A later process constructs a request containing only `"Report the saved result"`; no file read or earlier conversation is supplied. Does this request show the saved bytes reaching inference? What must the application do? Does saving or appending text demonstrate a weight update?

**B5 — Selection.** A corpus has these records; a literal selector keeps only text containing `niko`:

```text
S1: niko attempt 62 was denied by the identity source.
S2: niko attempt 62 was allowed by the application source; disagreement unresolved.
H1: Collection unavailable from 15:08 to 15:11 UTC.
S3: Unrelated service health check passed.
```

Which records enter the selected input, which relevant information is lost, and can that input justify “no later activity occurred”?

## Unfamiliar transfer: event lookup

All contracts and evidence are supplied here. No SIEM expertise or API implementation is required.

`lookup_event(event_id)` is a read-only Python function returning the matching synthetic record. The controller has registered it and validates string IDs. Only calling this function performs the lookup; no automatic database retrieval occurs. In this case, the exact task is to report the disposition of T52.

```text
Source record T52: disposition=blocked
Separate source note COVERAGE: collection unavailable 17:12–17:14 UTC

1. Controller supplies the user task and lookup_event definition to inference.
2. Assistant proposes lookup_event({"event_id":"T52"}), call ID t-8.
3. Controller dispatches it; actual result is {"event_id":"T52","disposition":"blocked"}, linked to t-8.
4. Controller builds the next request from only the original user task, dropping the call and result.
5. Assistant returns "allowed"; harness records completed.
6. A saved candidate evidence packet selects only rows whose event_id is T52; COVERAGE has no event_id.
```

Answer five questions:

- **T1:** Which step actually retrieves the record, and which only proposes it?
- **T2:** What history defect occurs at step 4? Show the call/result information that should reach the next request, including the ID.
- **T3:** What outcome check fails, despite completion? Does a correct tool result guarantee a correct final answer?
- **T4:** Does the separate saved COVERAGE note enter inference in the shown requests? What step would make it available, and is that a weight update?
- **T5:** What relevant information does step 6 omit? Could the selected packet establish absence of activity during 17:12–17:14?

## Delayed Form C

Use 3–7 days later; record actual interval, intervening practice and answer-key exposure. Do not provide the prior lesson/key during the check. This is a new form, not proof of equivalent difficulty.

**C1:** An assistant proposes `read_file("outcome.txt")`, ID `c-3`. The controller logs that proposal but calls no tool. Has execution occurred? Explain the missing transition.

**C2:** The assistant call ID is `c-3`; the next request contains a result with `tool_use_id: "c-8"` and `is_error: false`. Diagnose and correct the association. What does the false error flag not establish?

**C3:** The exact task expects `OPEN-36`; the assistant returns `OPEN-63` and the loop says completed. Grade the task separately from the stop.

**C4:** `outcome.txt` persists after a process exits. A new request contains only `"Summarize the saved result"`, without reading the file or supplying its history. Explain what is absent, how to supply it, and why that action does not train the model.

**C5:** A selector retains only text containing `sora`:

```text
U1: sora attempt 73 denied in identity audit.
U2: sora attempt 73 allowed in application audit; disagreement unresolved.
J1: Collection unavailable 18:04–18:07 UTC.
U3: Unrelated health check passed.
```

Identify included records, the relevant omission, and whether the selected input establishes no later activity.

## Reviewer calibration samples

These are deliberately authored candidate responses, not learner results. Give them to the second human reviewer with the general scoring rules, withholding the author's proposed scores until the reviewer has recorded theirs.

| Sample | Item | Candidate response |
| --- | --- | --- |
| S1 | A1 | “No. The dictionary requests work; the controller must dispatch read_file to the file-reading implementation.” |
| S2 | A1 | “No, it still needs another step.” |
| S3 | A1 | “Yes, because the model named read_file.” |
| S4 | A2 | “The ID is wrong.” |
| S5 | A3 | “Pass: completed means the task finished successfully.” |
| S6 | A5 | “R1/R2 survive; G1 is omitted. The gap and source disagreement prevent claiming no later activity.” |

Question design and timing are project choices. The [alignment record](alignment-and-review.md#original-foundations) cites the assessment/prior-knowledge/transfer foundations. Keep these assessment items separate from worked instruction until their assigned check.
