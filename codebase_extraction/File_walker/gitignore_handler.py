# file_walker/gitignore_handler.py

from pathlib import Path
import logging
from typing import List, Tuple

# Try to import pathspec for .gitignore parsing
try:
    import pathspec
    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False
    logging.warning("`pathspec` not installed; .gitignore support disabled. Install with `pip install pathspec`.")

def load_all_gitignore_specs(repo_path: Path) -> List[Tuple[Path, "pathspec.PathSpec"]]:
    """
    Recursively find all .gitignore files in the repository and build pathspec matchers for each.
    Returns a list of tuples: (directory containing .gitignore, pathspec matcher).

    Args:
        repo_path (Path): The root directory of the repository.

    Returns:
        List[Tuple[Path, pathspec.PathSpec]]: List of (base_path, matcher) pairs.
    """
    ignore_specs = []
    if not PATHSPEC_AVAILABLE:
        logging.warning("pathspec not available — cannot parse .gitignore.")
        return ignore_specs

    # Search for all .gitignore files in repo
    for gi_path in repo_path.rglob(".gitignore"):
        try:
            lines = gi_path.read_text(encoding="utf-8").splitlines()
            spec = pathspec.PathSpec.from_lines("gitwildmatch", lines)
            ignore_specs.append((gi_path.parent, spec))
            logging.info(f"Loaded .gitignore from {gi_path} with {len(lines)} lines.")
        except Exception as e:
            logging.warning(f"Failed to parse {gi_path}: {e}")
    return ignore_specs

def is_ignored_by_any_gitignore(file_path: Path, ignore_specs: List[Tuple[Path, "pathspec.PathSpec"]]) -> bool:
    """
    Check if a file should be ignored by any .gitignore matcher in the repository.
    For each matcher, the file path is made relative to the directory containing the .gitignore.

    Args:
        file_path (Path): The file or directory path to check.
        ignore_specs (List[Tuple[Path, pathspec.PathSpec]]): List of (base_path, matcher) pairs.

    Returns:
        bool: True if the file is ignored by any matcher, False otherwise.
    """
    for base_path, matcher in ignore_specs:
        try:
            # Make file path relative to the .gitignore's directory
            rel_path = file_path.relative_to(base_path).as_posix()
            if matcher.match_file(rel_path):
                logging.debug(f"{file_path} ignored by .gitignore in {base_path}")
                return True
        except ValueError:
            # file_path is not under base_path; skip
            continue
        except Exception as e:
            logging.error(f"Error matching {file_path} against .gitignore in {base_path}: {e}")
    return False