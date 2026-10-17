# Generation and sampling

Status: runnable lesson and validation checklist; see [current evidence](VALIDATION.md). Estimated lesson time: 45–75 minutes after initial setup, a project estimate. Building the runtime is a separate first-time step.
Prerequisites: Python lists/numbers and a 64-bit Linux machine. Raspberry Pi 4 is a portability target. No running model, installed inference runtime or API account is assumed.

## Goal

Follow one inference from formatted input through next-token probabilities, selection, appended tokens and termination. Change one sampling setting and explain the observation. Use a small model that is sufficient for the instruction and bounded task; matching frontier-model capabilities is not a requirement.

The selected baseline is **SmolLM2-135M-Instruct, Q8_0**, using a pinned llama.cpp CPU runtime. Task suitability and physical Pi 4 operation are [validation items](VALIDATION.md#model-and-hardware-validation-checklist). The later [tool-feedback lesson](../tool-requests-and-feedback/README.md#run-the-observed-working-configuration) adds an explicit 360M comparison after the baseline failed to complete that exchange reliably; this sampling lesson still defaults to 135M. The model publisher describes [SmolLM2's training and intended use](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct); this course makes no general comparative capability claim.

## Start from a blank slate

The supplied setup path targets Debian/Ubuntu and 64-bit Raspberry Pi OS. Install system build tools once:

```bash
sudo apt update
sudo apt install -y build-essential git curl ca-certificates
```

Install uv following [Astral's original instructions](https://docs.astral.sh/uv/getting-started/installation/), then reopen the terminal if needed. From this repository's root:

```bash
uv python install 3.12
uv sync --frozen --group generation-setup
uv run --frozen --group generation-setup python modules/generation-and-sampling/lab/prepare.py --jobs 1
```

Initial setup needs PyPI, GitHub, huggingface.co and the Apache license site. The optional setup group pins CMake; system C++ and Git build the pinned runtime. The script downloads **144,811,360 bytes** of GGUF weights, verifies SHA-256, and retains the quantizer's original README and Apache-2.0 license. Runtime source retains its own license/notices. All artifacts stay in the ignored .cache/generation directory; nothing is installed system-wide by the script. No PyTorch, GPU toolkit, model account or provider key is required.

Allow additional disk space for source/build products and compiler tools; the GGUF size is not the total setup size or runtime RAM. Start with one build job on the Pi. Build time, peak RAM and latency on actual Pi hardware remain items to measure, not assumed results. Exact revisions, file hash and licensing are in [the source record](SOURCES.md).

Start the supplied server in **terminal A**:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/serve.py
```

It binds 127.0.0.1:8080, uses CPU only, four threads, one slot and a 1,024-token context. Wait for its ready/listening message. Keep it running; Ctrl-C stops it. If that port is occupied, use `--port 8091` and add `--base-url http://127.0.0.1:8091` to observation commands. No existing instance is reused silently.

The native server/API comes from [llama.cpp](https://github.com/ggml-org/llama.cpp). Python and uv orchestrate the lesson; the compiled runtime performs inference.

## Worked example: observe a short instruction

In **terminal B**, from the same repository root:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --task reply --mode greedy
```

The script applies the selected model's template, tokenizes that formatted prompt, and requests at most eight generated tokens. It prints the original/formatted input, prompt IDs, requested settings, generated IDs, returned per-token candidates, selected probabilities, stop reason and runtime timings. The task asks for only `OK`; check the actual answer rather than treating a finished generation as success.

The [native llama.cpp API](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/tools/server/README.md) exposes token probabilities. These are **not raw logits**, and the reported top eight candidates may omit substantial probability mass. The script displays the unreported mass instead of renormalizing that subset. A token's probability is not the probability that its answer is correct. Decoding a byte-fragment token individually can also give misleading text; inspect the full returned content and IDs.

## What happens inside this request?

The runtime processes the input tokens using learned weights and obtains scores for the next token. The sampler selects one token; the runtime appends it and repeats. A different selection changes the context for subsequent steps. [Karpathy's Deep Dive](https://www.youtube.com/watch?v=7xTGNNLPyMI) explains the model-generation mechanism; this script observes the runtime's outputs without reimplementing a transformer.

Training updates learned parameters. Pretraining learns from text; later instruction-oriented training changes how a model responds to formatted requests. Ordinary inference uses those weights to compute outputs; appending your prompt or a generated token does not itself train the model. See the [SmolLM2 original training description](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) for this model's specific process.

This token-generation loop is inside one call to Track 1's inference interface. Track 1's application loop resumes after the response and may dispatch a requested tool. No file-reading or shell tool is offered in this lesson.

## Predict and vary one setting

Hold the task and seed fixed. First compare two sampled temperatures, keeping top-k disabled:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --mode sample --temperature 0.5 --top-k 0
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --mode sample --temperature 1.5 --top-k 0
```

Then compare top-k at temperature one:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --mode sample --temperature 1 --top-k 0
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --mode sample --temperature 1 --top-k 5
```

For positive temperature T, a softmax turns scores z into probabilities proportional to exp(z/T). A lower T concentrates probability on higher scores; a larger T flattens it. Top-k first retains the k highest-scoring candidates in this lesson's explicit sampler order. Here zero means no top-k filter. Greedy chooses the maximum; this API uses temperature=-1 as its greedy control, not as a negative temperature in the formula.

The greedy observation requests ordinary softmax scores. Sampled observations request probabilities **after** the explicitly selected top-k/temperature chain. Compare the probability-stage label as well as numbers. Do not compare later-token distributions as if their context were unchanged: earlier sampled choices may already differ. These settings and probability-field meanings are specified in the pinned [server documentation](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/tools/server/README.md).

For the arithmetic alone, run this explicitly authored four-token example without starting the server:

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --example
```

At T=1, scores [2,1,0,-1] give approximately [0.644,0.237,0.087,0.032]. Top-k=2 gives approximately [0.731,0.269,0,0]. The small [calculation](lab/sampling.py) is original project code. It does not claim to be a model response or a complete-vocabulary reconstruction from the top-eight server output.

## Repeat, stop and check a task

```bash
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --mode sample --seed 7 --repeat 2
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --task rewrite --max-tokens 1
uv run --frozen --offline python modules/generation-and-sampling/lab/observe.py --task extract --max-tokens 16
```

Record whether repeated token IDs match; do not assume a seed guarantees identical output across builds, hardware or server configurations. The request disables prompt-cache reuse to reduce one confound. The [server documentation](https://github.com/ggml-org/llama.cpp/blob/f74e2fa6a31cc33ab4ee4ae516641cfe62df3924/tools/server/README.md) discusses batch/cache effects on repeatability.

Distinguish eos (model termination token), limit (output cap) and word (configured stop text). A one-token rewrite should make the output limit visible; inspect the actual stop rather than assuming it. To seek natural termination, rerun the short reply task with --max-tokens 32. If it still reaches the limit, record that outcome; an EOS demonstration remains unverified until observed.

The supplied [task prompts](lab/prompts.json) have checkable goals: exactly OK, exactly denied, a rewrite preserving three failed sign-ins, or the opposite of hot. Record successes and failures. These tasks test instructional usefulness, not whether a 135M model can run a general security agent.

> **What this demonstrates:** arithmetic on an authored score vector, plus observable generation from the locally configured model when run. Model suitability, runtime compatibility and Pi performance need actual observations recorded in the checklist. The client does not expose hidden model reasoning or measure factual confidence.

## Observed results to discuss

The [recorded x86 run](observations/x86-smoke.json) observed the expected sampling effects, repeatability, EOS and an output cap. It also failed the exact reply, extraction and faithful rewrite checks. A separate opposite-word calibration identified cold but was verbose. Preserve those distinctions: a model can make the mechanics visible while remaining unsuitable for a particular task. The original failed prompts stay in the lesson. Run `--task opposite` to compare the simpler language relation. Pi performance is still untested.

## Completion and troubleshooting

Explain one candidate distribution, one selected token, one deliberate sampling change and one terminal reason. Show whether the bounded task succeeded. Separate the runtime's generation loop from the harness's tool loop.

A missing compiler/Git error belongs to setup. A model hash mismatch requires re-preparing the pinned file, not accepting different bytes silently. A server connection error means terminal A is not ready or the port differs. Missing probability fields indicate a runtime/API mismatch; preserve the observation and compare the pinned build instead of inventing values. uv --offline blocks uv downloads; observation commands still contact the explicitly started loopback server.

Use synthetic prompts only. The server has no application tools; generated text is displayed, never executed. The script makes at most two completions per invocation, each capped at 64 output tokens and 256 input tokens. Context/RAM/server implementation can still affect performance.

> **Optional resource — Andrej Karpathy, Deep Dive into LLMs like ChatGPT**
> Explains training, inference and token generation beyond this bounded lab.
> [Original video](https://www.youtube.com/watch?v=7xTGNNLPyMI) · [makemore exercises](https://github.com/karpathy/makemore)

[Validation checklist](VALIDATION.md) · [Sources and exact setup](SOURCES.md) · [Active plan](../../docs/plans/active/04-generation-and-sampling.md) · [Collection](../../README.md)
