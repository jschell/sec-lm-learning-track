"""Lessons 1 and 2 starter. Check with check_authoring.py --file PATH."""

def infer_once(model, prompt):
    # Build a request with system, messages, tools=[] and max_tokens=1024.
    # Return model.complete(request); do not run a tool here.
    raise NotImplementedError('Lesson 1: one inference request')


def exchange(model, tools, prompt):
    # Make one request with tools.definitions; append assistant content.
    # Dispatch its tool_use blocks and append their results as one user message.
    # Make a second request with the expanded history; return (response, messages).
    raise NotImplementedError('Lesson 2: one complete tool exchange')
