# Track 1 learner pilot

Status: **not performed**. This is an original project usability check, not a claim that CI validates teaching effectiveness. The loop concept being taught is attributed to [Geoffrey Huntley](https://ghuntley.com/agent/).

Use [the pilot protocol](../../docs/pilot/README.md), separate assessment forms/key and blank session record. It selects worksheet sections 1, 2, 4 and 5 plus Context and state Lesson 2. Capture baseline responses before reading the explanations. Record every clarification; setup problems and conceptual help are different evidence.

The table below is an observation menu. Only the protocol's selected route is required; injection, reconstruction, models and Docker are optional extensions, not assessment prerequisites.

| Step | Observe / record |
| --- | --- |
| Prepare with uv | Platform, interpreter, unclear installation/environment assumptions |
| Run and inspect | Whether the learner finds the printed trace and distinguishes replay from a model call |
| Run request and exchange stages | Predict a change, inspect requests/feedback, explain actual execution; record help needed |
| Read the complete trace | The viewer summarizes events; Stage 2 feedback is in the second request/history rather than a standalone tool event. Can the learner find it without extra help? |
| Run and vary the loop | Explain repeated feedback and a finite stop; record confusion between short and guarded references |
| Read the one-page loop recap (after section 2) | Whether they identify model decisions, controller state, and actual tool execution; whether the Next-in-core links were followed without help |
| Transfer a read-only tool | Connect count_lines and explain registration/validation/feedback |
| Optional reconstruction | Whether starter and behavior-check guidance suffice |
| Error and stop limit | Whether they can explain the result without guessing |
| Injected-file walkthrough | Locate the instruction in tool-result data; distinguish host restrictions from model resistance |
| Local read-only, if setup available | Follow the explicit 360M/example route; record real file access, final task check and any setup blockers. No provider key is required |
| Hosted read-only, if credentials available | Complete predictions/observations; record unsupported provider behavior separately from local results |
| Optional Docker | Record actual execution separately from scripted observations |

Record date, approximate elapsed time, failed/unclear steps, exact documentation fixes, and completion level. Keep credentials and customer data out of notes. A successful first pilot can support usability confidence; it does not establish every platform or model is supported.

Finish when the learner can explain a run and deliberately change it, and identified instruction blockers are corrected. If neither live route is run, record controller familiarity only; inspecting an author's model record is not the learner's own model observation. Local results do not establish hosted-provider compatibility or physical Pi support. Source and model/hardware boundaries are recorded in [local-model validation](../../modules/tool-requests-and-feedback/VALIDATION.md).
