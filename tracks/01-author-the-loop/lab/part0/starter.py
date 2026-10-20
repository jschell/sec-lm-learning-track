"""Optional Part 0 exercise: write the loop yourself.

Copy this file, write run_conversation, then check it:
    uv run --frozen --offline python learn.py check --stage 0 --file YOUR_COPY.py
The worked version is minimal_loop.py next to this file; try before reading it.
"""
from collections.abc import Callable

SYSTEM = 'You can use the listed read-only tools. Answer from what they return.'


def request(conversation: list, tools) -> dict:
    """Everything the model receives: instructions, the whole conversation, the tools."""
    return {'system': SYSTEM, 'messages': conversation, 'tools': tools.definitions, 'max_tokens': 1024}


def run_conversation(model, tools, user_turns: list[str], show: Callable[[str, str], None]) -> list:
    """Return the whole conversation after every user turn has been answered.

    For each user turn: append it, ask the model (model.complete(request(...))), append its
    message, then, while that message proposes tool calls, run each with tools.dispatch(block),
    append all results as one user message, and ask again. show(label, text) is optional output.
    """
    raise NotImplementedError('Write the loop; see 00-the-loop.md, optional step')
