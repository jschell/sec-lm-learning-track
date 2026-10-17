# Generation and sampling: validation

The selection criterion is usefulness for the lesson and bounded task, not comprehensive capability or a comparison with state-of-the-art assistants. Baseline: SmolLM2-135M-Instruct Q8_0. Exact artifacts are in [SOURCES.md](SOURCES.md).

## Implementation evidence

| Check | Current evidence |
| --- | --- |
| Authored four-token arithmetic | Runs locally; temperature concentration, normalization, top-k and repeatability checked |
| Client/server contract | Twelve standard-library tests pass with explicitly synthetic server responses; these are not model runs |
| Blank-slate setup | Pinned source/model preparation implemented; succeeded locally on Linux x86_64 from no runtime/model; source/model/notices prepared in approximately 333 seconds, excluding system/uv installation |
| Actual model generation and task outcomes | Native API/probabilities, temperature/top-k changes, matching seeded IDs, EOS and output cap observed. Exact OK reply and extraction failed; opposite-word calibration identified cold, then continued to the token cap |
| Physical Raspberry Pi 4 | Not tested |
| Independent learner walkthrough | Not performed |

Repeat client/math checks:

```bash
uv run --frozen --offline python -m unittest discover -s modules/generation-and-sampling/lab/tests -v
```

The separate actual-model smoke command builds no infrastructure itself; after preparation it starts a dedicated server, records observations, and stops that server:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/verify_model.py > /tmp/generation-observations.json
```

This is separate from the synthetic contract suite. Inspect task_checks and experiment outputs; the smoke process checks API fields and a deliberate token cap, not broad model quality. CI retains its actual observations as an artifact.

## Model and hardware validation checklist

Record pass, fail or not attempted beside each item, with the actual output/command. Failing an exercise is evidence to explain, not a reason to relabel an output or move the goalposts.

- [x] Model provenance: selected model/revision, quantizer revision, GGUF SHA-256 and license match the setup manifest.
- [ ] Full fresh-OS walkthrough (runtime/model setup succeeded on Linux x86; compiler/Git were already present): a fresh 64-bit Linux setup can install prerequisites, build the runtime, fetch the model and start its own server with the written commands.
- [x] Runtime/API on the pinned x86 build: actual responses contain IDs, candidate probabilities, stop reason and timing fields understood by the client. Record server commit and alias; a reported name alone does not prove model identity.
- [ ] Instruction/task usefulness: run reply, extract and rewrite. Preserve actual answers and assess the stated checks. At least one simple instruction and one bounded task should work clearly enough for the lesson; no general assistant score is required.
- [x] Probability observation: identify the selected token and candidate probabilities. Show retained/unreported probability mass without renormalizing a top-N subset.
- [x] Sampling variation: hold task/settings fixed except temperature or top-k; compare the first-token distributions and later outputs with their changed context acknowledged.
- [x] Repeatability on the tested build: repeat the same seed and input on the same build/hardware; record whether IDs match, including failures. Do not generalize across runtimes.
- [x] Termination: observe both an actual EOS stop and an output-limit stop. If EOS is absent within the bound, leave that part open.
- [x] Failure interpretation: preserve a failed/limited response and explain the observed cause or uncertainty. Do not require a destructive operation to demonstrate failure.
- [ ] Portability: repeat the lesson on physical Pi 4, with RAM variant, 64-bit OS, cooling, runtime commit, thread count, context and quantization recorded.
- [ ] Resources: measure build/download duration and disk use, server peak RSS, swap/throttling, prompt-processing time, decode tokens/sec and bounded-request wall time. Non-streamed wall time is not time to first token.
- [ ] Usability: a fresh learner can follow the setup and distinguish authored calculations, model computation, sampling and the application loop.

If the 135M baseline cannot illustrate a required objective, first record the failing prompt/settings/output. A 360M comparison is a documented fallback, not a requirement to pursue frontier-model coverage. Pi RAM/latency targets remain provisional until measured.

## Recorded local observation

[Compact original observation record](observations/x86-smoke.json): Linux x86_64, AMD EPYC 9V74, CPython 3.12.14, two inference threads, 1,024-token context. Runtime/model hashes and requested settings are retained in that record. The model file is 144.8 MB; this is not peak RAM. Approximately 333 seconds covers runtime preparation, GGUF retrieval and notices on this machine, excluding installation of system tools/uv/CMake. It is not a Pi estimate.

| Experiment | Actual outcome | Interpretation |
| --- | --- | --- |
| Greedy reply, 32 tokens | Apologetic refusal rather than OK; limit stop | Exact instruction check failed |
| Extraction, 32 tokens | Claimed inability to provide real-time responses; limit stop | Extraction failed; preserve this as a limitation |
| Rewrite, 32 tokens | Omitted the count and changed account meaning; EOS stop | Natural termination observed; task fidelity failed |
| Opposite-word calibration | Identified cold, then continued until token cap | Simple bounded language relation worked; brevity/control remains weak |
| Temperature 0.5 versus 1.5 | First-token probability for The approximately 0.969 versus 0.160 | Temperature effect visible with identical first-token context |
| Top-k disabled versus five | Retained top-five mass rose to approximately one | Post-sampling distribution/filter effect observed |
| Seeded repeat | Identical generated IDs on this build | Local repeatability observed, not a cross-platform guarantee |
| One-token rewrite | The, limit stop | Output cap observed |

The baseline is useful for observing generation mechanics and a simple language relation. Exact-format instruction and evidence-extraction suitability remain **unvalidated/failed on these prompts**. The opposite-word prompt was added as a separate calibration after the original failures; it does not replace their checks. Do not claim a dependable security-task model from these results.

## Further observation template

Date / machine / RAM / OS / runtime commit / model hash / threads / context:

| Experiment | Actual output and stop | Task check | What changed or failed? |
| --- | --- | --- | --- |
| Greedy reply | | | |
| Sampled temperatures | | | |
| Top-k variation | | | |
| Seeded repeat | | | |
| Output cap and EOS | | | |
| Extraction or bounded task | | | |

Physical Pi 4 resource measurements, a fresh learner walkthrough, and the failed suitability items remain open. A successful x86 run does not establish Pi performance.
