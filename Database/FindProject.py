import os
from pathlib import Path


def find_project_root(search_filename=".git"):
    """
    Find the root directory of the project by looking for a specific file or directory.

    :param search_filename: The filename or directory to look for to identify the project root.
                            Defaults to '.git'.
    :return: The absolute path to the root directory of the project.
    """
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if (parent / search_filename).exists():
            return parent

    raise FileNotFoundError(f"Could not find the project root containing {search_filename}")

