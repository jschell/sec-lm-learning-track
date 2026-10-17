"""Optional transfer: add behavior for the registered count_lines tool."""
from loop import Workspace


def count_lines(workspace: Workspace, path: str) -> int:
    """Read through workspace.read, then count splitlines (including blank lines)."""
    raise NotImplementedError('Implement the new read-only operation')
