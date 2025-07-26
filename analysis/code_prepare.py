import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_codebase(source_path: str) -> Dict[str, Any]:
    """
    Scans a directory for .py files and collects basic metadata.

    Args:
        source_path (str): The path to the root of the source code directory.

    Returns:
        A dictionary containing the list of found Python files and metadata.
        Returns an empty dictionary if the path is invalid.
    """
    logging.info(f"Starting codebase analysis at: {source_path}")

    # Use pathlib for robust path handling
    root_path = Path(source_path)

    if not root_path.is_dir():
        logging.error(f"Invalid directory path provided: {source_path}")
        return {}

    # 1. Filter valid source files (.py) using rglob
    # rglob('*.py') recursively finds all files ending with .py
    logging.info("Filtering for .py source files...")
    python_files: List[Path] = list(root_path.rglob("*.py"))

    if not python_files:
        logging.warning("No Python files found in the provided directory.")
        return {
            "files": [],
            "metadata": {
                "file_count": 0,
                "total_size_kb": 0
            }
        }

    # 2. Collect basic metadata
    logging.info("Collecting basic metadata (file count, total size)...")
    file_count = len(python_files)
    total_size_bytes = sum(p.stat().st_size for p in python_files)
    total_size_kb = round(total_size_bytes / 1024, 2)

    metadata = {
        "file_count": file_count,
        "total_size_kb": total_size_kb
    }

    # Convert Path objects to strings for easier use later
    file_paths_str = [str(p) for p in python_files]

    logging.info(f"Analysis complete. Found {file_count} Python files.")

    return {
        "files": file_paths_str,
        "metadata": metadata
    }