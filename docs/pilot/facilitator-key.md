# Facilitator key and scoring anchors

Author-created key, not observed learner results. Distribute only after the relevant checks. Record any prior exposure; public repository separation cannot guarantee an unseen assessment.

## Scoring

Score each objective separately: **0** incorrect or missing in an attempted item; **1** partially correct but missing the mechanism or necessary evidence; **2** correct with a sound mechanism/evidence explanation. Accept equivalent concise explanations. Mark **NA** if unadministered or interrupted; missing follow-up is not zero or a retention pass. Do not set a total-score certification threshold.

Record assistance separately: **N** none, **V** navigation clarification, **H** conceptual hint, **W** worked explanation. Capture the initial answer before corrections and retain revisions separately. An answer reached with H/W is not independent performance. Log V as well, even if it supplies no conceptual content.

| Objective | 0 example | 1 example | 2 anchor |
| --- | --- | --- | --- |
| O1 Inference/dispatch | Naming a tool executed it | Says execution is separate without locating the step | Distinguishes the proposal from invocation of the implementation |
| O2 Feedback | Unmatched result is enough | Notices a mismatch but cannot repair the sequence | Identifies matching IDs, actual result provenance and inclusion in the subsequent request |
| O3 Correctness | Completed means correct | Notices an issue without checking the requested outcome | Compares exact requirement/output and explains why completion is insufficient |
| O4 State/input | Disk save updated weights or supplies every later request | Says information is missing without a retrieval/input step | Explains explicit retrieval/inclusion and separates ordinary history from weight training |
| O5 Selection | No selected event proves no activity | Notes omission without interpreting its consequence | Identifies the lost coverage/contradiction and limits the conclusion |

## Forms A/B/C

| Objective | Expected mechanism and values |
| --- | --- |
| O1 | No read happened: the controller stopped after a proposal and before invoking the file tool. Naming the function does not invoke it. |
| O2 | A: a-4/a-9; B: b-7/b-2; C: c-3/c-8 mismatch. The non-error flag establishes neither correct call association nor correct task output. Obtain/associate the actual result of the executed call and include the assistant call plus matching result in the next request. Rejecting/investigating the mismatch is acceptable; blindly relabeling arbitrary text is not a valid repair. |
| O3 | A requires GREEN-14, returns GREEN-41; B requires AMBER-25, returns AMBER-52; C requires OPEN-36, returns OPEN-63. Each fails the stated requirement despite completed status. |
| O4 | Saved bytes are not automatically in a new request. Read/retrieve and include them explicitly; appending ordinary messages or saving a file does not train weights. Do not infer unobserved provider internals. |
| O5 | A retains R1/R2 and drops G1; B retains S1/S2 and drops H1; C retains U1/U2 and drops J1. The coverage gap is relevant, and the differing event records do not justify absence of activity. Unrelated health entries are not the consequential omission. |

## Unfamiliar transfer

- **T1:** Step 2 proposes lookup; step 3 actually invokes it and records its result.
- **T2:** Step 4 drops the assistant call and result. Include the lookup_event proposal for T52 with ID t-8, then its actual matching tool result reporting blocked, in the subsequent request. A correctly executed tool alone does not supply feedback to the model.
- **T3:** The final allowed contradicts the supplied blocked disposition. Completed does not prove task correctness.
- **T4:** Saving COVERAGE does not put it in input. Retrieve/include it when needed; this is ordinary state handling, not weight updating.
- **T5:** Filtering for event_id T52 drops COVERAGE because it has no event_id. Its gap prevents a claim of complete observation/no other activity.

## Calibration sample scores

Compare only after the independent reviewer scores S1–S6 without these author scores.

| Sample | Author score | Reason |
| --- | --- | --- |
| S1 | 2 | Correctly separates request and invocation |
| S2 | 1 | Correct direction, unspecified missing step |
| S3 | 0 | Treats naming the tool as execution |
| S4 | 1 | Detects mismatch without explaining association/input repair |
| S5 | 0 | Equates completion with task success |
| S6 | 2 | Identifies selected evidence, lost gap and invalid absence claim |

If reviewers disagree, retain both initial scores and the rationale before reconciliation. Version any changed item/rubric; retain original responses and do not silently rescore historical failures into successes.

The [assessment foundations and limits](alignment-and-review.md#original-foundations) apply to this project-authored key. It is not a standardized instrument.
