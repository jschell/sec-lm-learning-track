# Part 0. The loop

> **Core route** — *The loop:* **Part 0 (you are here)** · [1 Exchange](pilot-worksheet.md#1-follow-one-exchange) · [2 Errors](pilot-worksheet.md#2-follow-feedback-after-an-error) · [Loop recap](core-loop.md) — *Controls:* [4 Budget](pilot-worksheet.md#4-change-one-controller-setting) — *Evidence:* [5 Transfer](pilot-worksheet.md#5-transfer-the-mechanism-to-a-new-tool) — *Application:* [Record](pilot-worksheet.md#explain-and-record-completion)

Status: authored; offline steps checked by tests. Planning estimate 30–45 minutes (a project judgment, not a measured learner time).
Prerequisites: reading short Python functions; the one-time [setup](README.md#prepare-once). No model, API key or Docker.

## Goal

Before any focus area, security included, establish base understanding of how an agent works. By the end of Part 0 you can show that:

1. A conversation is history that the application re-sends with every request.
2. A tool definition, a model's proposed call and the controller's dispatch are three different things.
3. A result goes back to the model as a message matched to its call by ID, including error results.
4. The loop repeats until the model stops proposing calls.
5. The whole loop is small.

Your check is to predict what request N+1 contains, given request N.

The order follows [Geoffrey Huntley's workshop](https://ghuntley.com/agent/): a chat program first, then a tool, then the same loop with more tools. His pinned repository builds an outer loop over user input and an inner loop that keeps running requested tools "until Claude stops using tools", returning tool failures as results marked as errors ([`chat.go`](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/chat.go), [`read.go`](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/read.go)). The Python here is original project code with the same shape: [lab/part0/minimal_loop.py](lab/part0/minimal_loop.py).

**How each step works.** Write your prediction first, run the command, watch the transcript, then open the checkpoint. The model's replies are scripted (authored in advance, not a real model), so you can compare your prediction with exactly the same run every time; file reads are real. Each run is kept under `.cache/exercises/track-1/part0-STEP/` and prints an `Inspect:` command you can use later.

## Step 1: a conversation is re-sent history

**Predict:** you tell the program your project code, then ask for it in a second message. The model keeps no memory between requests. How can the second reply know the code?

```bash
uv run --frozen --offline python learn.py part0 chat
```

<details><summary>Checkpoint</summary>

The program keeps a list called `conversation`. Each user turn and each model reply is appended to it, and the whole list is sent with every request. The second request contains three messages: your first turn, the model's reply and your second turn. The reply can mention the code because the code is in that request, not because the model remembered it. Drop the list and the second request would contain only "What is my project code?".

</details>

## Step 2: a tool is a definition plus a function

**Predict:** when the program offers the model a `read_file` tool, what does the model actually receive: the Python function, or something else?

```bash
uv run --frozen --offline python learn.py part0 tools
```

<details><summary>Checkpoint</summary>

The model receives only the definition: a name, a description and an input schema saying which arguments are expected. The function (`read_file()` in `minimal_loop.py`) stays in the program. When the model asks for a tool, `ReadOnlyTools.dispatch` looks the function up by name and runs it. A description grants no access: if no function is registered under that name, nothing runs and the model gets an error result instead.

</details>

## Step 3: one tool exchange

**Predict:** the model is asked to read `notes.txt`. Write the order of what happens: who proposes, who reads the file, and what is in the next request?

```bash
uv run --frozen --offline python learn.py part0 exchange
```

<details><summary>Checkpoint</summary>

The model's reply is a proposed call (`tool: read_file(...)`) with an ID. The program runs the function and builds a result carrying the same ID (`tool_use_id`). The next request contains the original question, the model's call and that result, in that order. Only then does the model answer. The ID, not the tool's name, ties the result to the call. This pairing follows [Anthropic's client-tool protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).

</details>

## Step 4: the loop, including an error

**Predict:** the model first asks for a file that does not exist. Does the program stop, skip the result, or send something back? How many requests will be made before the final answer?

```bash
uv run --frozen --offline python learn.py part0 loop
```

<details><summary>Checkpoint</summary>

The failed read becomes an ordinary result marked as an error, and it goes into the next request like any other result. The model then proposes a second read, which succeeds, and finally answers: three requests in total. This is the whole mechanism: ask the model; if it proposes calls, run each one, send every result back in one message, and ask again; stop when a reply proposes no calls. Read `run_conversation` in [minimal_loop.py](lab/part0/minimal_loop.py): the loop logic is about twenty lines.

What it deliberately lacks: it does not check why the model stopped, it has no limit on turns or calls, and it does not reject a repeated call ID. Huntley's loop has none of these either. Here it is safe only because Part 0 uses scripted replies and read-only tools. Later sections add these checks.

</details>

## Step 5: the same loop, more tools

**Predict:** add a `list_files` tool. What has to change in the loop itself?

```bash
uv run --frozen --offline python learn.py part0 more-tools
```

<details><summary>Checkpoint</summary>

Nothing in the loop changes. A new tool is one more definition and one more function; the loop runs whatever is requested and sends the results back. Huntley's later stages work the same way: each adds tools to an unchanged loop. Section 5 of the worksheet repeats this with a `count_lines` tool.

</details>

## Predict request N+1

Pick the second request from your step 4 run (open it with the printed `Inspect:` command, or the run's `trace.jsonl`). Without looking at the third request, write down exactly which messages it will contain, in order. Then check.

<details><summary>Checkpoint</summary>

Request 3 contains everything in request 2, then the model's second reply (its text and the `notes.txt` call), then one user message with that call's result. Nothing is removed; the list only grows.

</details>

## Key points

- The model receives a fresh request each time; the program re-sends the conversation.
- The model sees tool definitions and proposes calls; the program decides what runs.
- Every result, including an error, returns as a message matched to its call by ID.
- The loop asks, runs requested tools, sends the results, and asks again until no call is proposed.
- The loop is small. Most of what makes a real agent safe and reliable is added around it, not inside it.

## Optional: write the loop yourself

Copy [lab/part0/starter.py](lab/part0/starter.py), write `run_conversation`, then check it:

```bash
uv run --frozen --offline python learn.py check --stage 0 --file YOUR_COPY.py
```

The check uses a synthetic model that verifies each request contains your conversation and the actual results, including an error result, across several turns. It does not check limits; those come later. A passing check confirms the mechanics, not your understanding. Compare with the worked loop afterwards.

## Optional: the same loop with a real model

Part 0 refuses live runs on purpose. To see a real model drive the same kind of loop, use the [hosted read-only guide](live-observation.md) or the [local CPU route](../../modules/tool-requests-and-feedback/README.md#run-the-observed-working-configuration). Those use the guarded reference loop, and their results are separate evidence from this scripted step.

**Next in core:** [worksheet section 1: one exchange](pilot-worksheet.md#1-follow-one-exchange), which looks at the same exchange through the run record and adds the first checks.

## Sources

| Concept | Source | Verification / adaptation |
| --- | --- | --- |
| Chat first, then tools; nested loops; errors as results; same loop with more tools | [Huntley workshop](https://ghuntley.com/agent/); pinned [`chat.go`](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/chat.go) and [`read.go`](https://github.com/ghuntley/how-to-build-a-coding-agent/blob/fa3dd49fdddf45e92b35c66746e6bb6aac6ac27e/read.go); later stages listed in [SOURCES.md](SOURCES.md) | Inspected 2026-10-20 (UTC); original Python, no upstream code copied (the repository has no licence file) |
| Call/result pairing by ID, error results | [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | Protocol shape only; replay, no live API call |
| Base-understanding outcomes and step design | [Decision 0003](../../docs/decisions/0003-base-understanding-first.md) | Project judgment; not validated with learners yet |
