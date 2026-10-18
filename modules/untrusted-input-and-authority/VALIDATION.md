# Validation record

Author check: 2026-10-17 (America/Los_Angeles), Python 3.12.15 / uv 0.12.23. No model inference, external action or secret access is performed.

```bash
uv run --frozen --offline python -m unittest discover -s modules/untrusted-input-and-authority/lab/tests -v
uv run --frozen --offline python -m unittest discover -s tracks/01-author-the-loop/lab/tests -v
```

## Performed

- Seven new tests pass: identical initial requests/authored responses with changed note bytes; same proposals across recording-only and enforcing paths plus denial reaching request 3; rejected operations/paths/extra fields never reaching the read primitive; description-only variation; negated approval fooling only the flawed recorder; allowed-filename symlink rejection without a completed read effect; and CLI persistence/overwrite refusal.
- Existing Track 1 suite: 43 tests pass. Its loop, command executor and guards are unchanged.
- Both documented commands ran successfully with fresh output directories. Targets remained unchanged, allowed reads are recorded, and forbidden execution count is zero. [Worked observations](worked-observations.md) distinguishes the separate cases.
- Source fixture comparison confirms the injected note reuses the original synthetic Track 1 bytes. Only its embedded instruction is added to the benign factual sentence.

[Authority CI](../../.github/workflows/authority.yml) runs both suites and both entry points on Python 3.12/3.13. Configuration does not imply completed CI; consult actual runs.

## Evidence status

| Evidence | Status |
| --- | --- |
| Actual file-result/next-request transition | Checked with identical authored responses |
| Recording-only flawed permission idea | Checked; never execution evidence |
| Exact dispatcher decisions and real allowed reads | Checked, including denial before read primitive |
| Authored attempted edit and matching denial feedback | Checked through the existing guarded loop |
| Actual model susceptibility/refusal | Unperformed; no live behavior claimed |
| Independent learner explanation/transfer | Pending |
| Physical Pi / fresh OS / full sandbox security | Not tested here |

No real private data or external communication is available in the exercise, so it does not reproduce all parts of the lethal trifecta. The source packet, code and tests establish this bounded behavior, not general injection prevention. [Original sources](SOURCES.md).
