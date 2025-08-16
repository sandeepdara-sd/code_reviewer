# file_walker/walker.py

import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from codebase_extraction.File_walker.config import EXCLUDE_FOLDERS, PARALLEL_FILE_COUNT, PARALLEL_AVG_FILE_KB, EXTENSION_TO_LANGUAGE
from codebase_extraction.File_walker.lang_cache import save_language_cache, add_extension_mapping, add_filename_mapping
from codebase_extraction.File_walker.metrics import get_file_size, count_lines, hash_file
from codebase_extraction.File_walker.notebook_handler import extract_ipynb_cells
from codebase_extraction.File_walker.gitignore_handler import load_all_gitignore_specs, is_ignored_by_any_gitignore
from codebase_extraction.File_walker.lang_detect import detect_language, resolve_unknowns

"""
walker.py — File Walker Orchestrator (with .gitignore, MIME, and batch LLM fallback)

Returns:
{
  "summary": {...},
  "file_map": { "<rel_path>": {...}, ... },
  "skipped_files": {
      "by_folder": [...],
      "by_gitignore": [...]
  }
}
"""

logger = logging.getLogger(__name__)


def should_exclude_by_folder(path: Path) -> bool:
    """
    Checks if a folder should be excluded based on EXCLUDE_FOLDERS.
    """
    return any(part in EXCLUDE_FOLDERS for part in path.parts)


def process_file(root: Path, file_path: Path) -> dict:
    """
    Processes a single file: language detection (no LLM), metrics collection.

    Returns:
        dict: File metadata.
    """
    language = detect_language(file_path, str(file_path.relative_to(root)))

    info = {
        "path": str(file_path.relative_to(root)),
        "language": language,
        "size_bytes": get_file_size(file_path),
        "lines": count_lines(file_path),
        "hash": hash_file(file_path),
    }

    # Notebook special handling
    if info["language"].lower() == "jupyter notebook":
        info["notebook_cells"] = extract_ipynb_cells(file_path)

    return info


def walk_directory(root_path: Path) -> dict:
    """
    Walks through the directory and returns a structured file map.

    Honors EXCLUDE_FOLDERS and repository .gitignore files (recursive).
    """
    root = Path(root_path)
    if not root.exists():
        logger.error("Root path does not exist: %s", root)
        return {}

    # Load all .gitignore specs (root plus nested)
    gitignore_spec = load_all_gitignore_specs(root)

    all_paths = [p for p in root.rglob("*") if p.is_file()]

    skipped_by_folder = []
    skipped_by_gitignore = []
    scannable = []

    for p in all_paths:
        # 1) exclude folders
        if should_exclude_by_folder(p):
            skipped_by_folder.append(str(p.relative_to(root)))
            continue

        # 2) apply gitignore rules
        if gitignore_spec and is_ignored_by_any_gitignore(p, gitignore_spec):
            skipped_by_gitignore.append(str(p.relative_to(root)))
            continue

        scannable.append(p)

    total_files = len(all_paths)
    scanned_files = len(scannable)

    # compute avg file size (KB) for the scannable set
    avg_file_kb = 0
    if scanned_files:
        avg_file_kb = (sum(get_file_size(f) for f in scannable) / scanned_files) / 1024

    logger.info(
        "Total files found: %d; will scan: %d; skipped by folder: %d; skipped by gitignore: %d",
        total_files, scanned_files, len(skipped_by_folder), len(skipped_by_gitignore)
    )
    logger.debug("Average scannable file size: %.2f KB", avg_file_kb)

    file_map = {}

    # decide parallelism
    use_parallel = scanned_files > PARALLEL_FILE_COUNT or avg_file_kb > PARALLEL_AVG_FILE_KB

    if use_parallel:
        logger.info("Using parallel processing for file scan...")
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_file, root, f): f for f in scannable}
            for future in as_completed(futures):
                try:
                    info = future.result()
                    file_map[info["path"]] = info
                except Exception as e:
                    logger.error("Error processing file: %s", e)
    else:
        logger.info("Using sequential processing for file scan...")
        for f in scannable:
            try:
                info = process_file(root, f)
                file_map[info["path"]] = info
            except Exception as e:
                logger.error("Error processing file %s: %s", f, e)

    # Resolve any unknown language entries in the file map
    resolve_unknowns(file_map)

    # Build summary AFTER resolutions
    summary = {
        "total_files_found": total_files,
        "scanned_files": len(file_map),
        "skipped_by_folder": len(skipped_by_folder),
        "skipped_by_gitignore": len(skipped_by_gitignore),
    }

    # Save the detected language information to the cache
    save_language_cache(file_map)

    return {
        "summary": summary,
        "file_map": file_map,
        "skipped_files": {
            "by_folder": skipped_by_folder,
            "by_gitignore": skipped_by_gitignore
        }
    }
