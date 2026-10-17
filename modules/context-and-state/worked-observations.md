# Worked observations

Recorded from the supplied offline script on 2026-10-17, Python 3.12.15. These are deterministic input/file observations, not model behavior or an independent learner pilot. Predict before comparing your run.

## State

`requests.json` contains two snapshots. Only the second includes the actual file contents in a result matching `read-status-1`. The counterfactual copy omits that result and is never sent. The source file and trace remain readable after the subprocess exits.

## Selection and summaries

These sizes describe rendered evidence, excluding the task, system message, JSON formatting and tool definitions. They are not token counts.

| Variant | Present IDs | Missing required IDs | Characters | UTF-8 bytes |
| --- | --- | --- | --- | --- |
| Full packet | C01, E01, E02, E03 | None | 374 | 376 |
| Query `alice` | E01, E02 | C01 | 172 | 172 |
| Faithful authored summary | C01, E01, E02 | None | 230 | 232 |
| Lossy authored summary | E01 | E02, C01 | 82 | 82 |

The full and faithful variants pass the literal checks. That means required ID/anchor strings occur, not that all claims are true. The lossy version even contains the substring `success` in an unsupported denial, illustrating why a word match is insufficient.

With query `collection gap`, only C01 remains. Neither keyword query alone supplies everything needed for the original question. The human review should identify both source disagreement and incomplete coverage.

`resume-without-loading.json` contains no summary, despite the note existing on disk. `resume-after-loading.json` includes the note after an explicit read. Both are inspection artifacts, not actual inference requests.

The [source record](SOURCES.md) supports the mechanisms; this packet, measurements and rubric are project-authored observations. Reproduce with the lesson commands; changing a fixture can change these values.
