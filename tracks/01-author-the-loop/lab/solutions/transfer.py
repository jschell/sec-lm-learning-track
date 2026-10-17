"""Original worked answer for the count_lines transfer exercise."""
from loop import Workspace


def count_lines(workspace: Workspace, path: str) -> int:
    return len(workspace.read(path).splitlines())
