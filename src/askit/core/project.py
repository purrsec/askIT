from pathlib import Path
from typing import Optional

def find_project_root() -> Optional[Path]:
    """
    Finds the project root by searching for a `.askit` directory.
    The search is performed from the current directory upwards to its parents.

    Returns:
        The path to the project root directory (containing .askit), or None if not found.
    """
    current_path = Path.cwd()
    for parent in [current_path] + list(current_path.parents):
        askit_dir = parent / ".askit"
        if askit_dir.is_dir():
            return parent
    return None 