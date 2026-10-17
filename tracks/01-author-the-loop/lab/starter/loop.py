"""Lesson 3 starter. Independently runnable with cli.py --loop-file PATH.

Complete run_loop; do not import the solution's run_loop. The cli supplies
model, tools, prompt and trace. Helpers here are interfaces, not a framework.
"""

from loop import SYSTEM


def run_loop(model, tools, prompt, trace, max_turns=12, max_calls=24, max_tokens=1024, system=SYSTEM):
    messages = [{'role': 'user', 'content': prompt}]
    # 1. Preserve the supplied system instructions in the request, alongside messages, tools.definitions, max_tokens.
    # 2. Call model.complete(request); inspect response['stop_reason']/['content'].
    # 3. Append the assistant content before any tool results.
    # 4. Dispatch each tool_use, preserving its id; append all tool_result blocks
    #    together in the next user message. Continue with the updated messages.
    # 5. Return {'status': 'completed', 'messages': messages, 'tool_calls': count}
    #    on end_turn, or an explicit limit/error status. Never equate this to a grade.
    # 6. Add traces and preflight the whole batch against max_calls.
    # Reference SYSTEM and the worked implementation in ../loop.py AFTER trying.
    raise NotImplementedError('Author the inference/tool-feedback loop here')
