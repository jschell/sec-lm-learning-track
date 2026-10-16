# Curriculum design sketch

Status: draft design · 2026-10-16

## Audience and learning objective

Security consultants who already understand investigation, evidence, access control, and Python. The objective is to understand and author a small loop, then learn how it fits defensible consulting workflows.

The learning unit is a capability, not a week, vendor, or video. Track 1 remains approximately 4–8 focused hours; this is a planning estimate, not a requirement. Later tracks are independently selectable and do not carry a fixed schedule.

## Structure

Use tracks/<track>/README.md for scope and navigation. Add numbered lesson Markdown files only as they are authored. Put runnable starter code, worked solutions, synthetic fixtures, and example traces beside the lesson or in clearly linked shared directories. Do not create empty placeholders that look like delivered lessons.

A lesson includes explanation, a complete worked example, a small exercise, observations, a completion check, troubleshooting, and citations. See the [template](../templates/module.md).

Baseline safety travels with runnable examples. Deeper evaluation and security material belongs in Tracks 4 and 5, without making either a prerequisite for the first contained exercise.

## One common exercise family

Use a synthetic investigation with event IDs, timestamps, a small rule, and conflicting indicator-enrichment responses. Introduce one capability at a time:
1. Inspect a broken toy program to learn loop mechanics.
2. Replace generic tools with bounded synthetic event/enrichment operations.
3. Produce a timeline with stable evidence references.
4. Check claims and detect incomplete results.
5. Attempt cross-engagement access and synthetic injection.
6. Hand the packaged workflow to another consultant.

This sequence is an original project proposal. It does not claim that a toy corpus proves operational detection quality.

## Pedagogy and technical choices

- Markdown is the primary surface; no website or notebook is required.
- Python examples will use uv and a locked environment once executable work begins.
- A provider SDK is allowed in the raw loop; an agent framework is introduced later.
- Saved synthetic responses support offline replay. Replay teaches protocol mechanics; live inference is a separate exercise with separately stated requirements.
- Preserve independent grader fixtures outside the agent's writable workspace.
- Local inference, MCP, tokenization implementation, training, and multi-model delegation are optional branches.
- No broad model leaderboard, framework survey, or production deployment is required.

## Foundations and attribution

[Huntley](https://ghuntley.com/agent/) supplies the hands-on loop starting point. [Anthropic's Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) supplies the workflow/agent distinction. [Karpathy's educational catalog](https://karpathy.ai/) supplies optional conceptual and model-internals material. These are sources of concepts, not authors of this design.

## Decisions still open

Track 1 chooses Python 3.12+, standard-library Anthropic REST transport (no SDK), JSON replay fixtures, and Docker-only command execution; see its source and validation records. Later consulting fixture schemas remain open. Select a project license separately. Do not make these unresolved choices prerequisites for reviewing the curriculum.

