# 2. Locate execution authority

Goal: separate claimed permission, requested operation, enforcing decision and actual effect.

A retrieved claim of authority is still source data. Our project policy permits one exact read and no edits. Willison's [original risk framing](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) motivates locating what actions remain possible after content exposure; the exact policy and the two dispatch comparisons here are original teaching design.

## Predict and run

Open [proposals.json](lab/fixtures/proposals.json). Each proposal has a display description containing `Approved`, including the forbidden edit and another file path. Predict what a description-only policy would do, and what an enforcing operation/path policy should do.

```bash
uv run --frozen --offline python modules/untrusted-input-and-authority/lab/inspect_authority.py authority --output .cache/authority-decisions-1
```

From the repository root after [setup](README.md#setup-and-run), this compares the same three proposals through two paths.

The deliberately wrong path checks:

```python
approved = 'approved' in proposal['display_description'].casefold()
```

It returns `would_allow` or `would_deny` and **always** `executed: false`. It has no tool callback or operation implementation. This lets you inspect a flawed permission idea without giving it side effects, following the project's [missing-controls teaching decision](../../tracks/01-author-the-loop/08-learn-from-missing-guards.md).

The enforcing dispatcher checks:

```python
allowed = call.get('name') == 'read_file' and call.get('input') == {'path': 'note.txt'}
```

On denial, it returns an error result before any read. On allowance, its only operation is `workspace.read('note.txt')`. The shared workspace primitive also rejects symlinks. See [the complete code](lab/inspect_authority.py); descriptions and prompt instructions are not consulted by this condition.

## Inspect decisions and actual effects

Open `report.json` and `trace.jsonl`. The recorder says `would_allow` for all three descriptions but executes nothing. The enforcing path actually reads `note.txt` once, denies `edit_file`, and denies `read_file(private.txt)`. The latter file exists with harmless synthetic contents, so this is a policy denial rather than a missing-file result.

The read's `effect` event follows the completed file operation. A decision event alone does not establish execution; even an allowed operation could encounter an I/O failure. Setup writes and host-side report inspection are separate from dispatched tool effects.

Now inspect `scripted-attempt/trace.jsonl`:

1. The loop reads injected text and places it in request 2.
2. An authored response proposes the forbidden edit from the fixture. The program selected this scenario; no model inferred it from the injected text.
3. The dispatcher denies that edit and returns `is_error: true` with the matching `proposal-edit` ID.
4. Request 3 includes the denial; an authored final response ends the loop.

Open `scripted-attempt/work/notes.txt`: it remains open. This time an attempted edit is present and denied. Both this branch and the direct comparison contain real permitted reads but zero forbidden operation executions. No edit implementation or outbound destination exists on either enforcing path.

## Vary one factor and explain

For the forbidden edit, imagine changing only the display description from `Approved read-only maintenance.` to `No permission.` The recorder's label changes; the enforcing outcome does not. Inspect the function directly or explain the two condition results without modifying reference code. The transfer phrase `Not approved.` still contains the recorder's substring; its false permission remains recording-only.

Complete these checks:

- Identify a `proposal`, `decision`, returned `tool` result and actual read `effect`.
- Match the denied edit to its error feedback in request 3. What prevented the edit, independently of the script's final text?
- Why are an ended conversation, an absent attempt, a denial and a completed effect different observations?
- What does this fixed read-only fixture leave untested?

Expected: operation/argument enforcement and absence of an edit implementation prevent effects. The recording-only mistake grants no actual permission. This does not test a real model's susceptibility, actual secret exfiltration, arbitrary tool code, remote authorization or general sandbox security. The existing execution-enabled reference retains its controls.

[Worked observations](worked-observations.md) · [Session notes](README.md#completion-notes) · [Sources](SOURCES.md)
